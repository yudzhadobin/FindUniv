__author__ = 'yudzh_000'

import os
import enteries_sets
import jinja2
import webapp2



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Check(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('checkPage.html')

        town = self.request.get('town', '')
        offset = self.request.get('offset', 10)
        offset = int(offset)
        universities = enteries_sets.University.query(enteries_sets.University.town == town).fetch(limit=10, offset=offset)


        template_values = {'universities': universities}
        self.response.write(template.render(template_values))