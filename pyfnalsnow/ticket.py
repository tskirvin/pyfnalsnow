"""
pyfnalsnow.ticket
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
    """

    d = iso8601.parse_date("%sZ" % string)
    return d.strftime("%Y-%m-%d %H:%M:%S")

def formatText(text, **kwargs):
    """
    Add the 'prefix' field to a simple text field.  This may need
    improvement.
    """

    prefix = wrap_defaults['prefix']
    if prefix in kwargs: prefix = kwargs['prefix']

    ret = []
    for i in text.split("\n"): ret.append("%s%s" % (prefix, i))
    return ret

def formatTextField(field, value, **kwargs):
    """
    """

    minWidth = wrap_defaults['minWidth']
    if minWidth in kwargs: minWidth = kwargs['minWidth']

    prefix = wrap_defaults['prefix']
    if prefix in kwargs: prefix = kwargs['prefix']

    width = wrap_defaults['width']
    if prefix in kwargs: prefix = kwargs['width']

    if value: v = value
    else:     v = '*unknown*'

    w = "%s %%s" % ( '%%-%ss' % minWidth )

    text = textwrap.wrap (
        w % ("%s:" % field, v),
        initial_indent = prefix,
        subsequent_indent = ' ' * (len(prefix) + minWidth + 1),
        width = width
    )
    return text

#########################################################################
### Ticket Strings ######################################################
#########################################################################

def tktStringBase(tkt):
    """
    """

    ret = []
    ret.extend(tktStringPrimary(tkt))
    ret.append('')

    ret.extend(tktStringRequestor(tkt))
    ret.append('')

    ret.extend(tktStringAssignee(tkt))
    ret.append('')

    ret.extend(tktStringDescription(tkt))
    ret.append('')

    # ret.extend(tktStringJournal(tkt))
    # ret.append('')

    if pyfnalsnow.tktIsResolved(tkt):
        ret.extend(tktStringResolution(tkt))
        ret.append('')

    return ret

def tktStringAssignee(tkt):
    """
    """

    extra = {}
    ret = []
    ret.append('Assignee Info')
    ret.extend(formatTextField('Group', tktAssignedGroup(tkt), **extra))
    ret.extend(formatTextField('Name',  tktAssignedPerson(tkt), **extra))
    ret.extend(formatTextField('Last Modified',
        formatDate(tktDateUpdate(tkt)), **extra))

    return ret

def tktStringDescription(tkt):
    """
    """
    extra = {}
    ret = []
    ret.append("User-Provided Description")
    ret.extend(formatText(tkt['description']), **extra)
    return ret

def tktStringJournal(tkt):
    """
    """
    extra = {}
    ret = []
    journals = pyfnalsnow.tktJournalEntries(tkt)
    if len(journals) < 1: return ret

    ret.append('Journal Entries')
    for i in journals:
        print i
        ret.extend(i)

    return ret


def tktStringPrimary(tkt):
    """
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

    return ret

def tktStringRequestor(tkt):
    extra = {}
    ret = []
    
    requestor = pyfnalsnow.userByUsername(tktRequestPerson(tkt))

    ret.append('Requestor Info')
    ret.extend(formatTextField('Name',  requestor['name'],  **extra))
    ret.extend(formatTextField('Email', requestor['email'], **extra))

    return ret


def tktStringResolution(tkt):
    """
    """
    extra = {}
    ret = []
    ret.append("Resolution")
    print tkt
    # ret.extend(formatTextField('Resolved By',  tktResolvedBy(tkt),  **extra))
    # ret.extend(formatTextField('Date', formatDate(tktDateResolved(tkt)),
    #     **extra))
    # ret.extend(formatTextField('Close Code',  tktResolvedCode(tkt), **extra))
    ret.append('')
    ret.extend(formatText(tkt['close_notes']), **extra)

    return ret

#########################################################################
### Ticket Field Conversions ############################################
#########################################################################
## Given a ticket with all fields, pull out printable information.  This
## is primarily used internally.

def groupLink(group):
    if isinstance(group, dict):
        if 'value' in group:
            g = pyfnalsnow.groupById(group['value'])
            return g['name']
    return group

def userLink(user):
    if isinstance(user, dict):
        if 'value' in user:
            u = pyfnalsnow.userById(user['value'])
            return u['name']
    return user

def tktAssignedPerson(tkt): return userLink(tkt['assigned_to'])
def tktAssignedGroup(tkt):  return groupLink(tkt['assignment_group'])
def tktCallingPerson(tkt):  return tkt['caller_id']
def tktDateResolved(tkt):   return tkt['resolved_at']
def tktDateSubmit(tkt):     return tkt['opened_at']
def tktDateUpdate(tkt):     return tkt['sys_updated_on']
def tktNumber(tkt):         return tkt['number']
def tktPriority(tkt):       return tkt['priority']
def tktRequestPerson(tkt):  return tkt['sys_created_by']
def tktResolvedBy(tkt):     return userLink(tkt['resolved_by'])
def tktResolvedCode(tkt):   return tkt['close_code']
def tktServiceType(tkt):    return tkt['u_service_type']

def tktStatus(tkt):
    for i in ['dv_incident_state', 'u_itil_state']:
        if i in tkt: return tkt[i]
    return ''

def tktState(tkt):          return tkt['state']
def tktSummary(tkt):        return tkt['short_description']
def tktUrgency(tkt):        return tkt['urgency']
