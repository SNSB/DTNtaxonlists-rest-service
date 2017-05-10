# api tests

from flask.ext import restful
from flask.ext.restful import Resource
import requests

class testapi(restful.Resource):
    def __init__(self):
        self.baseurl = 'http://services.snsb.info/DTNtaxonlists/rest/v0.1'
        self.endpoints = [
        '/lists' ,
        '/lists/DiversityTaxonNames_Insecta/854/',
        '/lists/DiversityTaxonNames_Insecta/854/www',
        '/lists/DiversityTaxonNames_Insecta/854/project',
        '/lists/DiversityTaxonNames_Insecta/854/flat',
        '/lists/DiversityTaxonNames_Insecta/854/csv',
        '/lists/DiversityTaxonNames_Insecta/854/dwc',
        '/lists/DiversityTaxonNames_Insecta/854/dwc_offline',
        '/names/' ,
        '/names/DiversityTaxonNames_Insecta/5446067/' ,
        '/names/DiversityTaxonNames_Insecta/5446067/www' ,
        '/names/DiversityTaxonNames_Insecta/5000224/commonnames',
        '/names/DiversityTaxonNames_Insecta/5446067/acceptednames' ,
        '/names/DiversityTaxonNames_Insecta/5446067/synonyms' ,
        '/names/DiversityTaxonNames_Insecta/5446067/hierarchies' ,
        '/names/DiversityTaxonNames_Insecta/5446067/lists' ,
        '/Agents_TNT/',
        '/agents/DiversityAgents_TNT/43109' ,
        '/agents/DiversityAgents_TNT/43109/relations' ,
        '/Agents_TNT/43109/' ,
        '/Agents_TNT/43109/relations' ,
        '/contacts/1/',
        '/commonnames/',
        '/commonnames/DiversityTaxonNames_Insecta/5000224/%5BBlauseggen-Spornzikade%20%23de%23DE%23Artenliste%20der%20Zikaden%20Deutschlands%5D/',
        '/acceptednames/DiversityTaxonNames_Insecta/85/5000224/',
        '/synonymy/DiversityTaxonNames_Plants/1128/9/13/',
        '/hierarchy/DiversityTaxonNames_Insecta/85/5000224/',
        '/hierarchy/DiversityTaxonNames_Insecta/85/5000224/full',
        '/hierarchy/DiversityTaxonNames_Insecta/85/5000224/fullnarrow',
        '/projects/',
        '/Projects_TNT/864/',
        '/Projects_TNT/864/agents',
        '/Projects_TNT/864/references',
        '/Projects_TNT/864/licenses',
        '/Projects_TNT/864/modificationdate',
        '/references/',
        '/references/DiversityReferences_TNT/7462795/',
        '/References_TNT/608046211/',
        '/References_TNT/699074100/childs/',
        '/references/DiversityReferences_TNT/699074100/childs/',
        '/references/DiversityReferences_TNT/699074100/relations' ,
        '/referencerelation/DiversityReferences_TNT/1552085223/aut/3/',
        '/references/DiversityReferences_TNT/1552085223/referencing/',
        '/references/DiversityReferences_TNT/1552085223/referencing/names/',
        '/references/DiversityReferences_TNT/1552085223/referencing/acceptednames/',
        '/references/DiversityReferences_TNT/1552085223/referencing/synonyms/',
        '/references/DiversityReferences_TNT/1552085223/referencing/hierarchies/',
        '/references/DiversityReferences_TNT/1552085223/referencing/analysis/',
        '/references/DiversityReferences_TNT/1665225180/referencing/commonnames/',
        '/references/DiversityReferences_TNT/1665225180/referencing/taxonlists/',
        '/references/DiversityReferences_TNT/2042700531/referencing/projects/',
        '/references/DiversityReferences_TNT/1552085223/referencing/agents/',
        '/analysiscategories/',
        '/analysiscategories/DiversityTaxonNames_Animalia/59/',
        '/analysiscategories/DiversityTaxonNames_Animalia/59/childs/',
        '/analysiscategories/DiversityTaxonNames_Animalia/50/projects/',
        '/analysiscategories/DiversityTaxonNames_Animalia/50/valuedefinitions/',
        '/analysiscategorievalues/DiversityTaxonNames_Animalia/50/ex/',
        '/lists/DiversityTaxonNames_Animalia/712/analysis/',
        '/lists/DiversityTaxonNames_Animalia/712/analysis/55/',
        '/analysis/DiversityTaxonNames_Animalia/712/4404200/',
        '/analysis/DiversityTaxonNames_Animalia/712/4404200/55/'
        ]

    def testendpoint(self, url, errorlist):
        resp = requests.get(''.join([self.baseurl,url]))
        if resp.status_code != 200:
            errorlist.append("ERROR %s at %s" % (resp.status_code, url))
        return(resp.status_code) 

    def get(self):
        errorlist=[]
        retcode = 0
        for uri in self.endpoints:
            tcode = self.testendpoint(uri,errorlist)
            if tcode>retcode:
                retcode=tcode
        
        return errorlist, retcode



