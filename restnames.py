import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import sqlalchemy
import string

#import config.py

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASESERVER='''mssql+pymssql://TNT:***REMOVED***@tnt.diversityworkbench.de:5432''',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def create_tnt_engine():
    engine = sqlalchemy.create_engine(app.config['DATABASESERVER'])
    return engine

def connect_tnt_db():
    """Connects to the specific database."""
    conn = g.tnt_engine.connect()
    return conn

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'tnt-engine'):
        g.tnt_engine =  create_tnt_engine()
    if not hasattr(g, 'tnt-db'):
        g.tnt_db = connect_tnt_db()
    return g.tnt_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'tnt-db'):
        g.tnt_db.close()
    if hasattr(g, 'tnt-engine'):
        g.tnt_engine = None
        
def init_db():
    pass

def toDict(data):
    return dict(data.items())

def R2L(data):
    mydata = []
    for row in data:
        myrow = toDict(row)
        mydata.append(myrow)
    return mydata

def removeSQL(name):
    name = filter(lambda x: x in string.printable, name)
    name = filter(lambda x: x not in [';',"'"] , name)
    name = name.replace("--", "").replace("/*", "")
    return name

def parseDiversityWorkbenchURI(uri):
    # http://servername/dbname/projectid
    protocol, rest = uri.split('//')
    servername, dbname, projectid = rest.split('/')
    return (removeSQL(servername), removeSQL('Diversity' + dbname), int(projectid))

def genDiversityWorkbenchURI(server, dbname, projectid):
    dbname = dbname[len('Diversity'):]
    rest = '/'.join(['http:/', server, dbname, str(projectid)])
    return rest

def genRestLink(uri):
    return '/'.join(map(lambda x: str(x), parseDiversityWorkbenchURI(uri)))

def getTaxonomicDBs():
    taxonDBlist = []
    alldbs = []
    with get_db() as conn:
        result = conn.execute('''select name from master.dbo.sysdatabases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb');''')
        for row in result:
            alldbs.append(row['name'])
    for dbname in alldbs:
        try:
            with get_db() as conn:
                query = '''SELECT [%s].[dbo].[DiversityWorkbenchModule]() as name;''' % dbname
                # print(query)
                modulename = conn.execute(query).fetchone()['name']
                if modulename == 'DiversityTaxonNames':
                    taxonDBlist.append(dbname)
        except Exception as e:
            pass
            #print('Exception in %s.' % dbname)
            #print(e)
    return (taxonDBlist)

def getProjectInfo(uri):
    servername, dbname, projectid = parseDiversityWorkbenchURI(uri)
    # TODO: Parse if servername contains port!
    engine = sqlalchemy.create_engine('mssql+pymssql://TNT:***REMOVED***@%s:5432' % servername)
    try:
        with engine.connect() as conn:
            query = ('select Project, ProjectTitle, ProjectDescription, ProjectEditors, ProjectInstitution, ProjectNotes, '
                            'ProjectCopyright, ProjectURL '
                            'from [%s].[dbo].[Project] '
                            "where ProjectID = '%s'") % (dbname, int(projectid))
            projectInfoRaw = conn.execute(query).fetchone()
            projectInfo = dict(zip(projectInfoRaw.keys(),projectInfoRaw.values()))
            projectInfo['URI'] = uri
            return projectInfo
    except Exception as e:
        print('At project-uri: %s:' % uri)
        print(e)
        
        return {'URI':uri} #'No connection to server %s for uri %s' % (servername, uri)

@app.route('/')
def getAvailableLists():
    # get all project URI
    urilist = []
    listDBs = getTaxonomicDBs()
    for dbname in listDBs:
        query = 'select distinct ProjectID, ProjectURI from [%s].[dbo].[TaxonNameListProjectProxy]' % dbname
        with get_db() as conn:
            projectURI = conn.execute(query)
            if projectURI != None:
                for uri in projectURI:
                    if uri['ProjectURI'] != None:
                        urilist.append({'dbname':dbname, 'ProjectID':uri['ProjectID'], 'uri':uri['ProjectURI']})
    listinfo = []
    for listitem in urilist:
        #print(uri['uri'])
        #print(getProjectInfo(uri['uri']))
        info = getProjectInfo(listitem['uri'])
        #print(info)
        if len(info.keys())<3:
            continue
        uriinfo = toDict(info)
        server,dbname,listid = parseDiversityWorkbenchURI(listitem['uri'])
        uriinfo['linkurl'] = '%s/%s/%s' % (server,dbname,listid) 
        #print(uriinfo)
        listinfo.append(uriinfo)
    return render_template('show_lists.html', listinfo=listinfo)

def getAvailableLists_py():
    # get all project URI
    urilist = []
    listDBs = getTaxonomicDBs()
    for dbname in listDBs:
        query = 'select distinct ProjectURI from [%s].[dbo].[TaxonNameListProjectProxy]' % dbname
        with get_db() as conn:
            projectURI = conn.execute(query)
            if projectURI != None:
                for uri in projectURI:
                    if uri['ProjectURI'] != None:
                        urilist.append((dbname, uri['ProjectURI']))
    return urilist


@app.route('/lists/<string:project_server>/<string:project_db>/<int:listnumber>')
def show_list_info(project_server, project_db, listnumber):
    project_server = removeSQL(project_server)
    project_db = removeSQL(project_db)
    listnumber = int(listnumber)  
    dblist = getAvailableLists_py()
    uri = genDiversityWorkbenchURI(project_server, project_db, listnumber)
    #print(dblist)
    databases = filter(lambda a:a[1]==uri, dblist)
    print databases
    listdatabases = []
    for databaseitem in databases:
        database = databaseitem[0]
        query = ('''select count(*) as anz from [%s].[dbo].[TaxonNameList] a where '''
                   '  a.ProjectId=%s') % (database, listnumber)
        print query
        with get_db() as conn:   
            countlist = conn.execute(query)   
            for count in countlist:
                mycount = toDict(count)
                mycount['database'] = databaseitem[0]
                listdatabases.append(mycount)
    return render_template('show_list_info.html', databases=listdatabases)
        

    
@app.route('/lists/<string:project_server>/<string:project_db>/<int:listnumber>/')
def show_list(project_server, project_db, listnumber):
    project_server = removeSQL(project_server)
    project_db = removeSQL(project_db)
    listnumber = int(listnumber)
    
    dblist = getAvailableLists_py()
    uri = genDiversityWorkbenchURI(project_server, project_db, listnumber)
    #print(dblist)
    databases = filter(lambda a:a[1]==uri, dblist)
    taxonnames = []
    for databaseitem in databases:
        database = databaseitem[0]
        query = ('''select TaxonNameCache, TaxonomicRank, a.NameID, [%s].[dbo].[BaseURL]()  as BaseURI '''
                   'from [%s].[dbo].[TaxonNameList] a left join [%s].[dbo].[TaxonName] b '
                   '  on a.NameID = b.NameID where ProjectId=%s') % (database, database, database, listnumber)
        with get_db() as conn:   
            namelist = conn.execute(query)   
            for taxname in namelist:
                mytaxonname = toDict(taxname)
                baseuri = mytaxonname['BaseURI']
                # print(baseuri)
                baseuri = baseuri[len('http://'):] # skip http://
                baseserver, basedb, emphty = baseuri.split('/') 
                basedb = 'Diversity%s' % basedb 
                mytaxonname['BaseURI'] = '%s/%s/' % (baseserver,basedb)
                mytaxonname['BaseServer'] = baseserver
                mytaxonname['BaseDB'] = basedb
                taxonnames.append(mytaxonname)
    return render_template('show_taxonnames.html', taxonnamelist=taxonnames)

def getTaxonnameHierarchy(server,dbname,projectid, nameid):
    query = ('''with hierachy as (
                   select NameID as baseNameID, NameID, NameParentID, 0 as level, ProjectID 
                   from [%s].dbo.TaxonHierarchy
                   where NameID=%s and IgnoreButKeepForReference = 0
                 union all
                 select child.baseNameID, name.NameID, name.NameParentID, child.level +1 as level, child.ProjectID
                   from hierachy as child
                     inner join %s.dbo.TaxonHierarchy as name
                       on child.NameParentID = name.NameID and child.ProjectID = name.ProjectID
                   where name.IgnoreButKeepForReference = 0
                )
                select a.*, n.TaxonNameCache, n.TaxonomicRank 
                    from hierachy a 
                        left join %s.dbo.TaxonName n 
                        on a.NameID=n.nameID 
                order by baseNameID, level;''')  % (dbname, nameid, dbname, dbname)

    if not server == 'tnt.diversityworkbench.de':
        namelist = []
        return namelist
    with get_db() as conn:
        namelist = conn.execute(query).fetchall()
        return R2L(namelist)

def getTaxonNameInfo(taxonnameserver, taxondatabase, nameid):
    query = (''' select * ''' # NameID, TaxonNameCache, Version, TaxonomicRank, ReferenceTitle, ReferenceURI, RevisionLevel '''
            ''' from [%s].[dbo].[TaxonName] '''
            ''' where NameID = %s and IgnoreButKeepForReference = 0; ''') % (taxondatabase, nameid)
    if not taxonnameserver == 'tnt.diversityworkbench.de':
        return []
    with get_db() as conn:
        nameinfo = conn.execute(query)
        return R2L(nameinfo)
    
def getTaxonNameLog(taxonnameserver, taxondatabase, nameid):
    query = (''' select * ''' # NameID, TaxonNameCache, Version, TaxonomicRank, ReferenceTitle, ReferenceURI, RevisionLevel '''
            ''' from [%s].[dbo].[TaxonName_log] '''
            ''' where NameID = %s ''') % (taxondatabase, nameid)
    if not taxonnameserver == 'tnt.diversityworkbench.de':
        return []
    with get_db() as conn:
        nameinfo = conn.execute(query)
        return R2L(nameinfo)
     

def getHierarchyProjects(taxonnameserver, taxondatabase, nameid):
    query = (''' select distinct a.ProjectID, b.ProjectURI from [%s].[dbo].[TaxonHierarchy] a '''
             ''' inner join [%s].[dbo].[ProjectProxy] b '''
             ''' on a.ProjectID = b.ProjectID '''
             ''' where NameID = %s and IgnoreButKeepForReference = 0 ''') % (taxondatabase, taxondatabase, nameid)
    if not taxonnameserver == 'tnt.diversityworkbench.de':
        return []
    with get_db() as conn:
        projectids = conn.execute(query)
        myprojectids = R2L(projectids)
        for row in myprojectids:
            row['projectlink']=genRestLink(row['ProjectURI'])
        return myprojectids

def getAcceptedNamesProjects(taxonnameserver, taxondatabase, nameid):
    query = (''' select distinct a.ProjectID, b.ProjectURI from [%s].[dbo].[TaxonAcceptedName] a ''' 
             ''' inner join [%s].[dbo].[ProjectProxy] b '''
             ''' on a.ProjectID = b.ProjectID '''
             ''' where a.NameID = %s and a.IgnoreButKeepForReference = 0 ''') % (taxondatabase, taxondatabase, nameid)
    if not taxonnameserver == 'tnt.diversityworkbench.de':
        return []
    with get_db() as conn:
        projectids = conn.execute(query)
        return R2L(projectids)

def getAcceptedNames(taxonnameserver, taxondatabase, projectid, nameid):
    query = (''' select * ''' #ProjectID, NameID, ConceptSuffix, ConceptNotes, RefURI, RefText, RefDetail, TypistsNotes '''
             ''' from [%s].[dbo].[TaxonAcceptedName] '''
             ''' where NameID = %s and IgnoreButKeepForReference = 0 ''') % (taxondatabase, nameid)
    if not taxonnameserver == 'tnt.diversityworkbench.de':
        return []
    with get_db() as conn:
        names = conn.execute(query)
        myNames = R2L(names)
  #     for row in myNames:
  #          row['projectlink']=genRestLink(row['ProjectURI'])
        return myNames
    
def getCommonNames(taxonnameserver, taxondatabase, nameid):
    query = (''' select NameID, CommonName, LanguageCode, CountryCode, ReferenceTitle, ReferenceURI, ReferenceDetails, SubjectContext, Notes '''
             ''' from [%s].[dbo].[TaxonCommonName] '''
             ''' where NameID = %s ''') % (taxondatabase, nameid)
    if not taxonnameserver == 'tnt.diversityworkbench.de':
        return []
    with get_db() as conn:
        names = conn.execute(query)
        return R2L(names)
    
def getNameLists(taxonnameserver, taxondatabase, nameid):
    query = (''' select a.NameID, a.ProjectID, a.Notes, b.ProjectURI '''
             ''' from [%s].[dbo].[TaxonNameList] a '''
             ''' inner join [%s].[dbo].[TaxonNameListProjectProxy] b '''
             ''' on a.ProjectID = b.ProjectID '''
             ''' where NameID = %s ''') % (taxondatabase, taxondatabase, nameid)
    if not taxonnameserver == 'tnt.diversityworkbench.de':
        return []
    with get_db() as conn:
        names = conn.execute(query)
        myNames = R2L(names)
        for row in myNames:
            row['projectlink']=genRestLink(row['ProjectURI'])
        return myNames

def getProjectInfoDirect(projectserver, database, projectid):
    query = (''' select ProjectID, ProjectParentID, Project, ProjectTitle, ProjectDescription, ProjectEditors, ProjectInstitution, '''
             '''        ProjectNotes, ProjectCopyright, ProjectVersion, ProjectURL, ProjectSettings '''
             ''' from [%s].[dbo].[Project] '''
             ''' where ProjectID = %s ''') % (database, projectid)
    if not projectserver == 'tnt.diversityworkbench.de':
        return []
    with get_db() as conn:
        names = conn.execute(query)
        myNames = R2L(names)
        for row in myNames:
            row['projectlink']='/'.join([projectserver,database,str(projectid)])
        return myNames

@app.route('/projects/<string:projectserver>/<string:databasename>/<int:projectid>')
def getTaxonProjectInfo(projectserver, databasename, projectid):
    projectserver = removeSQL(projectserver)
    databasename = removeSQL(databasename)
    projectid = int(projectid)
    
    info = getProjectInfoDirect(projectserver, databasename, projectid)
    #for i in info:
    #    print '%s' % (i)
    return render_template('project_info.html', projectinfo=info)

@app.route('/names/<string:taxonnameserver>/<string:taxondatabase>/<int:nameid>')
def getTaxonName(taxonnameserver, taxondatabase, nameid):
    taxonnameserver = removeSQL(taxonnameserver)
    taxondatabase = removeSQL(taxondatabase)
    nameid = int(nameid)
    
    #taxondatabase = taxondatabase[len('Diversity'):]
    nameinfo = getTaxonNameInfo(taxonnameserver, taxondatabase, nameid)
    # print nameinfo
    hierarchyProjectIds = getHierarchyProjects(taxonnameserver, taxondatabase, nameid)
    #print ('HPID: %s' % hierarchyProjectIds)
    namehierarchies = []
    for projectid in hierarchyProjectIds:
       namehierarchy = getTaxonnameHierarchy(taxonnameserver, taxondatabase, projectid['ProjectID'], nameid)
       localHierarchy = []
       for row in namehierarchy:
          myrow = toDict(row)
          myrow['ProjectURI'] = projectid['ProjectURI']
          myrow['projectlink'] = genRestLink(myrow['ProjectURI'])
          localHierarchy.append(myrow)
       namehierarchies.append(localHierarchy)

    acceptedNamesProjectIds = getAcceptedNamesProjects(taxonnameserver, taxondatabase, nameid)
    acceptedNames = []
    for projectid in acceptedNamesProjectIds:
        acceptedname = getAcceptedNames(taxonnameserver, taxondatabase, projectid['ProjectID'], nameid)
        for row in acceptedname:
            row['ProjectURI'] = projectid['ProjectURI']
            row['projectlink'] = genRestLink(row['ProjectURI'])
            acceptedNames.append(row)

    commonNames = getCommonNames(taxonnameserver, taxondatabase, nameid)

    namelists = getNameLists(taxonnameserver, taxondatabase, nameid)
    if False:
        for name in nameinfo:
            print('name: %s' % name)
        for nlist in namelists:
            print('list: %s' % nlist)
        for aname in acceptedNames:
            print ('aname: %s' % aname)
        for hname in namehierarchies:
            print ('hname: %s' % hname)     

    requestpath = request.path;
    requestpath = requestpath[:requestpath.rfind('/%s' % nameid)]
                                                 
    return render_template('nameinfo.html', 
                           nameinfo=nameinfo, 
                           namehierarchies=namehierarchies, 
                           acceptedNames=acceptedNames, 
                           commonNames=commonNames,  
                           namelists=namelists,
                           requestpath=requestpath)

@app.route('/names/<string:taxonnameserver>/<string:taxondatabase>/<int:nameid>/history')
def gethistory(taxonnameserver, taxondatabase, nameid):
    taxonnameserver = removeSQL(taxonnameserver)
    taxondatabase = removeSQL(taxondatabase)
    nameid = int(nameid)
    namelog = getTaxonNameLog(taxonnameserver, taxondatabase, nameid)
    return render_template('name_history.html',
                           namelog=namelog)


def historydiff(base,logs):
    # logs in correct order?
    # apply in reverse order on base.
    # select only changed items
    return 0 
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

#synonyme!

if __name__ == '__main__':
    app.run(host='0.0.0.0')
