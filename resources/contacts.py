# contacts
# REST interface to contacts

import flask_restful as restful

class contacts(restful.Resource):
    def get(self):
        pass

class contact(restful.Resource):
    def get(self, id):
        pass
