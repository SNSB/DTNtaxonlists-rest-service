# database management
from flask import current_app,g
import sqlalchemy
import re

DWB_MODULES=['DiversityTaxonNames', 'DiversityAgents', 'DiversityProjects', 'DiversityReferences']

def get_db(host=None, port=None, user=None, password=None):
    # Opens a database engine to the given host on the given port 
    if (host is None):
        host=current_app.config['DEFAULTDBSERVER']
    if (port is None):
        port=current_app.config['DEFAULTDBPORT']
    if (user is None):
        user=current_app.config['DEFAULTDBUSER']
    if (password is None):
        password=current_app.config['DEFAULTDBPASSWORD']

    server='''{host}:{port}'''.format(host=host, port=port)
    if not hasattr(g, 'serverlist'):
        serverlist = getattr(g, 'serverlist', dict())       
        if serverlist.get(server) is None:
            t = dict()
            userpass='''{user}:{password}'''.format(user=user, password=password)
            connectstring='''mssql+pymssql://{userpass}@{server}/charset=utf8'''.format(userpass=userpass, server=server)
            current_app.logger.debug("Opening engine to %s" % connectstring)
            t['server']=server
            t['userpass']=userpass
            t['engine']=sqlalchemy.create_engine(connectstring)
            serverlist[server]=t
            setattr(g,'serverlist', serverlist)
    engine = getattr(g, 'serverlist').get(server).get('engine')
    return engine

# check if dab is already open, if not one can be asked abeout a user-password-combination first
def is_db_open(host=None, port=None):
    if (host is None):
        host=current_app.config['DEFAULTDBSERVER']
    if (port is None):
        port=current_app.config['DEFAULTDBPORT']
        
    server='''{host}:{port}'''.format(host=host, user=user)
    return hasattr(g, 'DBSERVER_'+server)

# get all databasenames which are DWB-modules and have the given moduletype
def getDBs(moduleType): 
    DBlist = []
    alldbs = []
    if not moduleType in DWB_MODULES:
        return DBlist
    with get_db().connect() as conn:
        result = conn.execute('''select name from master.dbo.sysdatabases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb');''')
        for row in result:
            alldbs.append(row['name'])
    #current_app.logger.debug(alldbs)
    for dbname in alldbs:
        try:
            with get_db().connect() as conn:
                query = '''SELECT [%s].[dbo].[DiversityWorkbenchModule]() as name;''' % dbname
                modulename = conn.execute(query).fetchone()['name']
                current_app.logger.debug("Query %s delivers %s" % (query, modulename))
                if modulename == moduleType:
                    DBlist.append(dbname)
        except Exception as e:
            current_app.logger.debug('Exception in %s.' % dbname)
            current_app.logger.debug(e)
            pass
    return (DBlist)    

def cleanDatabasename(name):
    return re.match("[A-Za-z0-9_-]*$",name)

