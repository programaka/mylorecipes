# webapp2 - a lightweight framework that allows you quickly
# build simple web applications for the Python 2.7 runtime.
import webapp2
import signup_validation
import jinja2
import os
import time
import hashlib
import random
import string
import re
from google.appengine.ext import db


USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile("^.{3,20}$") 

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def validate_username(username):
    return USER_RE.match(username)

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt=make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

def hash_str(s):
    return hashlib.sha256(s).hexdigest()

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

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        if validate_username(username):
            user = db.GqlQuery("SELECT * FROM User WHERE username= :1", username).get()
            if user:
                pass_hash = user.password
                #self.write(pass_hash)
                if valid_pw(username, password, pass_hash):
                    # set username cookie
                    username_hash = make_secure_val(username)
                    cookie_value = str('name=%s; Path=/' % username_hash)
                    self.response.headers.add_header('Set-Cookie', cookie_value)
                    self.redirect("/blog")
                else:
                    self.render("login.html",
                        username = username,
                        password = "",
                        login_error = "Invalid login")
            else:
                self.render("login.html",
                    username = username,
                    password = "",
                    login_error = "Invalid login")

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
            cookie_value = self.request.cookies.get('name')
            username = cookie_value.split('|')[0]
            if make_secure_val(username) == cookie_value:
                self.response.out.write("Welcome, "+username+"!")
            else:
                self.redirect("/blog/signup")

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
            cookie_value = "name=; Path=/"
            self.response.headers.add_header('Set-Cookie', cookie_value)
            self.redirect("/blog")

application = webapp2.WSGIApplication([('/blog/login', MainPage),
                                        ('/blog/welcome', WelcomeHandler),
                                        ('/blog/logout', LogoutHandler)
                                        ],
                              debug=True)