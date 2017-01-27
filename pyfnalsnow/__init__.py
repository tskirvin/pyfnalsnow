"""

"""

#########################################################################
### Configuration #######################################################
#########################################################################

config_file = '/etc/snow/config.yaml'
config = {}

cache = {}

modules = {
    'incident':    'pyfnalsnow.Incident',
    'sc_req_item': 'pyfnalsnow.RITM',
}

types = {
    'incident':   'Incident',
    'prjtask':    'Project Task',
    'sc_request': 'Request',
    'ritm':       'Requested Item',
    'task':       'Task',
}


#########################################################################
### Declarations ########################################################
#########################################################################

import pysnow, re, sys, yaml
import pyfnalsnow.Incident, pyfnalsnow.RITM

#########################################################################
### Definitions #########################################################
#########################################################################

impact = {}
priority = {}
urgency = {
    '1': '1 - Critical',
    '2': '2 - High',
    '3': '3 - Medium',
    '4': '4 - Low',
}

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
        raise_on_empty=True
    )

    return snow

#########################################################################
### pyfnalsnow wrappers #################################################
#########################################################################

def cacheQueryOne(table, query):
    """

    """
    if table not in cache: cache[table] = {}

    q = str(query)

    if q in cache[table]: 
        return cache[table][q]
    else: 
        r = snow.query(table=table, query=query)
        try:
            result = r.get_one()
        except:
            result = '(no match)'
        cache[table][q] = r.get_one()
    return cache[table][q]

def tableSwitch(table, function, **args):
    """
    Black Magic Ahoy!  Given a function name and a table type, invokes that
    function *from the matching class*.  
    """
    if table in modules: 
        return eval("%s.%s" % (modules[table], function))(**args)
    else: 
        raise Exception('unsupported table: %s' % type)

def typeSwitch(tkt, function):
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

#########################################################################
### Reporting Functions #################################################
#########################################################################

def printSearchSummary(type, query='group', subquery='open', **args):
    """
    """
    return None
    

def tktString (tkt, type='base', *args, **kwargs):
    """
    """

    if   type == 'audit':   return tktStringAudit(tkt, **kwargs)
    elif type == 'base':    return tktStringBase(tkt, **kwargs)
    elif type == 'debug':   return tktStringDebug(tkt, **kwargs)
    elif type == 'short':   return tktStringShort(tkt, **kwargs)
    elif type == 'worklog': return tktStringWorklog(tkt, **kwargs)
    else: 
        raise Exception('unknown string type: %s' % type)

def tktIsResolved(tkt): return typeSwitch(tkt, 'tktIsResolved')

def tktStringAssignee(tkt):    return typeSwitch(tkt, 'tktStringAssignee')
def tktStringAudit(tkt):       return typeSwitch(tkt, 'tktStringAudit')
def tktStringBase(tkt):        return typeSwitch(tkt, 'tktStringBase')
def tktStringDebug(tkt):       return typeSwitch(tkt, 'tktStringDebug')
def tktStringDescription(tkt): return typeSwitch(tkt, 'tktStringDescription')
def tktStringJournal(tkt):     return typeSwitch(tkt, 'tktStringJournal')
def tktStringPrimary(tkt):     return typeSwitch(tkt, 'tktStringPrimary')
def tktStringRequestor(tkt):   return typeSwitch(tkt, 'tktStringRequestor')
def tktStringResolution(tkt):  return typeSwitch(tkt, 'tktStringResolution')
def tktStringShort(tkt):       return typeSwitch(tkt, 'tktStringShort')
def tktStringSummary(tkt):     return typeSwitch(tkt, 'tktStringSummary')


#########################################################################
### ServiceNow Searching ################################################
#########################################################################

def groupById(id):
    """
    Pull a sys_user_group entry by sys_id.  Goes through cacheQueryOne, so
    future calls are cached.
    """
    return cacheQueryOne('sys_user_group', query={ 'sys_id': id })

def incidentByNumber(number):
    """
    """
    i = snow.query(table='incident', query={'number': number})
    inc = i.get_one()
    return inc 

def ritmByNumber(number):
    """
    """
    r = snow.query(table='sc_req_item', query={'number': number})
    ritm = r.get_one()
    return ritm

def groupByName(name):
    """
    """
    return cacheQueryOne('sys_user_group', query={ 'name': name })

def userById(id):
    """
    Queries and returns a single sys_user entry based on a user sys_id.
    """
    return cacheQueryOne('sys_user', query={ 'sys_id': id })

def userInGroups(username):
    """
    """
    me = userByUsername(username)
    ret = []
    q = snow.query(table='sys_user_grmember', query={ 'user': me['sys_id'] })
    for g in q.get_all():
        id = g['group']['value']
        group = groupById(id)
        ret.append(group['name'])
    return ret

def userByName(name):
    """
    """
    return cacheQueryOne('sys_user', query={ 'name': name })

def userByUsername(name):
    """
    """
    return cacheQueryOne('sys_user', query={ 'user_name': name })

def tktSearch(table, **args):
    """
    """

    try:
        search = tableSwitch(table, 'tktFilter', **args)
        q = snow.query(table=table, query=str(search))
        return q.get_all()
    except UnexpectedResponse, e:
        print "%s" % e

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
