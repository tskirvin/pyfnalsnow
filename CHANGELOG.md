# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.3] - 2021-07-06

* Incident.py - changing how we detect resolved tickets.
* Incident.py - tktStringResolution() sees cancelled tickets and
  prints different information for them
* ticket.py - tktStringResolution() sees cancelled tickets and
  prints different information for them

## [1.4.2] - 2020-12-01

* Incident.py - can now search by ticket age
* Incident.py - added debugging information to tktFilter()
* snow-incident-list - search by ticket age

## [1.4.1] - 2020-11-16

* RITM.py - tktIsResolved() now says "False" for work-in-progress tickets
* various Exceptions fixed

## [1.4.0] - 2020-04-20

* added CentOS 8 support (mostly Requires and BuildRequires work)
* snow-tkt - documentation formatting fix
* no longer using 'instance', now need 'hostname' for configuration
  (because instance isn't stable enough)
* `userLink()` - more general form of userLinkName() and usrLinkUsername()
* snow-tkt-assign - bug fixes for `--debug` call

## [1.3.2] - 2019-11-14

* fixes to make user 'guest' work more cleanly without crashing snow-tkt
    - __init__.py - CacheQueryOne() now returns None instead of a weird
      'value' block
    - ticket.py - touch-ups for Requestor Info block
    - * snow-tkt - better job of reporting exceptions

## [1.3.1] - 2019-08-19

* RITM.py - 'unresolved' search in tktFilter() now includes 'pending'.
  'open' does not.

## [1.3.0] - 2019-08-19

### Changed

* Incident.py - dropping all of the 'stage' search bits from tktFilter()
  because that field doesn't exist in SNOW (it's left over from Remedy-land)
* Converted all scripts and libraries to python 3
* RedHat .spec file now works with epel + python36
* ran all python through flake8 python linter, cleaned it up to match

### Dropped

* no longer building for RHEL 6

## [1.2.3] - 2019-03-20

### Added

* CHANGELOG.md - standardizing on a single changelog file

### Changed

* Makefile.local - now includes Pypi (pip) bindings
* setup.py, omdclient.spec - re-worked for setuptools instead of distutils.core
* README.md - lots of updates on the path towards real distribution

