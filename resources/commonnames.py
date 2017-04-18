# commonnames
# REST interface to commonnames

from flask.ext import restful
from flask_restful import reqparse
from flask import url_for
import re
from database.commonname import getcommonname, findCommonName
import urllib2
from urlparse import urlparse

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
def extractReferenceID(referenceuri):
    if referenceuri:
        parts = referenceuri.split('/')
        referenceid = parts[-1]
        if isInt(referenceid):
            return referenceid
    return None
        

class commonnames(restful.Resource):
    def get(self):
        results = []
        parser =  reqparse.RequestParser()
        parser.add_argument('exactcommonname')
        args = parser.parse_args()
        #createindex()
        if args['exactcommonname']:
            results = findCommonName(args['exactcommonname'])
            for row in results:
                links = []
                links.append(makelink('name', 'related', url_for('name', database=row['DatabaseName'], id=row['NameID'], _external=True) ))
                row['ReferenceURI'] = urlparse(row['ReferenceURI']).path
                referenceid = extractReferenceID(row['ReferenceURI'])
                if referenceid:
                    links.append(makelink('reference', 'related', url_for('referencetnt', id=referenceid, _external=True) ))
                row['links'] = links
        return results


class commonname(restful.Resource):
    def get(self, database, nameid, cid):
        # cid split [a,b,c,d] in a b c d
        commonname, languagecode, countrycode, referencetitle = re.sub("""[\[\]!"]""", "", cid).split("#")
        #print commonname #= commonname.encode('latin-1').decode('utf-8')
        results = getcommonname(database, nameid, commonname, languagecode, countrycode, referencetitle)
        for row in results:
            links = []
            links.append(makelink('name', 'related', url_for('name', database=row['DatabaseName'], id=row['NameID'], _external=True) ))
            row['ReferenceURI'] = urlparse(row['ReferenceURI']).path
            referenceid = extractReferenceID(row['ReferenceURI'])
            if referenceid:
                links.append(makelink('reference', 'related', url_for('referencetnt', id=referenceid, _external=True) ))
            row['links'] = links
        return results


