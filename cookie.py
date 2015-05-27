import os
import webapp2
import jinja2
import time
import re
from google.appengine.ext import db
import hashlib

# basically says I'm going to have a directory called "templates",
# and we're going to put those templated in there
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def hash_str(s):
	return hashlib.md5(s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

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

class MainPage(Handler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		visits = 0
		visit_cookie_str = self.request.cookies.get('visits')
		if visit_cookie_str:
			cookie_val = check_secure_val(visit_cookie_str)
			if cookie_val:
				visits = int(cookie_val)

		visits +=1

		new_cookie_val = make_secure_val(str(visits))
		
		self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)

		if visits > 100:
			self.write("You are the best ever!")
		else:
			self.write("You've been here %s times!" % visits)


application = webapp2.WSGIApplication([('/unit4/cookie', MainPage)
										],
										debug=True)