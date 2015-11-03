# TaxonName-Database specific functions

from flask import current_app
from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase


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

# also change in the search.py 701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154

# get all TaxonNameLists in this database:
def getTaxonNameLists(databasename):
    urilist = []
    if not cleanDatabasename(databasename):
        return []
    databasename=diversitydatabase(databasename)
    query = u'''select distinct a.ProjectID, a.ProjectURI from [%s].[dbo].[TaxonNameListProjectProxy] a \
                where a.ProjectID in (select distinct c.ProjectID  from [%s].[dbo].[TaxonName] b inner \
                join [%s].[dbo].[TaxonNameList] c on b.NameID=c.NameID \
                where (b.RevisionLevel is null or b.RevisionLevel = 'final revision') and \
                (b.IgnoreButKeepForReference is Null or b.IgnoreButKeepForReference=0) and \
                (b.DataWithholdingReason is Null or b.DataWithholdingReason='')) and \
                a.ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154) \
                ''' % (databasename, databasename,databasename) # TODO: Revision level has to be 'final revision'
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
    databasename=diversitydatabase(databasename)
    query = u'select distinct ProjectURI from [%s].[dbo].[TaxonNameListProjectProxy] where ProjectID=%s and ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154)' % (databasename, id)
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
    databasename=diversitydatabase(databasename)
    query = u'''select distinct a.NameID, a.Notes from [%s].[dbo].[TaxonNameList] a inner join [%s].[dbo].[TaxonName] b on a.NameID=b.NameID where \
                (b.RevisionLevel is Null or b.RevisionLevel='final revision') and \
                (b.IgnoreButKeepForReference is Null or b.IgnoreButKeepForReference=0) and \
                (b.DataWithholdingReason is Null or b.DataWithholdingReason='') \
                and ProjectID=%s and \
                ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154)''' % (databasename, databasename, listid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        nameids = conn.execute(query)
        if nameids != None:
            for nameid in nameids:
                if nameid['NameID'] != None:
                    namelist.append({'nameid':nameid['NameID'], 'notes': nameid['Notes'], 'database': databasename})
    return namelist

##########################################################

# Get all names of a list including the first accepted name and the first common name 
def getAllTaxonNamesFromListFlat(databasename, listid):
    namelist = []
    if not cleanDatabasename(databasename):
        return []
    databasename=diversitydatabase(databasename)
    query = u'''select '%s' as DatabaseName, a.NameID, a.TaxonNameCache, a.Version, a.TaxonomicRank as TaxonomicRankCode, c.DisplayText as TaxonomicRank, a.GenusOrSupragenericName, \
                a.InfragenericEpithet, a.SpeciesEpithet, a.InfraspecificEpithet, a.BasionymAuthors, \
                a.CombiningAuthors, a.PublishingAuthors, a.SanctioningAuthor, a.NonNomenclaturalNameSuffix, a.IsRecombination, \
                a.ReferenceTitle, a.ReferenceURI, \
                a.Volume, a.Issue, a.Pages, a.YearOfPubl, a.NomenclaturalCode, a.NomenclaturalStatus, a.NomenclaturalComment, \
                a.AnamorphTeleomorph, a.TypistNotes, a.RevisionLevel, a.IgnoreButKeepForReference, b.ProjectID, \
                (case when an.IgnoreButKeepForReference is null or an.IgnoreButKeepForReference = 0 then an.ProjectID else null end) as AcceptedNameProject, \
                (case when sy.IgnoreButKeepForReference is null or sy.IgnoreButKeepForReference = 0 then sy.ProjectID else null end) as SynonymieProject, \
                (case when sy.IgnoreButKeepForReference is null or sy.IgnoreButKeepForReference = 0 then sy.SynNameID else null end) as SynonymieNameID, \
                (case when sy.IgnoreButKeepForReference is null or sy.IgnoreButKeepForReference = 0 then sy.SynType else null end) as SynType, \
                (case when hi.IgnoreButKeepForReference is null or hi.IgnoreButKeepForReference = 0 then hi.NameParentID else null end) as HierarchieNameParentID, \
                (case when hi.IgnoreButKeepForReference is null or hi.IgnoreButKeepForReference = 0 then hi.ProjectID else null end) as HierarchieProject \
                from [%s].[dbo].[TaxonName] a inner join [%s].[dbo].[TaxonNameList] b on  \
                a.NameID=b.NameID left join [%s].[dbo].[TaxonNameTaxonomicRank_Enum] c on a.TaxonomicRank=c.Code left join \
                [%s].[dbo].[TaxonAcceptedName] an on an.NameID = a.NameID  left join \
                [%s].[dbo].[TaxonHierarchy] hi on hi.NameID = a.NameID left join \
                [%s].[dbo].[TaxonSynonymy] sy on sy.NameID = a.NameID \
                where b.ProjectID=%s and \
                (a.RevisionLevel is Null or a.RevisionLevel='final revision') and \
                (a.IgnoreButKeepForReference is Null or a.IgnoreButKeepForReference=0) and \
                (a.DataWithholdingReason is Null or a.DataWithholdingReason='') \
                and b.ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154) ''' % (databasename, databasename, databasename, databasename, databasename, databasename, databasename, listid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        namelistproxy = conn.execute(query)
        if namelistproxy != None:
            namelist=R2L(namelistproxy)
    return namelist 

def getAllCommonNamesFromListFlat(databasename, listid):
    namelist = []
    if not cleanDatabasename(databasename):
        return []
    databasename=diversitydatabase(databasename)
    query = u'''select '%s' as DatabaseName, a.NameID, c.CommonName, c.CountryCode, c.LanguageCode, b.ProjectID \
                from [%s].[dbo].[TaxonName] a inner join [%s].[dbo].[TaxonNameList] b on  \
                a.NameID = b.NameID \
                inner join [%s].[dbo].[TaxonCommonName] c on a.NameID = c.NameID
                where b.ProjectID=%s and \
                (a.RevisionLevel is Null or a.RevisionLevel='final revision') and \
                (a.IgnoreButKeepForReference is Null or a.IgnoreButKeepForReference=0) and \
                (a.DataWithholdingReason is Null or a.DataWithholdingReason='') \
                and b.ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154) ''' % (databasename, databasename, databasename, databasename, listid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        namelistproxy = conn.execute(query)
        if namelistproxy != None:
            namelist=R2L(namelistproxy)
    return namelist 
###################


# get all taxonname in this db
def getTaxonNames(databasename):
    namelist = []
    if not cleanDatabasename(databasename):
        return []
    databasename=diversitydatabase(databasename)
    query = u'''select '%s' as DatabaseName, b.NameID, a.ProjectID from [%s].[dbo].[TaxonName] b inner join [%s].[dbo].[TaxonNameList] a on a.NameID=b.NameID where \
                (b.RevisionLevel is Null or b.RevisionLevel='final revision') and \
                (b.IgnoreButKeepForReference is Null or b.IgnoreButKeepForReference=0) and \
                (b.DataWithholdingReason is Null or b.DataWithholdingReason='') ''' % (databasename, databasename, databasename)
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
    databasename=diversitydatabase(databasename)
    query = u'''select '%s' as DatabaseName, a.NameID, a.TaxonNameCache, a.Version, a.TaxonomicRank as TaxonomicRankCode, c.DisplayText as TaxonomicRank, a.GenusOrSupragenericName, \
                a.InfragenericEpithet, a.SpeciesEpithet, a.InfraspecificEpithet, a.BasionymAuthors, \
                a.CombiningAuthors, a.PublishingAuthors, a.SanctioningAuthor, a.NonNomenclaturalNameSuffix, a.IsRecombination, \
                a.ReferenceTitle, a.ReferenceURI, \
                a.Volume, a.Issue, a.Pages, a.YearOfPubl, a.NomenclaturalCode, a.NomenclaturalStatus, a.NomenclaturalComment, \
                a.AnamorphTeleomorph, a.TypistNotes, a.RevisionLevel, a.IgnoreButKeepForReference, b.ProjectID \
                from [%s].[dbo].[TaxonName] a inner join [%s].[dbo].[TaxonNameList] b on  \
                a.NameID=b.NameID left join [%s].[dbo].[TaxonNameTaxonomicRank_Enum] c on a.TaxonomicRank=c.Code
                where a.NameID=%s and \
                (a.RevisionLevel is Null or a.RevisionLevel='final revision') and \
                (a.IgnoreButKeepForReference is Null or a.IgnoreButKeepForReference=0) and \
                (a.DataWithholdingReason is Null or a.DataWithholdingReason='') \
                and ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154) ''' % (databasename, databasename, databasename, databasename, nameid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        namelistproxy = conn.execute(query)
        if namelistproxy != None:
            namelist=R2L(namelistproxy)
    return namelist                    

def getTaxonName_for_search_only(databasename, nameid):
    namelist = []
    if not cleanDatabasename(databasename):
        return []
    databasename=diversitydatabase(databasename)
    query = u'''select '%s' as DatabaseName, a.NameID, a.TaxonNameCache, a.Version, a.TaxonomicRank as TaxonomicRankCode, c.DisplayText as TaxonomicRank, a.GenusOrSupragenericName, \
                a.InfragenericEpithet, a.SpeciesEpithet, a.InfraspecificEpithet, a.BasionymAuthors, \
                a.CombiningAuthors, a.PublishingAuthors, a.SanctioningAuthor, a.NonNomenclaturalNameSuffix, a.IsRecombination, \
                a.ReferenceTitle, a.ReferenceURI, \
                a.Volume, a.Issue, a.Pages, a.YearOfPubl, a.NomenclaturalCode, a.NomenclaturalStatus, a.NomenclaturalComment, \
                a.AnamorphTeleomorph, a.TypistNotes, a.RevisionLevel, a.IgnoreButKeepForReference, b.ProjectID, \
                a.GenusOrSupragenericName + \
                case when a.InfragenericEpithet is null or a.InfragenericEpithet = '' then '' else \
                    case when a.NomenclaturalCode = 3 \
                        then case when a.TaxonomicRank = 'subgen.' then  + ' ' + a.TaxonomicRank + ' ' + a.InfragenericEpithet \
                        else ' (' + a.InfragenericEpithet + ')' end \
                    else ' ' + a.TaxonomicRank + ' ' + RTRIM(a.InfragenericEpithet) end \
                end \
                + \
                case when a.SpeciesEpithet is null or a.SpeciesEpithet  = '' then '' else ' ' + RTRIM(a.SpeciesEpithet) end \
                + \
                case when a.InfraspecificEpithet is null  or a.InfraspecificEpithet = '' \
                    then '' \
                    else \
                        case    when a.SpeciesEpithet <> a.InfraspecificEpithet \
                            then    ' ' + \
                            case when a.TaxonomicRank is null or a.TaxonomicRank = ''  then '' \
                            else case when a.NomenclaturalCode = 3 and (a.TaxonomicRank = 'ssp.' or a.TaxonomicRank = 'subsp.')  then '' else a.TaxonomicRank + ' ' end \
                            end \
                           + RTRIM(a.InfraspecificEpithet) \
                        else \
                        case when a.NomenclaturalCode = 3 /* Zoology */ and a.SpeciesEpithet = a.InfraspecificEpithet and  (a.TaxonomicRank = 'ssp.' or a.TaxonomicRank = 'subsp.') \
                            then ' ' + RTRIM(a.InfraspecificEpithet) else '' end \
                        end \
                end as TaxonName_for_search_only \
                from [%s].[dbo].[TaxonName] a inner join [%s].[dbo].[TaxonNameList] b on  \
                a.NameID=b.NameID left join [%s].[dbo].[TaxonNameTaxonomicRank_Enum] c on a.TaxonomicRank=c.Code
                where a.NameID=%s and \
                (a.RevisionLevel is Null or a.RevisionLevel='final revision') and \
                (a.IgnoreButKeepForReference is Null or a.IgnoreButKeepForReference=0) and \
                (a.DataWithholdingReason is Null or a.DataWithholdingReason='') \
                and ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154) ''' % (databasename, databasename, databasename, databasename, nameid)
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
    databasename=diversitydatabase(databasename)
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
    databasename=diversitydatabase(databasename)
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
    databasename=diversitydatabase(databasename)
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
    databasename=diversitydatabase(databasename)
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
    database=diversitydatabase(database)
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
    database=diversitydatabase(database)
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
    database=diversitydatabase(database)
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
    database=diversitydatabase(database)
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

def getTaxonHierarchyFull(database, projectid,  nameid, ignorebutkeepforreferences):
    anamelist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    
    query = ('''with hierachy as (
                   select NameID as baseNameID, NameID, NameParentID, 0 as level, ProjectID 
                   from [%s].dbo.TaxonHierarchy
                   where NameID=%s and IgnoreButKeepForReference = %s
                 union all
                 select child.baseNameID, name.NameID, name.NameParentID, child.level +1 as level, child.ProjectID
                   from hierachy as child
                     inner join %s.dbo.TaxonHierarchy as name
                       on child.NameParentID = name.NameID and child.ProjectID = name.ProjectID
                   where name.IgnoreButKeepForReference = %s
                )
                select a.*, n.TaxonNameCache, n.TaxonomicRank as TaxonomicRankCode, c.DisplayText as TaxonomicRank 
                    from hierachy a 
                        left join %s.dbo.TaxonName n 
                        on a.NameID=n.nameID 
                        left join %s.dbo.TaxonNameTaxonomicRank_Enum c on
                        n.TaxonomicRank=c.Code
                order by baseNameID, level;''')  % (database, nameid, ignorebutkeepforreferences, database, ignorebutkeepforreferences, database, database)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tanamelist = conn.execute(query)
        if tanamelist != None:
            anamelist=R2L(tanamelist)
    return anamelist

