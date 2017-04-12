# TaxonName-Database specific functions

from flask import current_app
from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase


DWB_MODULE='DiversityReferences'

def encoded_dict(in_dict):
    return in_dict
    #out_dict = {}
    #for k, v in in_dict.iteritems():
        #if isinstance(v, unicode):
            #v = v.decode('utf8')
        #elif isinstance(v, str):
            ## Must be encoded in UTF-8
            #v.encode('utf8')
        #out_dict[k] = v
    #return out_dict

def toDict(data):
    d= dict(data.items())
    return encoded_dict(d)

def R2L(data):
    mydata = []
    for row in data:
        myrow = toDict(row)
        mydata.append(myrow)
    return mydata

def databasenameOK(databasename):
    dblists=getDBs('DiversityReferences')
    if not databasename in dblists:
        return False
    return True

###########################

def getReferences(database):
    reflist=[]
    if not cleanDatabasename(database):
        return []
    database = diversitydatabase(database)
    query = u''' select '%s' as DatabaseName, RefID
                 from [%s].[dbo].[ReferenceTitle] \
                 ''' % (database, database)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        treflist = conn.execute(query)
        if treflist != None:
            reflist=R2L(treflist)
    return reflist

def getReference(database, refid):
    agentlist=[]
    if not cleanDatabasename(database):
        return [] 
    database = diversitydatabase(database)
    query = u''' select '%s' as DatabaseName, RefID, RefType, RefDescription_Cache, Title, DateYear, \
                 DateMonth, DateDay, DateSuppl, SourceTitle, SeriesTitle, Periodical, Volume, Issue, Pages, Publisher, \
                 PublPlace, Edition, ISSN_ISBN, Miscellaneous1, Miscellaneous2, Miscellaneous3, Weblinks, LinkToPDF, UserDef1, UserDef2, UserDef3, \
                 Language, [%s].[dbo].RefAutoDescription_2(RefID) as fullref \
                 from [%s].[dbo].[ReferenceTitle] \
                 where RefID='%s' ''' % (database, database, database, refid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        treflist = conn.execute(query)
        if treflist != None:
            reflist=R2L(treflist)
    return reflist

def getReferenceRelations(database, refid):
    agentlist=[]
    if not cleanDatabasename(database):
        return []    
    database = diversitydatabase(database)
    query = u''' select '%s' as DatabaseName, RefID, Role, Sequence, Name 
                 from [%s].[dbo].[ReferenceRelator] \
                 where RefID=%s ''' % (database, database, refid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        treflist = conn.execute(query)
        if treflist != None:
            reflist=R2L(treflist)
    return reflist


##########################
# Subitems

def getReferenceRelation(database, refid, role, sequence):
    agentlist=[]
    if not cleanDatabasename(database):
        return []    
    database = diversitydatabase(database)
    query = u''' select '%s' as DatabaseName, RefID, Role, Sequence, Name 
                 from [%s].[dbo].[ReferenceRelator] \
                 where RefID=%s and role = '%s' and sequence = %s''' % (database, database, refid, role, sequence)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        treflist = conn.execute(query)
        if treflist != None:
            reflist=R2L(treflist)
    return reflist

###

def makeReferenceURI(database, id):
    query = u'''select dbo.BaseURL() & :itemid;'''
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        treflist = conn.execute(query, itemid=id)
        if treflist != None:
            reflist=R2L(treflist)
    return reflist         

def queryReferenceLinksNames(database, id):
    
    return None
    
