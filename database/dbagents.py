# TaxonName-Database specific functions

from flask import current_app
from database.management import get_db, getDBs


DWB_MODULE='DiversityAgents_TNT'

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
    dblists=getDBs('DiversityAgents')
    if not databasename in dblists:
        return False
    return True

###########################

def getAgents(database):
    agentlist=[]
    query = u''' select '%s' as DatabaseName, AgentID
                 from [%s].[dbo].[Agent] where DataWithholdingReason is Null \
                 ''' % (database, database)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tagentlist = conn.execute(query)
        if tagentlist != None:
            agentlist=R2L(tagentlist)
    return agentlist

def getAgent(database, agentid):
    agentlist=[]
    query = u''' select '%s' as DatabaseName, AgentID, AgentParentID, AgentName, Version, AgentTitle, \
                 GivenName, GivenNamePostfix, InheritedName, InheritedNamePostfix, \
                 Abbreviation, AgentType, AgentRole, AgentGender, Description, \
                 OriginalSpelling, Notes, PlaceOfBirth, PlaceOfDeath, \
                 SynonymToAgentID, SynonymisationType, RevisionLevel, DataWithholdingReason, \
                 ValidFromDate, ValidFromDay, ValidFromMonth, ValidFromYear, \
                 ValidUntilDate, ValidUntilDay, ValidUntilMonth, ValidUntilYear
                 from [%s].[dbo].[Agent] \
                 where AgentID=%s and DataWithholdingReason is Null''' % (database, database, agentid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tagentlist = conn.execute(query)
        if tagentlist != None:
            agentlist=R2L(tagentlist)
    return agentlist

def getAgentRelations(database, agentid):
    agentlist=[]
    query = u''' select '%s' as DatabaseName, AgentID, RelatedAgentID, RelationType
                 from [%s].[dbo].[AgentRelation] \
                 where AgentID=%s ''' % (database, database, agentid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tagentlist = conn.execute(query)
        if tagentlist != None:
            agentlist=R2L(tagentlist)
    return agentlist