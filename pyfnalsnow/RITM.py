"""
pyfnalsnow.RITM
"""

#########################################################################
### Declarations ########################################################
#########################################################################

import pyfnalsnow
from pyfnalsnow.ticket import tktStringAssignee
from pyfnalsnow.ticket import tktStringAudit
from pyfnalsnow.ticket import tktStringBase
from pyfnalsnow.ticket import tktStringBaseAudit
from pyfnalsnow.ticket import tktStringDebug
from pyfnalsnow.ticket import tktStringDescription
from pyfnalsnow.ticket import tktStringJournal
from pyfnalsnow.ticket import tktStringPrimary
from pyfnalsnow.ticket import tktStringRequestor
from pyfnalsnow.ticket import tktStringResolution
from pyfnalsnow.ticket import tktStringShort
from pyfnalsnow.ticket import tktStringSummary

#########################################################################
### Configuration #######################################################
#########################################################################

state = {
    -5: 'Pending',
     3: 'Closed',
    11: 'Complete',
    20: 'Waiting for Acknowledgement',
    21: 'Acknowledged',
    23: 'Work in Progress',
    24: 'Cancelled'
}


#########################################################################
### Subroutines #########################################################
#########################################################################

def tktFilter(status='open', **args):
    """
    Filter tickets.
    """

    extra = []
    if status.lower() == 'open':
        extra.append('state>3')
        extra.append('state!=24')
        extra.append('state!=11')
    elif status.lower() == 'closed':
        extra.append('state==3')
    elif status.lower() == 'unresolved':
        extra.append('state>3')
        extra.append('state<24')
        extra.append('state!=11')

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

    search='^'.join(extra)

    return search


def tktIsResolved(tkt):
    """
    Returns True if the RITM is resolved, False otherwise.
    """
    if tkt['state'] == '3':  return True        # closed
    if tkt['state'] == '24': return True        # cancelled
    if tkt['state'] == '23': return True        # work in progress?  huh?
    if tkt['state'] == '11': return True        # Complete
    else:                    return False

def tktResolve(tkt, update, goal=3):
    """
    Trying to get to 3 (closed) or 24 (cancelled).  Not very well tested.
    """

    ###########################
    ### valid state changes ###
    ###########################

    # -5 -> 23, 24
    #  3 -> no way out
    # 11 -> no way out
    # 20 -> 21, 24(?)
    # 21 -> 23, 24
    # 23 -> -5, 3, 24
    # 24 -> no way out

    new = { 'goal': goal }

    state = tkt['state']
    if state == goal: return tkt

    if state == -5:
        if   goal ==  3: new['status'] = 23
        elif goal == 24: new['status'] = 24
        else: new['state'] = goal
    elif state ==  3: raise Exception('cannot change state from 3')
    elif state == 11: raise Exception('cannot change state from 11')
    elif state == 20:
        if   goal ==  3: new['state'] = 21
        elif goal == 24: new['state'] = 24
        else: new['state'] = goal
    elif state == 21:
        if   goal ==  3: new['status'] = 23
        elif goal == 24: new['status'] = 24
        else: raise Exception('not a valid goal for resolution')
    elif state == 23:
        if   goal ==  3: new['status'] = 3
        elif goal == 24: new['status'] = 24
        else: raise Exception('not a valid goal for resolution')
    elif state == 24: raise Exception('cannot change state from 24')

    return tktResolve (pyfnalsnow.tktUpdate(tkt, new), goal=goal, **args)
