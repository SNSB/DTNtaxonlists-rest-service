# TaxonName-Database specific functions

from flask import current_app
from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
import re

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

# also change in the search.py 701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708, 707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865

# get all TaxonNameLists in this database:
def getTaxonNameLists(databasename):
    urilist = []
    if not cleanDatabasename(databasename):
        return []
    databasename=diversitydatabase(databasename)
    query = u'''select distinct '%s' as DatabaseName, a.ProjectID, a.ProjectURI, a.DefaultProjectID from [%s].[dbo].[TaxonNameListProjectProxy] a \
                where a.ProjectID in (select distinct c.ProjectID  from [%s].[dbo].[TaxonName] b inner \
                join [%s].[dbo].[TaxonNameList] c on b.NameID=c.NameID \
                where (b.RevisionLevel is null or b.RevisionLevel = 'final revision') and \
                (b.IgnoreButKeepForReference is Null or b.IgnoreButKeepForReference=0) and \
                (b.DataWithholdingReason is Null or b.DataWithholdingReason='')) and \
                a.ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865) \
                ''' % (databasename,databasename, databasename,databasename) # TODO: Revision level has to be 'final revision'
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        projectURI = conn.execute(query)
        if projectURI != None:
            for uri in projectURI:
                if uri['ProjectURI'] != None:
                    urilist.append({'projectid':uri['ProjectID'], 'projecturi':uri['ProjectURI'], 'DatabaseName': databasename, 'DefaultProjectID':uri['DefaultProjectID']})
    return urilist

# get the Project uri for the given list
def getTaxonNameListsProjectUri(databasename, id):
    urilist = []
    if not cleanDatabasename(databasename):
        return []
    databasename=diversitydatabase(databasename)
    query = u'select distinct ProjectURI, DefaultProjectID from [%s].[dbo].[TaxonNameListProjectProxy] where ProjectID=%s and ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865)' % (databasename, id)
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
    query = u'''select distinct '%s' as 'DatabaseName', a.NameID, a.Notes from [%s].[dbo].[TaxonNameList] a inner join [%s].[dbo].[TaxonName] b on a.NameID=b.NameID where \
                (b.RevisionLevel is Null or b.RevisionLevel='final revision') and \
                (b.IgnoreButKeepForReference is Null or b.IgnoreButKeepForReference=0) and \
                (b.DataWithholdingReason is Null or b.DataWithholdingReason='') \
                and ProjectID=%s and \
                ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865)''' % (databasename, databasename, databasename, listid)
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
    query0 = u'''select DefaultProjectID from [%s].[dbo].[TaxonNameListProjectProxy] where projectID=%s''' % (databasename, listid)
    current_app.logger.debug("Query DefaultProjectID %s " % (query0))
    defaultproject=""
    with get_db().connect() as conn:
        defaultproxy = conn.execute(query0)
        if defaultproxy and defaultproxy:
            defaultproject=defaultproxy.scalar() 
 
    if defaultproject:
        subjoin = ''' and hi.ProjectID=%s ''' % defaultproject
    else:
        subjoin = ''
    current_app.logger.debug("Limiting hierarchy to DefaultProjectID '%s' " % (subjoin))    
    query = u'''select distinct '%s' as DatabaseName, a.NameID, a.TaxonNameCache, a.Version, a.TaxonomicRank as TaxonomicRankCode, c.DisplayText as TaxonomicRank, a.GenusOrSupragenericName, \
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
                [%s].[dbo].[TaxonAcceptedName] an on an.NameID = a.NameID  and (an.IgnoreButKeepForReference is null or an.IgnoreButKeepForReference = 0) left join \
                [%s].[dbo].[TaxonHierarchy] hi on hi.NameID = a.NameID and (hi.IgnoreButKeepForReference is null or hi.IgnoreButKeepForReference = 0) %s left join \
                [%s].[dbo].[TaxonSynonymy] sy on sy.NameID = a.NameID and (sy.IgnoreButKeepForReference is null or sy.IgnoreButKeepForReference = 0) \
                where b.ProjectID=%s and \
                (a.RevisionLevel is Null or a.RevisionLevel='final revision') and \
                (a.IgnoreButKeepForReference is Null or a.IgnoreButKeepForReference=0) and \
                (a.DataWithholdingReason is Null or a.DataWithholdingReason='') \
                and b.ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865) ''' % (databasename, databasename, databasename, databasename, databasename, databasename, subjoin ,databasename, listid)
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
    query = u'''select distinct '%s' as DatabaseName, a.NameID, c.CommonName, c.CountryCode, c.LanguageCode, b.ProjectID \
                from [%s].[dbo].[TaxonName] a inner join [%s].[dbo].[TaxonNameList] b on  \
                a.NameID = b.NameID \
                inner join [%s].[dbo].[TaxonCommonName] c on a.NameID = c.NameID
                where b.ProjectID=%s and \
                (a.RevisionLevel is Null or a.RevisionLevel='final revision') and \
                (a.IgnoreButKeepForReference is Null or a.IgnoreButKeepForReference=0) and \
                (a.DataWithholdingReason is Null or a.DataWithholdingReason='') \
                and b.ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865) ''' % (databasename, databasename, databasename, databasename, listid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        namelistproxy = conn.execute(query)
        if namelistproxy != None:
            namelist=R2L(namelistproxy)
    return namelist 
###################

def getAllTaxonNameListForName(databasename, nameid):
    listlist = []
    if not cleanDatabasename(databasename):
        return []
    databasename=diversitydatabase(databasename)
    query = u'''select distinct '%s' as DatabaseName, a.NameID, a.Notes, a.ProjectID from [%s].[dbo].[TaxonNameList] a inner join [%s].[dbo].[TaxonName] b on a.NameID=b.NameID where \
                (b.RevisionLevel is Null or b.RevisionLevel='final revision') and \
                (b.IgnoreButKeepForReference is Null or b.IgnoreButKeepForReference=0) and \
                (b.DataWithholdingReason is Null or b.DataWithholdingReason='') \
                and a.NameID=%s and \
                a.ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865)''' % (databasename,databasename, databasename, nameid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        nameids = conn.execute(query)
        if nameids != None:
            listlist = R2L(nameids)
    return listlist

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
    query = u'''select distinct '%s' as DatabaseName, a.NameID, a.TaxonNameCache, a.Version, a.TaxonomicRank as TaxonomicRankCode, c.DisplayText as TaxonomicRank, a.GenusOrSupragenericName, \
                a.InfragenericEpithet, a.SpeciesEpithet, a.InfraspecificEpithet, a.BasionymAuthors, \
                a.CombiningAuthors, a.PublishingAuthors, a.SanctioningAuthor, a.NonNomenclaturalNameSuffix, a.IsRecombination, \
                a.ReferenceTitle, a.ReferenceURI,  d.DefaultProjectID, \
                a.Volume, a.Issue, a.Pages, a.YearOfPubl, a.NomenclaturalCode, a.NomenclaturalStatus, a.NomenclaturalComment, \
                a.AnamorphTeleomorph, a.TypistNotes, a.RevisionLevel, a.IgnoreButKeepForReference  \
                from [%s].[dbo].[TaxonName] a inner join [%s].[dbo].[TaxonNameList] b on  \
                a.NameID=b.NameID left join [%s].[dbo].[TaxonNameTaxonomicRank_Enum] c on a.TaxonomicRank=c.Code left join [%s].[dbo].[TaxonNameListProjectProxy] d on
                b.ProjectID=d.ProjectID
                where a.NameID=%s and \
                (a.RevisionLevel is Null or a.RevisionLevel='final revision') and \
                (a.IgnoreButKeepForReference is Null or a.IgnoreButKeepForReference=0) and \
                (a.DataWithholdingReason is Null or a.DataWithholdingReason='') \
                and b.ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865) ''' % (databasename, databasename, databasename, databasename, databasename, nameid)
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
    query = u'''select distinct '%s' as DatabaseName, a.NameID, a.TaxonNameCache, a.Version, a.TaxonomicRank as TaxonomicRankCode, c.DisplayText as TaxonomicRank, a.GenusOrSupragenericName, \
                a.InfragenericEpithet, a.SpeciesEpithet, a.InfraspecificEpithet, a.BasionymAuthors, \
                a.CombiningAuthors, a.PublishingAuthors, a.SanctioningAuthor, a.NonNomenclaturalNameSuffix, a.IsRecombination, \
                a.ReferenceTitle, a.ReferenceURI, \
                a.Volume, a.Issue, a.Pages, a.YearOfPubl, a.NomenclaturalCode, a.NomenclaturalStatus, a.NomenclaturalComment, \
                a.AnamorphTeleomorph, a.TypistNotes, a.RevisionLevel, a.IgnoreButKeepForReference, \
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
                and ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865) ''' % (databasename, databasename, databasename, databasename, nameid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        namelistproxy = conn.execute(query)
        if namelistproxy != None:
            namelist=R2L(namelistproxy)
    return namelist  


def findTaxonNames(databasename, namestring):
    namelist = []
    if not cleanDatabasename(databasename):
        return []
    if not namestring or len(namestring) > 200 or re.match(".*['\"\;\<\>\!].*",namestring):
        current_app.logger.debug("ERROR ATTACK! %s " % namestring)
        return []
    databasename=diversitydatabase(databasename)
    query = u'''select distinct '%s' as DatabaseName, b.NameID, b.TaxonNameCache from [%s].[dbo].[TaxonName] b inner join [%s].[dbo].[TaxonNameList] a on a.NameID=b.NameID where \
                (b.RevisionLevel is Null or b.RevisionLevel='final revision') and \
                (b.IgnoreButKeepForReference is Null or b.IgnoreButKeepForReference=0) and \
                (b.DataWithholdingReason is Null or b.DataWithholdingReason='') \
                and a.ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865) \
                and b.TaxonNameCache = '%s' ''' % (databasename, databasename, databasename, namestring)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        namelistproxy = conn.execute(query)
        if namelistproxy != None:
            namelist = R2L(namelistproxy)
    current_app.logger.debug("Resultlen = %i " % len(namelist))
    return namelist

def findTaxonNamePartly(databasename, namestring):
    namelist = []
    if not cleanDatabasename(databasename):
        return []
    if not namestring or len(namestring) > 200 or re.match(".*['\"\;\<\>\!].*",namestring):
        current_app.logger.debug("ERROR ATTACK! %s " % namestring)
        return []
    
    databasename=diversitydatabase(databasename)
    query = u'''select distinct '%s' as DatabaseName, a.NameID, a.TaxonNameCache, a.TypistNotes, a.RevisionLevel, a.IgnoreButKeepForReference \
                from [%s].[dbo].[TaxonName] a inner join [%s].[dbo].[TaxonNameList] b on  \
                a.NameID=b.NameID left join [%s].[dbo].[TaxonNameTaxonomicRank_Enum] c on a.TaxonomicRank=c.Code
                where \
                (a.RevisionLevel is Null or a.RevisionLevel='final revision') and \
                (a.IgnoreButKeepForReference is Null or a.IgnoreButKeepForReference=0) and \
                (a.DataWithholdingReason is Null or a.DataWithholdingReason='') \
                and ProjectID in (701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154, 923, 924, 925, 926, 927, 854, 856, 858, 867, 863, 715, 711, 703, 708 ,707, 702, 706, 712, 713, 716, 710, 705, 1138, 714, 876, 881, 866, 857, 860, 874, 878, 868, 880, 869, 877, 859, 861, 872, 879, 873, 381, 862, 870, 871, 864, 865) \
                and (a.GenusOrSupragenericName + \
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
                end) = '%s' ''' % (databasename, databasename, databasename, databasename, namestring)
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

def findCommonNames(databasename, namestring):
    commonnamelist =[]
    if not cleanDatabasename(databasename):
        return []
    if not namestring or len(namestring) > 200 or re.match(".*['\"\;\<\>\!].*",namestring):
        current_app.logger.debug("ERROR ATTACK! %s " % namestring)
        return []    
    databasename=diversitydatabase(databasename)
    query = u'''select '%s' as DatabaseName, NameID, CommonName, LanguageCode, CountryCode, ReferenceTitle, ReferenceURI, \
               ReferenceDetails, SubjectContext, Notes \
               from [%s].[dbo].[TaxonCommonName] where CommonName = '%s' ''' % (databasename, databasename, namestring)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        cnamelist = conn.execute(query)
        if cnamelist != None:
            commonnamelist=R2L(cnamelist)
    current_app.logger.debug("Resultlen = %i " % len(commonnamelist))            
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
            if len(acceptednamelist)>0:
                defaultProjectList = getTaxonNameDefaultProject(databasename, nameid)
                defaultProject = None
                if len(defaultProjectList)>0:
                    defaultProject = defaultProjectList[0]['DefaultProjectID']                
                for ac in acceptednamelist:
                    if ac['ProjectID'] == defaultProject:
                        ac['DefaultProject']='True'             
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
            if len(synonmylist)>0:
                defaultProjectList = getTaxonNameDefaultProject(databasename, nameid)
                defaultProject = None
                if len(defaultProjectList)>0:
                    defaultProject = defaultProjectList[0]['DefaultProjectID'] 
                for sy in synonmylist:
                    if sy['ProjectID'] == defaultProject:
                        sy['DefaultProject']='True'            
    return synonmylist  

def getTaxonNameDefaultProject(databasename, nameid):
    defaultProjectList =[]
    if not cleanDatabasename(databasename):
        return []
    databasename=diversitydatabase(databasename)
    query = u'''select distinct b.DefaultProjectID \
               from [%s].[dbo].[TaxonNameList] a inner join [%s].[dbo].[TaxonNameListProjectProxy] b \
               on a.ProjectID=b.ProjectID \
               where a.NameID = %s \
               ''' % (databasename, databasename, nameid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        defProjects = conn.execute(query)
        if defProjects != None:
            defaultProjectList=R2L(defProjects)
    return defaultProjectList                    
    

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
            if len(hierarchylist)>0:
                defaultProjectList = getTaxonNameDefaultProject(databasename, nameid)
                defaultProject = None
                if len(defaultProjectList)>0:
                    defaultProject = defaultProjectList[0]['DefaultProjectID']                
                for hi in hierarchylist:
                    if hi['ProjectID'] == defaultProject:
                        hi['DefaultProject']='True'
    return hierarchylist  
    
################################

def getCommonName(database, nameid, commonname, languagecode, countrycode, referencetitle):
    cnamelist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = u''' select '%s' as DatabaseName, NameID, CommonName, LanguageCode, CountryCode, ReferenceTitle, ReferenceURI, \
                ReferenceDetails, SubjectContext, Notes \
                from [%s].[dbo].[TaxonCommonName] where NameID=%s and CommonName='%s'and LanguageCode='%s' \
                and CountryCode = '%s' and ReferenceTitle = '%s' ''' % (database, database, nameid, commonname, languagecode, countrycode, referencetitle)
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

def getTaxonHierarchyNarrowerFull(database, projectid,  nameid, ignorebutkeepforreferences):
    anamelist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    
    query = ('''with hierachy as (
                   select NameID as baseNameID, NameID, NameParentID, 0 as level, ProjectID 
                   from [%s].dbo.TaxonHierarchy
                   where NameID=%s and IgnoreButKeepForReference = %s
                 union all
                 select child.baseNameID, name.NameID, name.NameParentID, child.level -1 as level, child.ProjectID
                   from hierachy as child
                     inner join %s.dbo.TaxonHierarchy as name
                       on child.NameID = name.NameParentID and child.ProjectID = name.ProjectID
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

# -----------------------------------------------
# Analysis

def getAnalysisCategoriesAll(database):
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ('''select '%s' as DatabaseName, AnalysisID, AnalysisParentID, DisplayText, Description, AnalysisURI,
                   ReferenceTitle, ReferenceURI, Notes
                   from [%s].[dbo].[TaxonNameListAnalysisCategory];''') % (database, database)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tanamelist = conn.execute(text(query))
        if tanamelist != None:
            aclist=R2L(tanamelist)
    return aclist


def getAnalysisCategorie(database, analysisid):
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ('''select '%s' as DatabaseName, AnalysisID, AnalysisParentID, DisplayText, Description, AnalysisURI, 
                   ReferenceTitle, ReferenceURI, Notes
                   from [%s].[dbo].[TaxonNameListAnalysisCategory]
                   where AnalysisID= :analid;''') % (database, database)
    current_app.logger.debug("Query %s with analid %s" % (query, analysisid))
    with get_db().connect() as conn:
        tanamelist = conn.execute(text(query), analid=analysisid)
        if tanamelist != None:
            aclist=R2L(tanamelist)
    return aclist


def getAnalysisCategorieChilds(database, analysisparentid):
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ('''select '%s' as DatabaseName, AnalysisID, AnalysisParentID, DisplayText, Description, AnalysisURI,
                   ReferenceTitle, ReferenceURI, Notes
                   from [%s].[dbo].[TaxonNameListAnalysisCategory]
                   where AnalysisParentID= :analid;''') % (database, database)
    current_app.logger.debug("Query %s with analid %s" % (query, analysisparentid))
    with get_db().connect() as conn:
        tanamelist = conn.execute(text(query), analid=analysisparentid)
        if tanamelist != None:
            aclist=R2L(tanamelist)
    return aclist


def getAnalysisValuesAll(database, analysisid):
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ('''select '%s' as DatabaseName, AnalysisID, AnalysisValue, Description, 
                      DisplayText, DisplayOrder, Notes
                   from [%s].[dbo].[TaxonNameListAnalysisCategoryValue]
                   where AnalysisID = :analid;''') % (database, database)
    current_app.logger.debug("Query %s with analid %s" % (query, analysisid))
    with get_db().connect() as conn:
        tanamelist = conn.execute(text(query), analid=analysisid)
        if tanamelist != None:
            aclist=R2L(tanamelist)
    return aclist


def getAnalysisValue(database, analysisid, analysisvalue):
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ('''select '%s' as DatabaseName, AnalysisID, AnalysisValue, Description, 
                      DisplayText, DisplayOrder, Notes
                   from [%s].[dbo].[TaxonNameListAnalysisCategoryValue]
                   where AnalysisID = :analid and AnalysisValue = :avalue;''') % (database, database)
    current_app.logger.debug("Query %s with analid %s and avalue '%s'" % (query, analysisid, analysisvalue))
    with get_db().connect() as conn:
        tanamelist = conn.execute(text(query), analid=analysisid, avalue=analysisvalue)
        if tanamelist != None:
            aclist=R2L(tanamelist)
    return aclist


def getAnalysisInProject(database,projectid):
    # return all AnalysisIDs in that project
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ('''select distinct '%s' as DatabaseName, ProjectID, AnalysisID
                   from [%s].[dbo].[TaxonNameListAnalysis]
                   where ProjectID = :pvalue;''') % (database, database)
    current_app.logger.debug("Query %s with pvalue %s " % (query, projectid))
    with get_db().connect() as conn:
        tanamelist = conn.execute(text(query), pvalue=projectid)
        if tanamelist != None:
            aclist=R2L(tanamelist)
    return aclist

def getAnalysisAll(database, projectid, analysisid):
    # returns all nameids (and extrafields) with the given analysisid
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ('''select distinct '%s' as DatabaseName, ProjectID, AnalysisID,
                   NameID, AnalysisValue, Notes, TaxonNameListRefID
                   from [%s].[dbo].[TaxonNameListAnalysis]
                   where ProjectID = :pvalue and AnalysisID= :avalue;''') % (database, database)
    current_app.logger.debug("Query %s with pvalue %s and avalue %s" % (query, projectid, analysisid))
    with get_db().connect() as conn:
        tanamelist = conn.execute(text(query), pvalue=projectid, avalue=analysisid)
        if tanamelist != None:
            aclist=R2L(tanamelist)
    return aclist

def getAnalysisAllTaxRef(database, projectid, analysisid, taxref):
    # returns all nameids (and extrafields) with the given analysisid
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ('''select distinct '%s' as DatabaseName, ProjectID, AnalysisID,
                   NameID, AnalysisValue, Notes, TaxonNameListRefID
                   from [%s].[dbo].[TaxonNameListAnalysis]
                   where ProjectID = :pvalue and AnalysisID= :avalue and TaxonNAmeListRefID = :tref;''') % (database, database)
    current_app.logger.debug("Query %s with pvalue %s ans avalue %s, tref: %s" % (query, projectid, analysisid, taxref))
    with get_db().connect() as conn:
        tanamelist = conn.execute(text(query), pvalue=projectid, avalue=analysisid, tref=taxref)
        if tanamelist != None:
            aclist=R2L(tanamelist)
    return aclist

def getAnalysis(database, projectid, nameid, analysisid, taxonnamelistrefid):
    # returns the analysis for the given name in the refenence SubjectContext
    # if reference context is -1 it is normally ignored in the database
    # if taxnameref is -1 we ignore the key in the query
    # returns all analysvalues (and extrafields) with the given nameid and analysisid
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    if taxonnamelistrefid < 0:
        query = ('''select '%s' as DatabaseName, ProjectID, AnalysisID,
                    NameID, AnalysisValue, Notes, TaxonNameListRefID
                    from [%s].[dbo].[TaxonNameListAnalysis]
                    where ProjectID = :pvalue and 
                            AnalysisID = :avalue and
                            NameID = :nvalue;''') % (database, database)
        current_app.logger.debug("Query %s with pvalue %s " % (query, projectid))
        with get_db().connect() as conn:
            tanamelist = conn.execute(text(query), pvalue=projectid, avalue=analysisid, nvalue=nameid)
            if tanamelist != None:
                aclist=R2L(tanamelist)
    else:
        query = ('''select '%s' as DatabaseName, ProjectID, AnalysisID,
                    NameID, AnalysisValue, Notes, TaxonNameListRefID
                    from [%s].[dbo].[TaxonNameListAnalysis]
                    where ProjectID = :pvalue and 
                            AnalysisID = :avalue and
                            NameID = :nvalue and
                            TaxonNameListRefID = :tvalue;''') % (database, database)
        current_app.logger.debug("Query %s with pvalue %s " % (query, projectid))
        with get_db().connect() as conn:
            tanamelist = conn.execute(text(query), pvalue=projectid, avalue=analysisid, nvalue=nameid, tvalue=taxonnamelistrefid)
            if tanamelist != None:
                aclist=R2L(tanamelist)        
    return aclist

def getAnalysisCategoriesforName(database, projectid, nameid):
    # returns the analysis for the given name in the refenence SubjectContext
    # returns all analysvalues (and extrafields) with the given nameid
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ('''select distinct '%s' as DatabaseName, ProjectID, AnalysisID,
                NameID
                from [%s].[dbo].[TaxonNameListAnalysis]
                where ProjectID = :pvalue and 
                        NameID = :nvalue;''') % (database, database)
    current_app.logger.debug("Query %s with pvalue %s, nvalue %s" % (query, projectid, nameid))
    with get_db().connect() as conn:
        tanamelist = conn.execute(text(query), pvalue=projectid, nvalue=nameid)
        if tanamelist != None:
            aclist=R2L(tanamelist)
    return aclist

def getAnalysisfilter(database, projectid, analysisid, taxonnamelistrefid, analysisvalue, operator='=', opnot = ''):
    # returns the analysis for the given name in the refenence SubjectContext
    # if reference context is -1 it is normally ignored in the database
    # if taxnameref is -1 we ignore the key in the query
    # returns all nameids (and extrafields) with the given analysisid
    # filtered by the analysisvalue
    aclist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    if taxonnamelistrefid < 0:
        query = ('''select '%s' as DatabaseName, ProjectID, AnalysisID,
                    NameID, AnalysisValue, Notes, TaxonNameListRefID
                    from [%s].[dbo].[TaxonNameListAnalysis]
                    where ProjectID = :pvalue and 
                            AnalysisID = :avalue and %s
                            AnalysisValue %s :analvalue;''') % (database, database, opnot, operator)
        current_app.logger.debug("Query %s with pvalue %s, avalue %s, analvalue '%s'" % (query, projectid, analysisid, analysisvalue))
        with get_db().connect() as conn:
            tanamelist = conn.execute(text(query), pvalue=projectid, avalue=analysisid, analvalue=analysisvalue)
            if tanamelist != None:
                aclist=R2L(tanamelist)
    else:
        query = ('''select '%s' as DatabaseName, ProjectID, AnalysisID,
                    NameID, AnalysisValue, Notes, TaxonNameListRefID
                    from [%s].[dbo].[TaxonNameListAnalysis]
                    where ProjectID = :pvalue and 
                            AnalysisID = :avalue and
                            TaxonNameListRefID = :tvalue and
                            AnalysisValue %s :analvalue;''') % (database, database, operator)
        current_app.logger.debug("Query %s with pvalue %s, avalue %s, analvalue '%s', tvalue %s" % (query, projectid, analysisid, analysisvalue, taxonnamelistrefid))
        with get_db().connect() as conn:
            tanamelist = conn.execute(text(query), pvalue=projectid, avalue=analysisid, tvalue=taxonnamelistrefid, analvalue=analysisvalue)
            if tanamelist != None:
                aclist=R2L(tanamelist)        
    return aclist


# ----------------------- Find References --------------------------------



def findTaxonnameWithReference(database, referenceurl):
    taxonnamelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query=u''' 
    select '%s' as DatabaseName, NameID from [%s].[dbo].[TaxonName] 
              where [ReferenceURI] = '%s' or TypificationReferenceURI = '%s' 
    union
    select '%s' as DatabaseName, NameID from [%s].[dbo].[TaxonName] 
              where [TypificationReferenceURI] = '%s'
    union
    select '%s' as DatabaseName, NameID from [%s].[dbo].[TaxonNameTypification]
              where [TypificationReferenceURI] = '%s';
    ''' % (database, database, referenceurl, database, database, referenceurl, database, database, referenceurl)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        alist = conn.execute(query, refuri=referenceurl)
        if alist != None:
           taxonnamelist = R2L(alist)
    return taxonnamelist


def findTaxonnamelistWithReference(database, referenceurl):
    taxonnamelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query=u''' select distinct '%s' as DatabaseName, ProjectID from [%s].[dbo].[TaxonNameListReference] where [TaxonNameListRefURI] = '%s'; ''' % (database, database, referenceurl)
    current_app.logger.debug("Query %s with refuri = '%s'" % (query, referenceurl))
    with get_db().connect() as conn:
        alist = conn.execute(query, refuri=referenceurl)
        if alist != None:
           taxonnamelist = R2L(alist)
    return taxonnamelist


def findTaxonCommonnameWithReference(database, referenceurl):
    taxonnamelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query=u''' select '%s' as DatabaseName, NameID, CommonName, LanguageCode, CountryCode, ReferenceTitle from [%s].[dbo].[TaxonCommonName] where [ReferenceURI] = '%s'; ''' % (database, database, referenceurl)
    current_app.logger.debug("Query %s with refuri = '%s'" % (query, referenceurl))
    with get_db().connect() as conn:
        alist = conn.execute(query, refuri=referenceurl)
        if alist != None:
            taxonnamelist = R2L(alist)
    return taxonnamelist


def findTaxonAcceptednameWithReference(database, referenceurl):
    taxonnamelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query=u''' select '%s' as DatabaseName, NameID, ProjectID from [%s].[dbo].[TaxonAcceptedName] where [RefURI] = '%s'; ''' % (database, database, referenceurl)
    current_app.logger.debug("Query %s with refuri = '%s'" % (query, referenceurl))
    with get_db().connect() as conn:
        alist = conn.execute(query, refuri=referenceurl)
        if alist != None:
           taxonnamelist = R2L(alist)
    return taxonnamelist


def findTaxonSynonymWithReference(database, referenceurl):
    taxonnamelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query=u''' select '%s' as DatabaseName, NameID, ProjectID from [%s].[dbo].[TaxonSynonymy] where [SynRefURI] = '%s'; ''' % (database, database, referenceurl)
    current_app.logger.debug("Query %s with refuri = '%s'" % (query, referenceurl))
    with get_db().connect() as conn:
        alist = conn.execute(query, refuri=referenceurl)
        if alist != None:
           taxonnamelist = R2L(alist)
    return taxonnamelist


def findTaxonHierarchyWithReference(database, referenceurl):
    taxonnamelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query=u''' select '%s' as DatabaseName, NameID, ProjectID from [%s].[dbo].[TaxonHierarchy] where [HierarchyRefURI] = '%s'; ''' % (database, database, referenceurl)
    current_app.logger.debug("Query %s with refuri = '%s'" % (query, referenceurl))
    with get_db().connect() as conn:
        alist = conn.execute(query, refuri=referenceurl)
        if alist != None:
           taxonnamelist = R2L(alist)
    return taxonnamelist

def findAnalysisCategoryWithReference(database, referenceurl):
    agnetlist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query=u''' select '%s' as DatabaseName, AnalysisID from [%s].[dbo].[TaxonNameListAnalysisCategory] where [ReferenceURI] = '%s'; ''' % (database, database, referenceurl)
    current_app.logger.debug("Query %s with refuri = '%s'" % (query, referenceurl))
    with get_db().connect() as conn:
        try:
            alist = conn.execute(query, refuri=referenceurl)
            if alist != None:
                agnetlist = R2L(alist)
        except ProgrammingError:
            return agnetlist
    return agnetlist
