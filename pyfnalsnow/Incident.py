"""
pyfnalsnow.Incident - parse Incident objects.  These are pretty much the
"default"
"""

#########################################################################
### Declarations ########################################################
#########################################################################

import pyfnalsnow

from pyfnalsnow.ticket import tktStringAssignee     # noqa:F401
from pyfnalsnow.ticket import tktStringAudit        # noqa:F401
from pyfnalsnow.ticket import tktStringBase         # noqa:F401
from pyfnalsnow.ticket import tktStringBaseAudit    # noqa:F401
from pyfnalsnow.ticket import tktStringDebug        # noqa:F401
from pyfnalsnow.ticket import tktStringDescription  # noqa:F401
from pyfnalsnow.ticket import tktStringJournal      # noqa:F401
from pyfnalsnow.ticket import tktStringPrimary      # noqa:F401
from pyfnalsnow.ticket import tktStringRequestor    # noqa:F401
# from pyfnalsnow.ticket import tktStringResolution # noqa:F401
from pyfnalsnow.ticket import tktStringShort        # noqa:F401
from pyfnalsnow.ticket import tktStringSummary      # noqa:F401

#########################################################################
### Configuration #######################################################
#########################################################################

state = {
    '1': 'Assigned',
    '2': 'Work In Progress',
    '6': 'Resolved',
    '7': 'Closed',
    '8': 'Cancelled'
}

resolve_code = 'Other (must describe below)'

#########################################################################
### Subroutines #########################################################
#########################################################################

def tktFilter(status='open', **args):
    """
    Filter tickets.
    """

    extra = []
    if status.lower() == 'open':
        extra.append('incident_state<4')
    elif status.lower() == 'closed':
        extra.append('incident_state>=4')
    elif status.lower() == 'unresolved':
        extra.append('incident_state<6')

    if 'unassigned' in args:
        extra.append('assigned_to=NULL')

    if 'group' in args:
        group = pyfnalsnow.groupByName(args['group'])
        extra.append('assignment_group=%s' % group['sys_id'])

    if 'assigned' in args:
        user = pyfnalsnow.userByUsername(args['assigned'])
        extra.append('assigned_to=%s' % user['sys_id'])

    if 'submit' in args:
        user = pyfnalsnow.userByUsername(args['submit'])
        extra.append('sys_created_by=%s' % user['user_name'])

    if 'caller' in args:
        user = pyfnalsnow.userByUsername(args['caller'])
        try:
            extra.append('caller_id=%s' % user['sys_id'])
        except: pass

    search = '^'.join(extra)

    return search

def tktIsResolved(tkt):
    if int(tkt['incident_state']) >= 4: return True
    else: return False

def tktPending(tkt, **kwargs):
    """
    Set an incident to status 'pending'.  This isn't *really* a thing for
    Incidents, though.

    kwargs:
      reason    String; default is 'Customer'
    """

    try:    reason = kwargs['reason']
    except: reason = 'Customer'

    new = {'u_pending_reason': reason}
    return pyfnalsnow.tktUpdate(tkt['number'], new)

def tktStringResolution(tkt):
    """
    """
    extra = {}
    ret = []
    ret.append("Resolution")
    resolvedBy = pyfnalsnow.userLinkName(tkt['resolved_by'])
    ret.extend(pyfnalsnow.ticket.formatTextField('Resolved By', resolvedBy,  **extra))
    ret.extend(pyfnalsnow.ticket.formatTextField('Date', tkt['resolved_at'], **extra))
    ret.append('')
    ret.extend(pyfnalsnow.ticket.formatText(tkt['close_notes']), **extra)
    ret.append('')

    return ret

def tktResolve(tkt, update, goal=6, **kwargs):
    """
    Resolve an incident.  Set the state to 6 (or something from the call), the
    resolution code to something known, and the text and user fields come from
    the 'update' hash.
    """

    if goal is None: goal = 6

    new = {
        'close_code': resolve_code,
        'close_notes': update['text'],
        'incident_state': goal,
        'resolved_by': update['user']
    }

    return pyfnalsnow.tktUpdate(tkt['number'], new)
