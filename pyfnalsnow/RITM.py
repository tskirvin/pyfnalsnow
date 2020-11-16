"""
pyfnalsnow.RITM
"""

#########################################################################
### Declarations ########################################################
#########################################################################

import pyfnalsnow   # noqa:F401
from pyfnalsnow.ticket import tktStringAssignee     # noqa:F401
from pyfnalsnow.ticket import tktStringAudit        # noqa:F401
from pyfnalsnow.ticket import tktStringBase         # noqa:F401
from pyfnalsnow.ticket import tktStringBaseAudit    # noqa:F401
from pyfnalsnow.ticket import tktStringDebug        # noqa:F401
from pyfnalsnow.ticket import tktStringDescription  # noqa:F401
from pyfnalsnow.ticket import tktStringJournal      # noqa:F401
from pyfnalsnow.ticket import tktStringPrimary      # noqa:F401
from pyfnalsnow.ticket import tktStringRequestor    # noqa:F401
from pyfnalsnow.ticket import tktStringResolution   # noqa:F401
from pyfnalsnow.ticket import tktStringShort        # noqa:F401
from pyfnalsnow.ticket import tktStringSummary      # noqa:F401

#########################################################################
### Configuration #######################################################
#########################################################################

state = {
    -5: 'Pending',
     3: 'Closed',       # noqa:E121
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
    if status.lower() == 'open':            # not pending, closed, cancelled, complete
        extra.append('state!=-5')
        extra.append('state!=3')
        extra.append('state!=24')
        extra.append('state!=11')
    elif status.lower() == 'closed':
        extra.append('state==3')
    elif status.lower() == 'unresolved':    # not closed, cancelled, complete
        extra.append('state!=3')
        extra.append('state!=24')
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

    search = '^'.join(extra)

    return search


def tktIsResolved(tkt):
    """
    Returns True if the RITM is resolved, False otherwise.
    """
    if tkt['state'] == '3': return True         # closed
    if tkt['state'] == '24': return True        # cancelled
    if tkt['state'] == '23': return False       # work in progress?
    if tkt['state'] == '11': return True        # Complete
    else: return False

def tktPending(tkt, **kwargs):
    """
    Set the state of this RITM to 'pending' (-5).  As with tktResolve(),
    this is complicated because you have to move from one state to
    another in a very specific manner.

    kwargs:
      debug     Boolean; default False
      reason    String; default is 'Customer'
    """

    goal = -5

    try:    debug = kwargs['debug']
    except: debug = False

    try:    reason = kwargs['reason']
    except: reason = 'Customer'

    new = {}

    state = tkt['state']
    if debug: print("initial state: %s  goal state: %s" % (state, goal))

    if int(state) == int(goal):
        if debug: print("nothing to do (already in goal state)")
        return tkt

    if int(state) == -5: raise Exception('at goal state')
    elif int(state) == 3: raise Exception('cannot change state from 3')
    elif int(state) == 11: raise Exception('cannot change state from 11')
    elif int(state) == 20: new['state'] = 21
    elif int(state) == 21: new['state'] = 23
    elif int(state) == 23: new['state'] = -5
    elif int(state) == 24: raise Exception('cannot change state from 24')
    else: raise Exception('invalid start state: %s' % state)

    if debug: print("updating goal state to %s" % new['state'])

    if new['state'] == int(goal):
        if debug: print("going to goal state, will also set u_pending_reason")
        new['u_pending_reason'] = reason

    updated = pyfnalsnow.tktUpdate(tkt['number'], new)
    return tktPending(updated, **kwargs)


def tktResolve(tkt, update, **kwargs):
    """
    Resolve an RITM.  This is complicated because there are a very
    specific list of state changes for the 'state' field that are
    acceptable.  The goal must be either 3 (closed, default) or 24
    (cancelled).

    update is a dict of key/value pairs that will be used for making
    updates.  You must pass in 'text' (will be used as close_notes).

    kwargs:
      debug     Boolean, default False
      goal      Integer, default 3, must be either 3 or 24.

    """

    try:    goal = int(kwargs['goal'])
    except: goal = 3

    if goal == 3: pass
    elif goal == 24: pass
    else: raise Exception('invalid goal state: %d' % goal)

    try: text = update['text']
    except: raise Exception('required field: text')

    try:    debug = kwargs['debug']
    except: debug = False

    new = {}

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

    state = tkt['state']

    if debug: print("initial state: %s  goal state: %s" % (state, goal))

    if int(state) == int(goal):
        if debug: print("nothing to do (already in goal state)")
        return tkt

    if int(state) == -5:
        if goal == 3: new['state'] = 23
        elif goal == 24: new['state'] = 24
        else: new['state'] = goal
    elif int(state) == 3: raise Exception('cannot change state from 3')
    elif int(state) == 11: raise Exception('cannot change state from 11')
    elif int(state) == 20:
        if goal == 3: new['state'] = 21
        elif goal == 24: new['state'] = 24
        else: new['state'] = goal
    elif int(state) == 21:
        if goal == 3: new['state'] = 23
        elif goal == 24: new['state'] = 24
        else: raise Exception('not a valid goal for resolution')
    elif int(state) == 23:
        if goal == 3: new['state'] = 3
        elif goal == 24: new['state'] = 24
        else: raise Exception('not a valid goal for resolution')
    elif int(state) == 24: raise Exception('cannot change state from 24')
    else:
        raise Exception('invalid start state: %s' % state)

    if debug:
        print("updating goal state to %s" % new['state'])

    if new['state'] == int(goal):
        if debug: print("going to goal state, will also set close_notes")
        new['close_notes'] = text

    updated = pyfnalsnow.tktUpdate(tkt['number'], new)
    return tktResolve(updated, update, **kwargs)
