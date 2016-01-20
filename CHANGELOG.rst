Changelog
=========

2.1.2 (2016-01-20)
------------------

* Fixes bug in version checker where it failed if there's no newer version available


2.1.1 (2016-01-20)
------------------

* PyPi errored during upload, reuploading with patch 2.1.1


2.1 (2016-01-20)
------------------

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
