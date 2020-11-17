"""
pyfnalsnow - a python module to interact with the JSON API of the FNAL
Service Now (SNOW) instance.
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
    'sc_request':  'pyfnalsnow.Request',
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
import pyfnalsnow.Incident, pyfnalsnow.Request, pyfnalsnow.RITM

import urllib3
urllib3.disable_warnings()

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


def pyfnalsnow_config(file=config_file):
    """
    Load a yaml configuration from a configuration file.  Sets a global
    'config' variable.
    """
    global config

    try:
        config = yaml.load(open(file, 'r'))
    except IOError as e:
        print("file error:  %s" % e)
        sys.exit(2)
    except Exception as e:
        print("unknown error:  %s" % e)
        sys.exit(2)

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
        host=config['servicenow']['hostname'],
        user=config['servicenow']['username'],
        password=config['servicenow']['password']
    )

    return snow

#########################################################################
### pyfnalsnow wrappers #################################################
#########################################################################

def cacheQueryOne(table, query):
    """
    Do a SNOW database query and cache the result for later.  Uses
    'get_one()' so we only get a single result.  Especially useful for
    user and group lookups, which change rarely and need to be queried
    several times.
    """
    if table not in cache: cache[table] = {}

    q = str(query)

    if q in cache[table]:
        return cache[table][q]
    else:
        try:
            r = snow.resource(api_path='/table/%s' % table).get(
                query=query,
                stream=True
            )
            entries = []
            for record in r.all():
                entries.append(record)
            if len(entries) == 0:
                raise Exception('no matching entries (%s vs %s)'
                    % (query, table))
            elif len(entries) > 1:
                raise Exception('too many entries (%s) (%s vs %s)'
                     % (len(entries), query, table))
            result = entries[0]
        except Exception as e:  # noqa: F841
            result = None
        cache[table][q] = result
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

def typeSwitch(tkt, function, **kwargs):
    """
    Black Magic Ahoy!  Given a function name and a ticket, invokes that
    function *from the matching class*.
    """
    try:    number = tkt['number']
    except: raise Exception('no ticket number in ticket')
    type = tktType(number)

    if type in modules:
        return eval("%s.%s" % (modules[type], function))(tkt, **kwargs)
    else:
        raise Exception('unsupported type: %s' % type)

#########################################################################
### Reporting Functions #################################################
#########################################################################


def tktString(tkt, type='base', *args, **kwargs):
    """
    Create a string summarizing ticket data, and return as an array.
    """

    if type == 'audit': return tktStringBaseAudit(tkt, **kwargs)
    elif type == 'base': return tktStringBase(tkt, **kwargs)
    elif type == 'debug': return tktStringDebug(tkt, **kwargs)
    elif type == 'short': return tktStringShort(tkt, **kwargs)
    elif type == 'worklog': return tktStringWorklog(tkt, **kwargs)
    else:
        raise Exception('unknown string type: %s' % type)

def tktIsResolved(tkt): return typeSwitch(tkt, 'tktIsResolved')

def tktStringAssignee(tkt): return typeSwitch(tkt, 'tktStringAssignee')
def tktStringAudit(tkt): return typeSwitch(tkt, 'tktStringAudit')
def tktStringBase(tkt): return typeSwitch(tkt, 'tktStringBase')
def tktStringBaseAudit(tkt): return typeSwitch(tkt, 'tktStringBaseAudit')
def tktStringDebug(tkt): return typeSwitch(tkt, 'tktStringDebug')
def tktStringDescription(tkt): return typeSwitch(tkt, 'tktStringDescription')
def tktStringJournal(tkt): return typeSwitch(tkt, 'tktStringJournal')
def tktStringPrimary(tkt): return typeSwitch(tkt, 'tktStringPrimary')
def tktStringRequestor(tkt): return typeSwitch(tkt, 'tktStringRequestor')
def tktStringResolution(tkt): return typeSwitch(tkt, 'tktStringResolution')
def tktStringShort(tkt): return typeSwitch(tkt, 'tktStringShort')
def tktStringSummary(tkt): return typeSwitch(tkt, 'tktStringSummary')
def tktStringWorklog(tkt): return typeSwitch(tkt, 'tktStringWorklog')

#########################################################################
### ServiceNow Searching ################################################
#########################################################################

def ciById(id):
    """
    Pull a cmdb_ci by sys_id.  Goes through cacheQueryOne(), so
    future calls are cached.
    """
    return cacheQueryOne('cmdb_ci', query={'sys_id': id})

def ciByName(name):
    """
    Pull a cmdb_ci by name.  Goes through cacheQueryOne(), so
    future calls are cached.
    """
    return cacheQueryOne('cmdb_ci', query={'name': name})

def groupById(id):
    """
    Pull a sys_user_group entry by sys_id.  Goes through cacheQueryOne(), so
    future calls are cached.
    """
    return cacheQueryOne('sys_user_group', query={'sys_id': id})

def groupByName(name):
    """
    Pull a sys_user_group entry by name.  Goes through cacheQueryOne(), so
    future calls are cached.
    """
    return cacheQueryOne('sys_user_group', query={'name': name})

def groupLink(group):
    """
    Convert a 'group' style object to a group name.  This is the data
    structure that sometimes appears in the middle of standard results.
    """
    if isinstance(group, dict):
        if 'value' in group:
            if group['value'] == '0': return '*none*'
            g = groupById(group['value'])
            return g['name']
    return group

def tktByNumber(number):
    """
    Look up a ticket number by number.  We will look up the correct table
    type based on the ticket number as well.  Returns a single object.
    """

    type = tktType(number)

    r = snow.resource(api_path='/table/%s' % type).get(
        query={'number': number},
        stream=True
    )

    entries = []
    for record in r.all():
        entries.append(record)

    if len(entries) == 0:
        raise Exception('%s: no matching entries' % number)
    elif len(entries) > 1:
        raise Exception('%s: too many entries (%s)' % number, len(entries))
    return entries[0]

def tktHistory(tkt):
    """
    Given a full ticket, query for associated sys_history_line objects.
    """

    r = snow.resource(api_path='/table/%s' % 'sys_history_line').get(
        query={'set.id': tkt['sys_id']},
        stream=True
    )
    entries = []
    for record in r.all(): entries.append(record)

    ret = []
    for i in entries:
        ret.append(i)
    return ret

def tktPending(tkt, **kwargs):
    """
    Given a full ticket, set the status of that ticket to 'Pending'.
    """
    return typeSwitch(tkt, 'tktPending', **kwargs)

def tktResolve(tkt, update, **kwargs):
    """
    Given a full ticket, close that ticket out.
    """
    return typeSwitch(tkt, 'tktResolve', update=update, **kwargs)

def tktJournalEntries(tkt):
    """
    Given a full ticket, query for journal entries.
    """

    r = snow.resource(api_path='/table/%s' % 'sys_journal_field').get(
        query={'element_id': tkt['sys_id']}, stream=True)
    entries = []
    for record in r.all(): entries.append(record)

    ret = []
    journals = {}
    for i in entries:
        if 'sys_created_on' in i:
            key = i['sys_created_on']
            journals[key] = i

    for i in sorted(journals.keys()):
        ret.append(journals[i])
    return ret

def tktSearch(table, **args):
    """
    Given a table name, search the table using tktFilter().  Returns an
    array of matching objects.
    """

    try:
        search = tableSwitch(table, 'tktFilter', **args)
        r = snow.resource(api_path='/table/%s' % table).get(query=search,
            stream=True)
    except Exception as e:
        raise Exception("search error: %s" % e)

    ret = []
    for i in r.all():
        if i: ret.append(i)
    return ret

def tktCreate(table, entry, **args):
    """
    """
    return snow.insert(table, entry, **args)

def tktUpdate(number, updateHash):
    """
    Update a ticket number by number.  We will look up the correct table
    type based on the ticket number as well.  Returns a single object.
    """
    type = tktType(number)
    r = snow.resource(api_path='/table/%s' % type).update(
        query={'number': number},
        payload=updateHash
    )

    ret = []
    for i in r.all(): ret.append(i)
    if len(ret) >= 1: return ret[0]
    return []

def userById(id):
    """
    Pull a sys_user entry by sys_id.  Goes through cacheQueryOne(), so
    future falls are cached.
    """
    return cacheQueryOne('sys_user', query={'sys_id': id})

def userByName(name):
    """
    Pull a sys_user entry by name.  Goes through cacheQueryOne(), so
    future falls are cached.
    """
    return cacheQueryOne('sys_user', query={'name': name})

def userByUsername(name):
    """
    Pull a sys_user entry by user_name.  Goes through cacheQueryOne(), so
    future falls are cached.
    """
    return cacheQueryOne('sys_user', query={'user_name': name})

def userInGroup(username, group):
    """
    Return True is the user with the offered username is in the group with
    the offered group name, False otherwise.
    """

    groups = userInGroups(username)
    for g in groups:
        if g == group: return True
    return False

def userInGroups(username):
    """
    Given a username, return a list of group names that this user is a
    member of.
    """
    me = userByUsername(username)
    ret = []
    if me:
        r = snow.resource(api_path='/table/%s' % 'sys_user_grmember').get(
            query={'user': me['sys_id']},
            stream=True
        )
        for g in r.all():
            id = g['group']['value']
            group = groupById(id)
            ret.append(group['name'])
    return ret

def userLink(user):
    """
    Convert a 'user' style object to a data structure.  This is the data
    structure that sometimes appears in the middle of standard results.
    """
    if isinstance(user, dict):
        if 'value' in user:
            if user['value'] == '0': return '*nobody*'
            u = pyfnalsnow.userById(user['value'])
            return u
    return user

def userLinkName(user):
    """
    Convert a 'user' style object to a name.  This is the data structure
    that sometimes appears in the middle of standard results.
    """
    if isinstance(user, dict):
        if 'value' in user:
            if user['value'] == '0': return '*nobody*'
            u = pyfnalsnow.userById(user['value'])
            return u['name']
    return user

def userLinkUsername(user):
    """
    Convert a 'user' style object to a user_name.  This is the data structure
    that sometimes appears in the middle of standard results.
    """
    if isinstance(user, dict):
        if 'value' in user:
            if user['value'] == '0': return '*nobody*'
            u = pyfnalsnow.userById(user['value'])
            return u['user_name']
    return user

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
        num = m.group(2)
        length = len(number)
        if type == 'INC': return 'INC%s%s' % ('0' * (15 - length), num)
        if type == 'REQ': return 'REQ%s%s' % ('0' * (15 - length), num)
        if type == 'TASK': return 'TASK%s%s' % ('0' * (11 - length), num)
        if type == 'RITM': return 'RITM%s%s' % ('0' * (11 - length), num)
        if type == 'PRJTASK': return 'PRJTASK%s%s' % ('0' * (11 - length), num)
        raise Exception('unknown ticket type: %s' % type)

    elif re.match('^(\d+)$', number):
        return "INC%s%s" % ('0' * (12 - len(number)), number)

    else:
        raise Exception('could not parse "%s"' % number)

def tktType(number):
    """
    Given a ticket number, return the matching ServiceNow table name.
    """

    num = tktNumberParse(number)
    m = re.match('^(TASK|RITM|INC|REQ|PRJTASK)(\d+)$', num, re.IGNORECASE)
    if m:
        type = m.group(1).upper()
        if type == 'INC': return 'incident'
        if type == 'PRJTASK': return 'pm_project_task'
        if type == 'REQ': return 'sc_request'
        if type == 'RITM': return 'sc_req_item'
        if type == 'TASK': return 'sc_task'

    raise Exception('unknown ticket type for %s' % number)

#########################################################################
### main () #############################################################
#########################################################################

pyfnalsnow_config(config_file)
