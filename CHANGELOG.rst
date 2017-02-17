Changelog
=========

3.1.0 (2017-02-11)
------------------

* Execute migration commands when running ``divio project update``
* Add support to decrypt encrypted backups with ``divio backup decrypt``
* Fix an issue on windows by specifying ``--format=gztar`` when building addons, thanks to @bertah
* More leftover renamings from ``aldryn`` to ``divio``


3.0.1 (2016-11-15)
------------------

* rename remanding 'aldryn' strings with their new 'divio' counterparts


3.0.0 (2016-11-15)
------------------

* rename from aldryn-client to divio-cli
* improve ``aldryn version``: now shows more upgrade paths and more detailed information
* add script for testing unix builds on multiple linux distros


2.3.5 (2016-10-21)
------------------

* Fix bug in ``aldryn project push db``
* Harden ``aldryn project push media`` command


2.3.4 (2016-10-19)
------------------

* Add ``--noinput`` flags to push media and database commands


2.3.3 (2016-10-19)
------------------

* Add ``aldryn project import/export db`` commands
* Doctor checks can now be disabled through the global ``.aldryn`` file
* ``aldryn project update`` now detects the current git branch
* Make login status check more resilient by not relying on its own executable to be findable in `PATH`
* Fix issues with ``aldryn addon/boilerplate upload`` in Python 3
* Fix error with recursive delete on windows during project setup


2.3.2 (2016-07-05)
------------------

* enable postgis if local database supports it


2.3.1 (2016-06-06)
------------------

* Fix unicode issue in ``aldryn login``


2.3.0 (2016-06-06)
------------------

* Cleanup and improve boilerplate upload
* Boilerplate now uses ``excluded`` instead of ``protected`` to specify included files
* ``--debug`` now shows more info on API request errors
* Fix form meta in python 3 projects
* Fix CLI description for ``addon develop``


2.2.4 (2016-05-26)
------------------

* Fix an issue with quotes in the doctor's DNS check
* Test if a check exists when using ``aldryn doctor -c``


2.2.3 (2016-05-26)
------------------

* Push and pull db/media from test or live stage
* Check for login status in ``aldryn doctor``
* Fix an issue on some platforms with timeout in the doctor's DNS check
* freeze PyInstaller version to fix building the binaries


2.2.2 (2016-05-10)
------------------

* Use plain requests for media and database downloads
* Send the user agent with API requests
* Fix some python3 compatibility issues


2.2.1 (2016-04-26)
------------------

* Fix ``aldryn doctor`` failing on the ``docker-machine`` step (it's not strictly required)


2.2 (2016-04-07)
----------------

* Release binary package for Linux, OS X and Windows
* Improve ``aldryn doctor`` command
* Replaced usage of ``exit`` with ``sys.exit`` for compatibility
* Fixes an issue in local dev setup with newer Docker version (docker exec changed)


2.1.7 (2016-02-19)
------------------

* Do not mangle the hostname when using the client as a library
* Fix a bug in the update notification


2.1.6 (2016-02-16)
------------------

* ``aldryn project deploy`` command
* netrc: catch errors
* netrc: fix regression introduced in 2.1.5


2.1.5 (2016-02-10)
------------------

* Fixes various bugs with Python 3 bytes vs strings


2.1.4 (2016-02-01)
------------------

* Adds a workaround for postgres hstore support


2.1.3 (2016-01-27)
------------------

* Fixes a bug in ``aldryn addon register`` where the passed args were in the wrong order


2.1.2 (2016-01-20)
------------------

* Fixes bug in version checker where it failed if there's no newer version available


2.1.1 (2016-01-20)
------------------

* PyPi errored during upload, reuploading with patch 2.1.1


2.1 (2016-01-20)
----------------

* Python 3 support (experimental)
* Automated update checker
* New command ``aldryn addon register``
* Improve ordering and grouping of ``aldryn project list``
* Introduces a system for a config file


2.0.5 (2015-12-17)
------------------

* Issue a warning instead of failing on missing boilerplate files.
* Fix ``media`` directory size calculation during ``aldryn project push media``.


2.0.4 (2015-11-05)
------------------

* Don't set DB permissions when uploading the database.


2.0.3 (2015-10-29)
------------------

* More robust push/pull commands for db and media.
* Encode database dump log into utf-8 before writing the file.


2.0.2 (2015-10-21)
------------------

* Fix for local directory permissions on Linux (https://github.com/aldryn/aldryn-client/pull/98).
* Don't automatically delete a project after a failed setup.
  Users are prompted to delete the project if trying to set it up again.


2.0.1 (2015-10-14)
------------------

* Change push database / media confirmation texts to represent the actual state.


2.0 (2015-10-13)
----------------

* Brand new client, entirely rewritten from scratch and now completely dockerized.
* Ready for the new Aldryn baseproject (v3).
