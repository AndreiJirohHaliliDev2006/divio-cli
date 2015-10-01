import re
import os
import subprocess
from time import sleep

import click

from ..utils import dev_null, execute
from . import utils


GIT_CLONE_URL = 'git@git.aldryn.com:{slug}.git'


def get_docker_compose_cmd(path):
    docker_compose_base = [
        'docker-compose', '-f', os.path.join(path, 'docker-compose.yml')
    ]

    def docker_compose(*commands):
        return docker_compose_base + [cmd for cmd in commands]

    return docker_compose


def create_workspace(client, website_slug, path=None):
    click.secho('Creating workspace...', fg='green')

    path = os.path.abspath(
        os.path.join(path, website_slug)
        if path else website_slug
    )

    docker_compose = get_docker_compose_cmd(path)
    website_git_url = GIT_CLONE_URL.format(slug=website_slug)

    try:
        click.secho('\ncloning project repository', fg='green')
        clone_args = ['git', 'clone', website_git_url]
        if path:
            clone_args.append(path)
        execute(clone_args, silent=False, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        raise click.ClickException(exc.output)

    # Detect old style or invalid projects
    if not os.path.isfile(os.path.join(path or website_slug, 'docker-compose.yml')):
        raise click.ClickException(
            "Aldryn local development only works with projects using "
            "baseproject version 3 and have a valid 'docker-compose.yml' file."
        )

    existing_db_container_id = execute(
        docker_compose('ps', '-q', 'db'),
        silent=True,
    ).replace(os.linesep, '')

    # stop all running for project
    execute(docker_compose('stop'), silent=True)

    # pull docker images
    click.secho('downloading remote docker images', fg='green')
    execute(docker_compose('pull'), silent=False, stderr=subprocess.STDOUT)

    # build docker images
    click.secho('building local docker images', fg='green')
    execute(docker_compose('build'), silent=False, stderr=subprocess.STDOUT)

    if existing_db_container_id:
        click.secho('removing old database container', fg='green')
        execute(
            docker_compose('stop', 'db'),
            stderr=subprocess.STDOUT,
            silent=False,
        )
        execute(
            docker_compose('rm', '-f', 'db'),
            stderr=subprocess.STDOUT,
            silent=False,
        )

    click.secho('creating new database container', fg='green')
    load_database_dump(client, website_slug, path, recreate=True)

    instructions = [
        "Finished setting up your project's workspace!",
        "To start the project, please:",
    ]

    if path:
        instructions.append(' - change directory into {}'.format(path))
    instructions.append(' - run aldryn project up')

    click.secho('\n\n{}'.format(os.linesep.join(instructions)), fg='green')


def load_database_dump(client, website_slug, path=None, recreate=False):
    path = path or utils.get_project_home(path)
    docker_compose = get_docker_compose_cmd(path)

    start_db_cmd = ['up', '-d']
    if recreate:
        start_db_cmd.append('--force-recreate')
    start_db_cmd.append('db')

    # start db
    execute(
        docker_compose(*start_db_cmd),
        stderr=subprocess.STDOUT,
        silent=True,
    )

    # get db container id
    db_container_id = execute(
        docker_compose('ps', '-q', 'db'),
        stderr=subprocess.STDOUT,
        silent=True,
    ).replace(os.linesep, '')

    click.secho('fetching database dump', fg='green')
    db_dump_path = client.download_db(website_slug, directory=path)
    # strip path from dump_path for use in the docker container
    db_dump_path = db_dump_path.replace(path, '')

    # waiting another 10 seconds to make sure the db has enough time to start
    sleep(10)

    # create empty db
    try:
        execute([
            'docker', 'exec', db_container_id,
            'dropdb', '-U', 'postgres', 'db',
        ], silent=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        pass

    execute([
        'docker', 'exec', db_container_id,
        'createdb', '-U', 'postgres', 'db',
    ], silent=True, stderr=subprocess.STDOUT)

    click.secho('inserting database dump', fg='green')
    # FIXME: because of different ownership,
    # this spits a lot of warnings which can
    # ignored but we can't really validate success
    with dev_null() as devnull:
        try:
            piped_restore = (
                'tar -xzOf /app/{}'
                ' | pg_restore -U postgres -d db'
                .format(db_dump_path)
            )

            subprocess.call((
                'docker', 'exec', db_container_id,
                '/bin/bash', '-c', piped_restore,
            ), stdout=devnull, stderr=devnull)
        except subprocess.CalledProcessError:
            pass

    # stop db
    execute(
        docker_compose('stop'),
        silent=True,
        stderr=subprocess.STDOUT,
    )


def develop_package(package, no_rebuild=False):
    """
    :param package: package name in addons-dev folder
    """

    project_home = utils.get_project_home()
    addons_dev_dir = os.path.join(project_home, 'addons-dev')

    if not os.path.isdir(os.path.join(addons_dev_dir, package)):
        raise click.ClickException(
            'Package {} could not be found in {}. Please make '
            'sure it exists and try again.'
            .format(package, addons_dev_dir)
        )

    url_pattern = re.compile('(\S*/{}/\S*)'.format(package))
    new_package_path = '-e /app/addons-dev/{}\n'.format(package)

    # add package to requirements.in for dependencies
    requirements_file = os.path.join(project_home, 'requirements.in')
    # open file with 'universal newline support'
    # https://docs.python.org/2/library/functions.html#open
    with open(requirements_file, 'rU') as fh:
        addons = fh.readlines()

    replaced = False

    for counter, addon in enumerate(addons):
        if re.match(url_pattern, addon) or addon == new_package_path:
            addons[counter] = new_package_path
            replaced = True
            break

    if not replaced:
        # Not replaced, append to generated part of requirements
        for counter, addon in enumerate(addons):
            if '</INSTALLED_ADDONS>' in addon:
                addons.insert(counter, new_package_path)
                replaced = True
                break

    if not replaced:
        # fallback: generated section seems to be missing, appending
        addons.append(new_package_path)

    with open(requirements_file, 'w') as fh:
        fh.writelines(addons)

    if not no_rebuild:
        # build web again
        docker_compose = get_docker_compose_cmd(project_home)

        try:
            execute(
                docker_compose('build', 'web'),
                silent=True,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as exc:
            raise click.ClickException(exc.output)

    click.secho(
        'The package {} has been added to your local development project!'
        .format(package)
    )


def open_project(open_browser=True):
    docker_compose = get_docker_compose_cmd(os.getcwd())
    try:
        addr = execute(docker_compose('port', 'web', '80'), silent=True)
    except subprocess.CalledProcessError:
        click.secho(
            "Your project is not running. Please start it using "
            "'aldryn project up'.", fg='red'
        )
        return
    host, port = addr.split(':')

    if host == '0.0.0.0':
        docker_host_url = os.environ.get('DOCKER_HOST')
        if docker_host_url:
            proto, server_host_port = os.environ.get('DOCKER_HOST').split('://')
            host = server_host_port.split(':')[0]

    addr = 'http://{host}:{port}/'.format(
        host=host.replace(os.linesep, ''),
        port=port.replace(os.linesep, ''),
    )
    if open_browser:
        click.launch(addr)
    click.secho('Your project is running at {}'.format(addr), fg='green')
    return addr


def start_project():
    docker_compose = get_docker_compose_cmd(os.getcwd())
    execute(docker_compose('up', '-d'))
    return open_project(open_browser=False)


def stop_project():
    docker_compose = get_docker_compose_cmd(os.getcwd())
    execute(docker_compose('stop'))
