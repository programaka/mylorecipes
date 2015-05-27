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
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

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
        self.render("signup.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        valid_username = signup_validation.validate_username(username)
        valid_password = signup_validation.validate_password(password)
        passwords_match = (password == verify)
        valid_email = signup_validation.validate_email(email)

        if not (valid_username and valid_password and passwords_match and valid_email):
            self.render("signup.html",
                        username = username,
                        password = "",
                        verify = "",
                        email = email,
                        username_error = signup_validation.username_validation_message(username),
                        password_error = signup_validation.password_validation_message(password),
                        verify_error = signup_validation.password_match_message(password, verify),
                        email_error = signup_validation.email_validation_message(email))
        else:
            a = User(username = username, password = make_pw_hash(username, password))
            a.put()
            time.sleep(1)

            # set username cookie
            username_hash = make_secure_val(a.username)
            cookie_value = str('name=%s; Path=/' % username_hash)

            self.response.headers.add_header('Set-Cookie', cookie_value)

            self.redirect("/blog")


class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
            cookie_value = self.request.cookies.get('name')
            username = cookie_value.split('|')[0]
            if make_secure_val(username) == cookie_value:
                self.response.out.write("Welcome, "+username+"!")
            else:
                self.redirect("/blog/signup")

application = webapp2.WSGIApplication([('/blog/signup', MainPage),
                                        ('/blog/welcome', WelcomeHandler)
                                        ],
                              debug=True)