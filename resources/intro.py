# intro
# gives basic links to the RESTapi (esp. to /lists/)

import flask_restful as restful
from flask import render_template
from flask import url_for

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

class intro(restful.Resource):
    def get(self):
        links = []
        links.append(makelink('lists', 'related', url_for('taxonlists', _external=True)))
        links.append(makelink('names', 'related', url_for('names', _external=True)))
        links.append(makelink('projects', 'related', url_for('projects', _external=True)))
        links.append(makelink('agents', 'related', url_for('agents', _external=True)))
        links.append(makelink('contact', 'related', 'http://www.snsb.info'))
        return {'server':'http://tnt.diversityworkbench.de', 'links':links}
                     
                     
