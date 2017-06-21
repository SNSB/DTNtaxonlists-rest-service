# TaxonName-Database specific functions

from flask import current_app
from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase
from sqlalchemy import text 

DWB_MODULE='DiversityReferences'

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

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
    reflist=[]
    if not cleanDatabasename(database):
        return [] 
    database = diversitydatabase(database)
    query = u''' select '%s' as DatabaseName, RefID, RefType, RefDescription_Cache, Title, DateYear, \
                 DateMonth, DateDay, DateSuppl, SourceTitle, SeriesTitle, Periodical, Volume, Issue, Pages, Publisher, \
                 PublPlace, Edition, ISSN_ISBN, Miscellaneous1, Miscellaneous2, Miscellaneous3, Weblinks, LinkToPDF, UserDef1, UserDef2, UserDef3, ParentRefID, \
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
    reflist=[]
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

def getReferenceChilds(database, refid):
    reflist=[]
    if not cleanDatabasename(database):
        return []    
    database = diversitydatabase(database)
    query = text(''' select '%s' as DatabaseName, RefID, ParentRefID \
                 from [%s].[dbo].[ReferenceTitle] \
                 where ParentRefID = :rpid ''' % (database, database))
    current_app.logger.debug("Query %s with rpid=%s' " % (query, refid))
    with get_db().connect() as conn:
        treflist = conn.execute(query, rpid=refid)
        if treflist != None:
            reflist=R2L(treflist)
    return reflist

def getReferenceChildsAll(database, refid):
    reflist=[]
    if not cleanDatabasename(database):
        return []    
    database = diversitydatabase(database)

    query = text('''with hierachy as (
                   select '%s' as DatabaseName, RefID as baseRefID, RefID, ParentRefID, 0 as level 
                   from [%s].[dbo].[ReferenceTitle]
                   where RefID= :rpid
                 union all
                 select '%s' as DatabaseName, child.baseRefID, crefid.RefID, crefid.ParentRefID, child.level -1 as level
                   from hierachy as child
                     inner join [%s].[dbo].[ReferenceTitle] as crefid
                       on child.RefID = crefid.ParentRefID 
                )
                select a.*
                    from hierachy a 
                order by baseRefID, level desc;'''  % (database, database, database, database))
    current_app.logger.debug("Query %s with rpid=%s' " % (query, refid))
    with get_db().connect() as conn:
        treflist = conn.execute(query, rpid=refid)
        if treflist != None:
            reflist=R2L(treflist)
    return reflist

##########################
# Subitems

def getReferenceRelation(database, refid, role, sequence):
    reflist=[]
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
    if isInt(id):
        query = u'''select [%s].[dbo].BaseURL() + cast(%s as nvarchar) as ReferenceURI;''' % (database, id)
        current_app.logger.debug("Query %s " % (query))
        with get_db().connect() as conn:
            treflist = conn.execute(query)
            if treflist != None:
                reflist=treflist.fetchone()
                return reflist['ReferenceURI']
    return []

def queryReferenceLinksNames(database, id):
    
    return None
    
