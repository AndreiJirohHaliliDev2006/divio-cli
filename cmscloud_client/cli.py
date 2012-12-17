# -*- coding: utf-8 -*-
import sys
from cmscloud_client import __version__ as version
from cmscloud_client.client import Client
import docopt
import os

__doc__ = """django CMS cloud client.

Usage:
    cmscloud login
    cmscloud boilerplate upload
    cmscloud boilerplate validate

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --settings=<settings>       Settings file to use [default: settings.py].
    --language=<lang>           Language to use [default: en].
    --manage=<manage>           Path to manage.py [default: manage.py].
"""


def main():
    args = docopt.docopt(__doc__, version=version)
    client = Client(os.environ.get('CMSCLOUD_HOST', 'https://cloud.django-cms.com'))
    retval = True
    if args['login']:
        retval = client.login()
    elif args['boilerplate']:
        if args['upload']:
            retval = client.upload_boilerplate()
        elif args['validate']:
            retval = client.validate_boilerplate()
    sys.exit(int(retval))
