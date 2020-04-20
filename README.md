# pyfnalsnow

This module provides Python libraries and scripts to interact with 
[Service Now](http://www.service-now.com).  This was designed to work with
a specific instance of SNOW (FNAL), but these scripts and libraries will 
probably work with other sites, so it's worth sharing.

## Scripts

### Create: snow-incident-create, snow-ritm-create

Create Incidents and Requests/Requested Items, respectfully.  These work
directly with the REST API.

### Read: snow-incident-list, snow-ritm-list, snow-tkt, snow-tkt-list

Scripts to search and list Incident and Requested Items, respectfully.
snow-tkt-list calls both.

snow-tkt takes a ticket name and prints information about that ticket on
STDOUT.

### Update: many scripts

Most of these do what they say on the tin:

* snow-tkt-assign - assign a ticket to a user and/or group
* snow-tkt-journal - record a journal entry or comment to a ticket
* snow-tkt-pending - set a ticket to status pending (mostly for RITMs)
* snow-tkt-resolve - resolve a ticket
* snow-tkt-unassign - assign a ticket back to the Help Desk

### Delete: No Such Thing

Data doesn't generally get removed from SNOW, at least not by users.

## libraries

### pyfnalsnow

Creates and caches the connections to SNOW; caches searches; provides the
CRUD interface that the various scripts depend on; provides tools for
user/group searches; abstracts out the various ticket types (Incidents,
Requests, Tasks, Requested Items, etc); and works with a central
configuration file (`/etc/snow/config.yaml`) so that we can abstract
server/authentication data away from the user.

### pyfnalsnow.ticket

This mostly provides template functions for the various 
sub-tables (e.g. `Incident`): printing functions, mapping some functions
to field names, etc.

### pyfnalsnow.Incident, pyfnalsnow.Request, pyfnalsnow.RITM

Functions that must be customized per-table are stored here; for instance,
RITMs must change state several times to get to a pending or resolved
state.

## Requirements

This script requires [pysnow](https://github.com/rbw0/pysnow).  I would
probably just update it directly except that I don't know for sure what
changes we have made locally that don't apply to the "default" instance.

To make this work on RHEL6 and a modern `pysnow` you probably want to
install oauthlib 2.0.7: `pip install oauthlib==2.0.7`.

### Configuration File

`/etc/snow/config.yaml` looks something like:

    servicenow:
        username: '(USERNAME)'
        url:      'https://(SITENAME).servicenowservices.com/'
        password: '(PASSWORD)'
        hostname: '(SITENAME).servicenowservices.com'

    ritm_template:
        priority: '3'
        u_categorization: 'Hardware -- Worker Node -- No Item Available'
        urgency: '3'
