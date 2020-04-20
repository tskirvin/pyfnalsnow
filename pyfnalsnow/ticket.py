"""
pyfnalsnow.ticket - general functions for interacting with Service Now
ticket-like objects (incidents, requested items, etc).  This will rarely
be called directly, but will be the basis of (e.g.) pyfnalsnow.RITM.
"""

#########################################################################
### Declarations ########################################################
#########################################################################

import iso8601
import pyfnalsnow
import textwrap

#########################################################################
### Configuration #######################################################
#########################################################################

textwidth = 80

wrap_defaults = {'minWidth': 20, 'prefix': '  ', 'width': 80}

#########################################################################
### Subroutines #########################################################
#########################################################################

#########################################################################
### Format Subroutines ##################################################
#########################################################################

def formatDate(string):
    """
    Takes a date from a SNOW date field, parses it, and returns in a
    consistent format.
    """

    d = iso8601.parse_date("%sZ" % string)
    return d.strftime("%Y-%m-%d %H:%M:%S")

def formatText(text, **kwargs):
    """
    Add the 'prefix' field to a simple text field.  This may need
    improvement.
    """

    prefix = wrap_defaults['prefix']
    if 'prefix' in kwargs: prefix = kwargs['prefix']

    ret = []
    for i in text.split("\n"): ret.append("%s%s" % (prefix, i))
    return ret

def formatTextField(field, value, **kwargs):
    """
    Given a field and a value, return a consistently-format using textwrap.
    Takes the parameters 'prefix', 'width', and 'minWidth'
    """

    minWidth = wrap_defaults['minWidth']
    if 'minWidth' in kwargs: minWidth = kwargs['minWidth']

    prefix = wrap_defaults['prefix']
    if 'prefix' in kwargs: prefix = kwargs['prefix']

    width = wrap_defaults['width']
    if 'width' in kwargs: width = kwargs['width']

    if value: v = value
    else:     v = '*unknown*'

    w = "%s %%s" % ('%%-%ss' % minWidth)

    text = textwrap.wrap(
        w % ("%s:" % field, v),
        initial_indent=prefix,
        subsequent_indent=' ' * (len(prefix) + minWidth + 1),
        width=width
    )
    return text

#########################################################################
### Ticket Strings ######################################################
#########################################################################

def tktStringBase(tkt):
    """
    Return a printable array containing basic information about a given
    ticket.  This information is pulled from other tktString calls:
    tktStringPrimary, tktStringRequestor, tktStringAssignee,
    tktStringDescription, tktStringJournal, and tktStringResolution.
    """

    ret = []
    ret.extend(pyfnalsnow.tktStringPrimary(tkt))
    ret.append('')

    ret.extend(pyfnalsnow.tktStringRequestor(tkt))
    ret.append('')

    ret.extend(pyfnalsnow.tktStringAssignee(tkt))
    ret.append('')

    ret.extend(pyfnalsnow.tktStringDescription(tkt))
    ret.append('')

    ret.extend(pyfnalsnow.tktStringJournal(tkt))
    ret.append('')

    if pyfnalsnow.tktIsResolved(tkt):
        ret.extend(pyfnalsnow.tktStringResolution(tkt))
        ret.append('')

    return ret

def tktStringBaseAudit(tkt):
    """
    Return a printable array containing the Primary and Audit ticket data.
    """
    ret = []
    ret = []
    ret.extend(pyfnalsnow.tktStringPrimary(tkt))
    ret.append('')

    ret.extend(pyfnalsnow.tktStringAudit(tkt))
    ret.append('')

    return ret

def tktStringAssignee(tkt):
    """
    Return a printable array containing assignee information for a ticket:
    the assigned group, the assigned name, and the last time the ticket
    was updated.  Everything is run through formatTextField for a
    consistent layout.
    """

    extra = {}
    ret = []
    ret.append('Assignee Info')
    ret.extend(formatTextField('Group', tktAssignedGroup(tkt), **extra))
    ret.extend(formatTextField('Name',  tktAssignedPerson(tkt), **extra))
    ret.extend(formatTextField('Last Modified',
        formatDate(tktDateUpdate(tkt)), **extra))

    return ret

def tktStringAudit(tkt):
    """
    Return a printable array containing audit data for a ticket, skipping
    data where the 'update' field is 0.
    """

    history = pyfnalsnow.tktHistory(tkt)

    count = 0
    ret = []
    for i in history:
        if 'update' in i:
            if i['update'] != '0':
                count = count + 1
                field = i['field']
                old = i['old']
                new = i['new']
                ret.append('Audit Entry %s' % count)
                ret.extend(formatTextField('Date', i['update_time']))
                ret.extend(formatTextField('Updated By', i['user_id']))
                ret.extend(formatTextField('Field', field))
                ret.extend(formatTextField('Old', old))
                ret.extend(formatTextField('New', new))
                ret.append('')

    return ret


def tktStringDebug(tkt):
    """
    Returns a printable array containing all fields and values in this
    ticket, run through formatTextField for a consistent layout.
    """
    ret = []
    ret.append('== %s (%s) ==' % (tkt['number'], tkt['sys_id']))
    width = 0
    for key in tkt:
        if len(key) > width: width = len(key)

    for key in sorted(tkt):
        ret.extend(formatTextField(key, tkt[key],
            minWidth=width + 1, prefix=''))

    return ret

def tktStringDescription(tkt):
    """
    Returns a printable array containing the ticket 'description' field,
    run through formatText.
    """
    extra = {}
    ret = []
    ret.append("User-Provided Description")
    ret.extend(formatText(tkt['description']), **extra)
    return ret

def tktStringJournal(tkt):
    """
    Returns a printable array of journal entries for this ticket.  Gets
    the journals using tktJournalEntries.
    """

    depth1 = {'prefix': '    '}
    ret = []
    journals = pyfnalsnow.tktJournalEntries(tkt)
    if len(journals) < 1: return ret

    ret.append('Journal Entries')

    count = 1
    for i in journals:
        ret.append('  Entry %s' % count)
        count = count + 1
        ret.extend(formatTextField('Date', formatDate(tktCreatedOn(tkt)), **depth1))
        ret.extend(formatTextField('Created By', i['sys_created_by'], **depth1))
        ret.extend(formatTextField('Type', i['element'], **depth1))
        ret.append('')
        ret.extend(formatText(i['value'], prefix='    '))
        ret.append('')

    return ret


def tktStringPrimary(tkt):
    """
    Returns a printable array of "primary" information about this ticket:
    ticket number, summary (short description), status, submitted date,
    urgency, and priority.
    """
    extra = {'minWidth': 20, 'prefix': '  '}
    ret = []
    ret.append("Primary Ticket Information")
    ret.extend(formatTextField('Number',  tktNumber(tkt),  **extra))
    ret.extend(formatTextField('Summary', tktSummary(tkt), **extra))
    ret.extend(formatTextField('Status',  tktStatus(tkt),  **extra))
    ret.extend(formatTextField('Submitted', formatDate(tktDateSubmit(tkt)),
        **extra))
    ret.extend(formatTextField('Urgency', tktUrgency(tkt), **extra))
    ret.extend(formatTextField('Priority', tktPriority(tkt), **extra))
    if 'cmdb_ci' in tkt:
        ret.extend(formatTextField('CI', tktCiName(tkt), **extra))

    return ret

def tktStringRequestor(tkt):
    """
    Returns a printable array of information about the requestor of this
    ticket, specifically their Name and Email.
    """
    extra = {}
    ret = []
    ret.append('Requestor Info')

    requestor = tktCallingPerson(tkt)
    if requestor is not None:
        username = pyfnalsnow.userLink(requestor)
        if username is not None:
            ret.extend(formatTextField('Name',  username['name'], **extra))
            ret.extend(formatTextField('Email', username['email'], **extra))
        else:
            ret.extend(formatTextField('Name',  '', **extra))
            ret.extend(formatTextField('Email', '', **extra))
    else:
        ret.extend(formatTextField('Name',  '', **extra))
        ret.extend(formatTextField('Email', '', **extra))

    ret.extend(formatTextField('Submitted-By', tktRequestPerson(tkt), **extra))

    return ret

def tktStringResolution(tkt):
    """
    Returns a printable string summarizing the resolution data - who
    resolved the RITM, when this happened, and any associated 'close
    notes'.
    """
    extra = {}
    ret = []
    ret.append("Resolution")
    resolvedBy = pyfnalsnow.userLinkName(tkt['closed_by'])
    ret.extend(formatTextField('Resolved By', resolvedBy,  **extra))
    ret.extend(formatTextField('Date', tkt['closed_at'], **extra))
    ret.append('')
    ret.extend(formatText(tkt['close_notes']), **extra)
    ret.append('')

    return ret

def tktStringShort(tkt):
    """
    Like tktStringBase(), but skips the WorkLog data.
    """
    ret = []
    ret.extend(pyfnalsnow.tktStringPrimary(tkt))
    ret.append('')

    ret.extend(pyfnalsnow.tktStringRequestor(tkt))
    ret.append('')

    ret.extend(pyfnalsnow.tktStringAssignee(tkt))
    ret.append('')

    ret.extend(pyfnalsnow.tktStringDescription(tkt))
    ret.append('')

    if pyfnalsnow.tktIsResolved(tkt):
        ret.extend(pyfnalsnow.tktStringResolution(tkt))
        ret.append('')

    return ret

def tktStringSummary(tkt):
    """
    Returns a printable string summarizing important data about the given
    ticket in three lines: number, requestor, assigned group and
    individual, current status, created/update datetime, and short
    description.
    """

    ret = []

    number = tkt['number']

    assignee = pyfnalsnow.userLinkUsername(tkt['assigned_to'])
    if assignee: assign = assignee
    else:        assign = '*unassigned*'

    requestor = pyfnalsnow.userLinkUsername(tkt['sys_created_by'])
    if requestor: request = requestor
    else:         request = '*unknown*'

    group = tktAssignedGroup(tkt)
    status = tktStatus(tkt)

    ret.append("%-15.15s %-14.14s %-14.14s %-16.16s %17.17s" %
        (number, request, assign, group, status))

    created = formatDate(tktDateSubmit(tkt))
    updated = formatDate(tktDateUpdate(tkt))
    if 'cmdb_ci' in tkt:
        ci_text = tktCiName(tkt)
    else: ci_text = 'no CI'

    ret.append(" Created: %-19.19s  Updated: %-19.19s  CI: %-15.15s" %
        (created, updated, ci_text))

    description = tktSummary(tkt)
    ret.append(' Subject: %-70.70s' % description)

    return ret

#########################################################################
### Ticket Field Conversions ############################################
#########################################################################
## Given a ticket with all fields, pull out printable information.  This
## is primarily used internally.

def _FieldOrEmpty(tkt, *field):
    """
    """
    for i in field:
        if i in tkt: return tkt[i]

    return None

def tktAssignedPerson(tkt): return pyfnalsnow.userLinkName(tkt['assigned_to'])
def tktAssignedGroup(tkt): return pyfnalsnow.groupLink(tkt['assignment_group'])
def tktCallingPerson(tkt): return _FieldOrEmpty(tkt, 'caller_id')
def tktCiName(tkt):
    try:
        ci_entry = tkt['cmdb_ci']
        ci = pyfnalsnow.ciById(ci_entry['value'])
    except: return None

    if 'name' in ci: return ci['name']
    else: return 'unknown'

def tktCreatedOn(tkt): return _FieldOrEmpty(tkt, 'sys_created_on')
def tktDateResolved(tkt): return tkt['resolved_at']
def tktDateSubmit(tkt): return _FieldOrEmpty(tkt, 'opened_at')
def tktDateUpdate(tkt): return tkt['sys_updated_on']
def tktNumber(tkt): return tkt['number']
def tktPriority(tkt): return tkt['priority']
def tktRequestPerson(tkt): return tkt['sys_created_by']
def tktResolvedBy(tkt): return pyfnalsnow.userLinkName(tkt['resolved_by'])
def tktResolvedCode(tkt): return tkt['close_code']
def tktServiceType(tkt): return tkt['u_service_type']

def tktStatus(tkt):
    for i in ['dv_incident_state', 'u_itil_state']:
        if i in tkt: return tkt[i]
    return ''

def tktState(tkt): return tkt['state']
def tktSummary(tkt): return tkt['short_description']
def tktUrgency(tkt): return tkt['urgency']
