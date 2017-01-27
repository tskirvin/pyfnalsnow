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

#########################################################################
### Subroutines #########################################################
#########################################################################

def tktFilter(status='open', **args):
    """
    """

    extra = []
    if status.lower() == 'open':
        extra.append('state>3')
        extra.append('stage!=Request Cancelled')
    elif status.lower() == 'closed':
        extra.append('state<=3')
    elif status.lower() == 'unresolved':
        extra.append('state>=3')

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
        extra.append('sys_created_by=%s' % user['sys_id'])


    search='^'.join(extra)

    return search


def tktIsResolved(tkt): return False
