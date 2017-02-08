""" 
pyfnalsnow.Incident
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
    '1': 'Assigned',
    '2': 'Work In Progress',
    '6': 'Resolved',
    '7': 'Closed',
    '8': 'Cancelled'
}

#########################################################################
### Subroutines #########################################################
#########################################################################

def tktIsResolved(tkt):
    if tkt['state'] >= 4: return True
    else:                 return False
