# pyfnalsnow

This module provides libraries and scripts to interact with the FNAL
instance of <http://www.service-now.com>.

## Scripts

### Create: snow-incident-create, snow-ritm-create

Create Incidents and Requests/Requested Items, respectfully.  These work
directly with the REST API.

### Read: snow-incident-list, snow-ritm-list, snow-tkt, snow-tkt-list

Scripts to search and list Incident and Requested Items, respectfully.
snow-tkt-list calls both.

snow-tkt takes a ticket name and prints information about that ticket on
STDOUT.

### Update - many scripts

Most of these do what they say on the tin:

* snow-tkt-assign - assign a ticket to a user and/or group
* snow-tkt-journal - record a journal entry or comment to a ticket
* snow-tkt-pending - set a ticket to status pending (mostly for RITMs)
* snow-tkt-resolve - resolve a ticket
* snow-tkt-unassign - assign a ticket back to the Help Desk

### Delete

No such thing.  Data doesn't generally get removed from

## Requirements

This script requires [pysnow](https://github.com/rbw0/pysnow).  I would
probably just update it directly except that I don't know for sure what
changes we have made locally that don't apply to the "default" instance.

Note that modern `pysnow` doesn't run on RHEL6 derivatives, so I've dropped
support for that OS.

### Configuration File

`/etc/snow/config.yaml` looks something like:

    servicenow:
        username: '(USERNAME)'
        url:      'https://(SITENAME).service-now.com/'
        password: '(PASSWORD)'
        instance: '(INSTANCE)'

    ritm_template:
        priority: '3'
        u_categorization: 'Hardware -- Worker Node -- No Item Available'
        urgency: '3'
