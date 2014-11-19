# commonnames
# REST interface to commonnames

from flask.ext import restful
import re
from database.commonname import getcommonname
import urllib2

class commonnames(restful.Resource):
    def get(self):
        pass

class commonname(restful.Resource):
    def get(self, database, nameid, cid):
        # cid split [a,b,c,d] in a b c d
        commonname, languagecode, countrycode, referencetitle = re.sub("""[\[\]!#"]""", "", cid).split(",")
        #print commonname #= commonname.encode('latin-1').decode('utf-8')
        return getcommonname(database, nameid, commonname, languagecode, countrycode, referencetitle)
 
