"""

"""

#########################################################################
### Configuration #######################################################
#########################################################################

config_file = '/etc/snow/config.yaml'
config = {}

types = {
    'incident':   'Incident',
    'prjtask':    'Project Task',
    'sc_request': 'Request',
    'ritm':       'Requested Item',
    'task':       'Task',
}

modules = {
    'incident':    'pyfnalsnow.Incident',
    'sc_req_item': 'pyfnalsnow.RITM',
}

#########################################################################
### Declarations ########################################################
#########################################################################

import pysnow, re, yaml
import pyfnalsnow.Incident, pyfnalsnow.RITM
import sys

#########################################################################
### Configuration Subroutines ###########################################
#########################################################################

def pyfnalsnow_config(file):
    """
    Load a yaml configuration from a configuration file.  Sets a global
    'config' variable.
    """
    global config

    try:
        config = yaml.load(open(config_file, 'r'))
    except IOError, e:
        print "file error:  %s" % e
        sys.exit (2)
    except Exception, e:
        print "unknown error:  %s" % e
        sys.exit (2)

    return config


#########################################################################
### pysnow wrappers #####################################################
#########################################################################

def connect():
    """
    Connect to ServiceNow with credentials from the configuration file.
    Returns the pysnow client object directly.
    """

    global snow

    snow = pysnow.Client(
        instance=config['servicenow']['instance'],
        user=config['servicenow']['username'],
        password=config['servicenow']['password'],
        raise_on_empty=True)

    return snow

#########################################################################
### Reporting Functions #################################################
#########################################################################

def tktSwitch(tkt, function):
    """
    Black Magic Ahoy!  Given a function name and a ticket, invokes that
    function *from the matching class*.  
    """
    try:    number = tkt['number']
    except: raise Exception('no ticket number in ticket')
    type = tktType(number)

    if type in modules: 
        return eval("%s.%s" % (modules[type], function))(tkt)
    else: 
        raise Exception('unsupported type: %s' % type)

def tktIsResolved(tkt): return tktSwitch(tkt, 'tktIsResolved')
def tktStringBase(tkt): return tktSwitch(tkt, 'tktStringBase')

#########################################################################
### ServiceNow Searching ################################################
#########################################################################


def groupById(id):
    """
    """

    q = snow.query(table='sys_user_group', query={ 'sys_id': id })
    e = q.get_one()
    return e

def ritmByNumber(number):
    """
    """
    r = snow.query(table='sc_req_item', query={'number': number})
    ritm = r.get_one()
    return ritm

def userById(id):
    """
    Queries and returns a single sys_user entry based on a user sys_id.
    """
    q = snow.query(table='sys_user', query={ 'sys_id': id })
    return q.get_one()

def userByName(name):
    """
    """
    q = snow.query(table='sys_user', query={ 'name': name })
    return q.get_one()

def userByUsername(name):
    """
    """
    q = snow.query(table='sys_user', query={ 'user_name': name })
    return q.get_one()

def tktJournalEntries(tkt):
    """
    Given a full ticket, query for journal entries.
    """

    number = tkt['number']

    s = snow
    q = s.query(table='sys_journal_field', query={ 'element_id': tkt['sys_id'] })
    entries = q.get_all()

    ret = []
    journals = {}
    for i in entries:
        key = i['sys_created_on']
        journals[key] = i

    for i in sorted(journals.iterkeys()):
        ret.append(journals[key])

    return ret

#########################################################################
### Ticket Internals ####################################################
#########################################################################

def tktNumberParse(number):
    """
    Convert human-provided ticket numbers to the correct style for
    ServiceNow.  This means a) set the length correctly by ticket type and
    b) if we don't have a type, assume INC.  

    Note that this doesn't cover the case where we get a number that is
    too long.
    """

    m = re.match('^(TASK|RITM|INC|REQ|PRJTASK)(\d+)$', number, re.IGNORECASE)
    if m:
        type = m.group(1).upper()
        num  = m.group(2)
        length = len(number)
        if type == 'INC':     return 'INC%s%s'     % ('0' * (15 - length), num)
        if type == 'REQ':     return 'REQ%s%s'     % ('0' * (15 - length), num)
        if type == 'TASK':    return 'TASK%s%s'    % ('0' * (11 - length), num)
        if type == 'RITM':    return 'RITM%s%s'    % ('0' * (11 - length), num)
        if type == 'PRJTASK': return 'PRJTASK%s%s' % ('0' * (11 - length), num)
        raise 'unknown ticket type: %s' % type

    elif re.match('^(\d+)$', number):
        return "INC%s%s" % ('0' * (12 - len(number)), number)

    else:
        raise 'could not parse "%s"' % number

def tktType(number):
    """
    Given a ticket number, return the matching ServiceNow table name.
    """

    num = tktNumberParse(number)
    m = re.match('^(TASK|RITM|INC|REQ|PRJTASK)(\d+)$', num, re.IGNORECASE)
    if m:
        type = m.group(1).upper()
        if type == 'INC':       return 'incident'
        if type == 'PRJTASK':   return 'pm_project_task'
        if type == 'REQ':       return 'sc_request'
        if type == 'RITM':      return 'sc_req_item'
        if type == 'TASK':      return 'sc_task'

    raise 'unknown ticket type for %s' % number


#########################################################################
### main () #############################################################
#########################################################################

pyfnalsnow_config(config_file)
