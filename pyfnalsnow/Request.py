"""
pyfnalsnow.Request
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

#########################################################################
### Subroutines #########################################################
#########################################################################

def tktFilter():
    """
    """
    return ''


def tktIsResolved(tkt):
    """
    Returns True if the RITM is resolved, False otherwise.
    """
    return False

def tktResolve(tkt, **args):
    """
    """

    raise Exception ('not yet implemented')
