# TaxonName-Database specific functions

from flask import current_app
from database.management import get_db, getDBs, cleanDatabasename


DWB_MODULE='DiversityTaxonNames'
FINAL_REVISION_LEVEL = 'final revision'

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
    dblists=getDBs('DiversityTaxonNames')
    if not databasename in dblists:
        return False
    return True


# get all TaxonNameLists in this database:
def getTaxonNameLists(databasename):
    urilist = []
    if not cleanDatabasename(databasename):
        return []
    query = u'''select distinct a.ProjectID, a.ProjectURI from [%s].[dbo].[TaxonNameListProjectProxy] a \
                where a.ProjectID in (select distinct c.ProjectID  from [%s].[dbo].[TaxonName] b inner \
                join [%s].[dbo].[TaxonNameList] c on b.NameID=c.NameID \
                where (b.RevisionLevel is null or b.RevisionLevel = 'final revision') and \
                (b.IgnoreButKeepForReference is Null or b.IgnoreButKeepForReference=0) and \
                (b.DataWithholdingReason is Null or b.DataWithholdingReason='') \
                )''' % (databasename, databasename,databasename) # TODO: Revision level has to be 'final revision'
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        projectURI = conn.execute(query)
        if projectURI != None:
            for uri in projectURI:
                if uri['ProjectURI'] != None:
                    urilist.append({'projectid':uri['ProjectID'], 'projecturi':uri['ProjectURI'], 'DatabaseName': databasename})
    return urilist

# get the Project uri for the given list
def getTaxonNameListsProjectUri(databasename, id):
    urilist = []
    if not cleanDatabasename(databasename):
        return []
    query = u'select distinct ProjectURI from [%s].[dbo].[TaxonNameListProjectProxy] where ProjectID=%s' % (databasename, id)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        projectURI = conn.execute(query)
        if projectURI != None:
            for uri in projectURI:
                if uri['ProjectURI'] != None:
                    urilist.append({'projecturi':uri['ProjectURI']})
    return urilist
    
# Get ids of all names in the given list
def getAllTaxonNamesFromList(databasename, listid):
    namelist = []
    if not cleanDatabasename(databasename):
        return []
    query = u'''select distinct a.NameID, a.Notes from [%s].[dbo].[TaxonNameList] a inner join [%s].[dbo].[TaxonName] b on a.NameID=b.NameID where \
                (b.RevisionLevel is Null or b.RevisionLevel='final revision') and \
                (b.IgnoreButKeepForReference is Null or b.IgnoreButKeepForReference=0) and \
                (b.DataWithholdingReason is Null or b.DataWithholdingReason='') \
                and ProjectID=%s''' % (databasename, databasename, listid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        nameids = conn.execute(query)
        if nameids != None:
            for nameid in nameids:
                if nameid['NameID'] != None:
                    namelist.append({'nameid':nameid['NameID'], 'notes': nameid['Notes'], 'database': databasename})
    return namelist

###################


# get all taxonname in this db
def getTaxonNames(databasename):
    namelist = []
    if not cleanDatabasename(databasename):
        return []
    query = u'''select '%s' as DatabaseName, NameID from [%s].[dbo].[TaxonName] where \
                (RevisionLevel is Null or RevisionLevel='final revision') and \
                (IgnoreButKeepForReference is Null or IgnoreButKeepForReference=0) and \
                (DataWithholdingReason is Null or DataWithholdingReason='') ''' % (databasename, databasename)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        namelistproxy = conn.execute(query)
        if namelistproxy != None:
            namelist = R2L(namelistproxy)
    return namelist

def getTaxonName(databasename, nameid):
    namelist = []
    if not cleanDatabasename(databasename):
        return []
    query = u'''select '%s' as DatabaseName, NameID, TaxonNameCache,Version, TaxonomicRank, GenusOrSupragenericName, \
                 InfragenericEpithet, SpeciesEpithet, InfraspecificEpithet, BasionymAuthors, \
                CombiningAuthors, PublishingAuthors, SanctioningAuthor, NonNomenclaturalNameSuffix, IsRecombination, \
                ReferenceTitle, ReferenceURI, \
                Volume, Issue, Pages, YearOfPubl,NomenclaturalCode, NomenclaturalStatus, NomenclaturalComment, \
                AnamorphTeleomorph, TypistNotes, RevisionLevel, IgnoreButKeepForReference from [%s].[dbo].[TaxonName] where NameID=%s and \
                (RevisionLevel is Null or RevisionLevel='final revision') and \
                (IgnoreButKeepForReference is Null or IgnoreButKeepForReference=0) and \
                (DataWithholdingReason is Null or DataWithholdingReason='') ''' % (databasename, databasename, nameid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        namelistproxy = conn.execute(query)
        if namelistproxy != None:
            namelist=R2L(namelistproxy)
    return namelist                    

def getTaxonNameAllCommonNames(databasename, nameid):
    commonnamelist =[]
    if not cleanDatabasename(databasename):
        return []
    query = u'''select '%s' as DatabaseName, NameID, CommonName, LanguageCode, CountryCode, ReferenceTitle 
               from [%s].[dbo].[TaxonCommonName] where NameID = %s''' % (databasename, databasename, nameid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        cnamelist = conn.execute(query)
        if cnamelist != None:
            commonnamelist=R2L(cnamelist)
    return commonnamelist                    

def getTaxonNameAllAcceptedNames(databasename, nameid):
    acceptednamelist =[]
    if not cleanDatabasename(databasename):
        return []
    query = u'''select '%s' as DatabaseName, NameID, ProjectID, IgnoreButKeepForReference
               from [%s].[dbo].[TaxonAcceptedName] where NameID = %s and \
               (IgnoreButKeepForReference is Null or IgnoreButKeepForReference=0)
               ''' % (databasename, databasename, nameid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        cnamelist = conn.execute(query)
        if cnamelist != None:
            acceptednamelist=R2L(cnamelist)
    return acceptednamelist                    
    
#def getTaxonNameAllAcceptedNames(databasename, nameid):
    #acceptednamelist =[]
    #query = '''select '%s' as DatabaseName, NameID, ProjectID, IgnoreButKeepForReference
               #from [%s].[dbo].[TaxonAcceptedName] where NameID = %s''' % (databasename, databasename, nameid)
    #current_app.logger.debug("Query %s " % (query))
    #with get_db().connect() as conn:
        #acnamelist = conn.execute(query)
        #if acnamelist != None:
            #acceptednamelist=R2L(acnamelist)
    #return acceptednamelist                    
     
def getTaxonNameAllSynonyms(databasename, nameid):
    synonmylist =[]
    if not cleanDatabasename(databasename):
        return []
    query = u'''select '%s' as DatabaseName, NameID, ProjectID, SynNameID, IgnoreButKeepForReference
               from [%s].[dbo].[TaxonSynonymy] where NameID = %s and \
               (IgnoreButKeepForReference is Null or IgnoreButKeepForReference=0) \
               ''' % (databasename, databasename, nameid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        snamelist = conn.execute(query)
        if snamelist != None:
            synonmylist=R2L(snamelist)
    return synonmylist  

def getTaxonNameAllHierarchies(databasename, nameid):
    hierarchylist =[]
    if not cleanDatabasename(databasename):
        return []
    query = u'''select '%s' as DatabaseName, NameID, ProjectID, IgnoreButKeepForReference
               from [%s].[dbo].[TaxonHierarchy] where NameID = %s and \
               (IgnoreButKeepForReference is Null or IgnoreButKeepForReference=0) \
               ''' % (databasename, databasename, nameid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        snamelist = conn.execute(query)
        if snamelist != None:
            hierarchylist=R2L(snamelist)
    return hierarchylist  
    
################################

def getCommonName(database, nameid, commonname, languagecode, countrycode, referencetitle):
    cnamelist=[]
    if not cleanDatabasename(database):
        return []
    query = u''' select NameID, CommonName, LanguageCode, CountryCode, ReferenceTitle, ReferenceURI, \
                ReferenceDetails, SubjectContext, Notes \
                from [%s].[dbo].[TaxonCommonName] where NameID=%s and CommonName='%s'and LanguageCode='%s' \
                and CountryCode = '%s' and ReferenceTitle = '%s' ''' % (database, nameid, commonname, languagecode, countrycode, referencetitle)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tcnamelist = conn.execute(query)
        if tcnamelist != None:
            cnamelist=R2L(tcnamelist)
    return cnamelist

###############################

def getAcceptedName(database, projectid, nameid, ignorebutkeepforreferences):
    anamelist=[]
    if not cleanDatabasename(database):
        return []
    query = u''' select NameID, ProjectID, IgnoreButKeepForReference, ConceptSuffix, ConceptNotes, RefURI, RefText, RefDetail, TypistsNotes  \
                from [%s].[dbo].[TaxonAcceptedName] where NameID=%s and ProjectID='%s'and IgnoreButKeepForReference='%s' \
                 ''' % (database, nameid, projectid, ignorebutkeepforreferences)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tanamelist = conn.execute(query)
        if tanamelist != None:
            anamelist=R2L(tanamelist)
    return anamelist

##############################

def getSynonymy(database, projectid, nameid, synnameid, ignorebutkeepforreferences):
    anamelist=[]
    if not cleanDatabasename(database):
        return []
    query = u''' select '%s' as DatabaseName, NameID, ProjectID, SynNameID, IgnoreButKeepForReference, ConceptSuffix, ConceptNotes, SynRefURI, SynRefText, SynRefDetail, SynTypistsNotes,  \
                 SynType, SynIsUncertain
                from [%s].[dbo].[TaxonSynonymy] where NameID=%s and ProjectID='%s' and SynNameID='%s' and IgnoreButKeepForReference='%s' \
                 ''' % (database, database, nameid, projectid, synnameid, ignorebutkeepforreferences)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tanamelist = conn.execute(query)
        if tanamelist != None:
            anamelist=R2L(tanamelist)
    return anamelist

#############################

def getTaxonHierarchy(database, projectid,  nameid, ignorebutkeepforreferences):
    anamelist=[]
    if not cleanDatabasename(database):
        return []
    query = u''' select '%s' as DatabaseName, NameID, ProjectID, IgnoreButKeepForReference, NameParentID, HierarchyRefURI, HierarchyRefText, HierarchyRefDetail, \
                 HierarchyPositionIsUncertain, HierarchyTypistsNotes, HierarchyListCache \
                 from [%s].[dbo].[TaxonHierarchy] where NameID=%s and ProjectID='%s' and IgnoreButKeepForReference='%s' \
                 ''' % (database, database, nameid, projectid, ignorebutkeepforreferences)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tanamelist = conn.execute(query)
        if tanamelist != None:
            anamelist=R2L(tanamelist)
    return anamelist

