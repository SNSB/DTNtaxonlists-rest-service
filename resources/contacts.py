# contacts
# REST interface to contacts

from flask.ext import restful

class contacts(restful.Resource):
    def get(self):
        pass

class contact(restful.Resource):
    def get(self, id):
        pass
