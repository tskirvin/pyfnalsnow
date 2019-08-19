"""
pyfnalsnow.Request
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
    raise Exception('not yet implemented')
