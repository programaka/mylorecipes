import webapp2
import jinja2
import logging
import os

from google.appengine.ext import db
from google.appengine.api import memcache

# basically says I'm going to have a directory called "templates",
# and we're going to put those templated in there
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    # keeps us from having to type self.response.out all the time
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    # takes a template name and some dictionary, basically,
    # of parameters, things to substitute into the template
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    # calls write and render_str to print out a templateh
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Skills(Handler):
	def get(self):
		self.write("A list of skills:")
		self.render("skills.html")



application = webapp2.WSGIApplication([('/skills/?', Skills),
										],
										debug=True)