# queried %s seconds ago" % sec

import os
import webapp2
import jinja2
import time
import re
import json
import logging
import hashlib

from datetime import timedelta, datetime

from google.appengine.ext import db
from google.appengine.api import memcache

# basically says I'm going to have a directory called "templates",
# and we're going to put those templated in there
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def hash_str(s):
    return hashlib.sha256(s).hexdigest()

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

class Post(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class NewPost(Handler):
	#def render_front(self, subject="", content="", error=""):
	#	self.render(, subject=subject, content=content, error=error)

	def get(self):
		self.render("blog_newpost.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")
		
		if subject and content:
			a = Post(subject = subject, content = content)
			a.put()
			time.sleep(0.2)
			post_id = a.key().id()
			all_posts(True)
			self.redirect("/blog/%d" % post_id)
		else:
			error = "both subject and content need to be specified"
			self.render("blog_newpost.html", subject=subject, content=content, error = error)

def a_post(key, update = False):
	cached_result = memcache.get(key)
	if cached_result is None or update is True:

		logging.error("DB QUERY")
		post = Post.get_by_id(int(key))

		time = datetime.utcnow()
		memcache.set(key, (post, time))
	else:
		post, time = cached_result

	return time, post

class PostPage(Handler):
	def get(self, post_id):
		time, post = a_post(key = post_id)
		delta = (datetime.utcnow() - time).seconds
		# if not post:
		# 	self.error(405)
		# 	return
			
		self.render("blog_post.html", post=post, delta = delta)

class EditPost(Handler):
	def get(self, post_id):
		post = Post.get_by_id(int(post_id))
		# subject = str(post.subject)
		# content = str(post.content)

		self.render("blog_editpost.html", post=post)

	def post(self, post_id):
		subject = self.request.get("subject")
		content = self.request.get("content")
		
		if subject and content:
			post = Post.get_by_id(int(post_id))
			post.subject = subject
			post.content = content
			post.put()

			time.sleep(0.2)
			all_posts(True)
			memcache.set(post_id, (post, datetime.utcnow()))
			
			self.redirect("/blog/%d" % int(post_id))
		else:
			error = "both subject and content need to be specified"
			self.render("blog_newpost.html", subject=subject, content=content, error = error)


def all_posts(update = False):
	key = 'allposts'

	cached_result = memcache.get(key)
	if cached_result is None or update is True:

		logging.error("DB QUERY")
		posts = db.GqlQuery("SELECT * FROM Post "
							"ORDER BY created DESC")
		time = datetime.utcnow()
		
		posts = list(posts)
		memcache.set(key, (posts, time))
	else:
		posts, time = cached_result

	return time, posts

class AllPosts(Handler):
	def render_front(self, subject="", content=""):
		time, posts = all_posts()
		delta = (datetime.utcnow() - time).seconds 

		# check name cookie	
		cookie_value = self.request.cookies.get('name')
		if cookie_value:
			username = cookie_value.split('|')[0]
			is_login = make_secure_val(username) == cookie_value
		else:
			is_login = False
			username = None

		self.render("blog_allposts.html", subject=subject, content=content, posts=posts, delta=delta, is_login = is_login, username = username)
	
	def get(self):
		self.render_front()


class FlushCache(Handler):
	def get(self):
		memcache.flush_all()
		self.redirect("/blog")

class AllPostsJSON(Handler):
	def get(self):
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
		posts_json = []
		for post in posts:
			dic = {}
			dic["content"] = str(post.content)
			dic["subject"] = str(post.subject)
			posts_json.append(dic)

		self.write(json.dumps(posts_json))
		self.response.headers["content-type"] = "application/json; charset=utf-8"

class SinglePostJSON(Handler):
	def get(self, post_id):
		post = Post.get_by_id (int(post_id))
		dic = {}
		'"{}"'.format(str([]))
		dic["content"] = str(post.content)
		dic["subject"] = str(post.subject)

		self.write(json.dumps(dic))
		self.response.headers["content-type"] = "application/json; charset=utf-8"


application = webapp2.WSGIApplication([('/blog/newpost', NewPost),	
										('/blog/(\d+)', PostPage),
										('/blog/?', AllPosts),
										('/blog/_edit/(\d+)', EditPost),
										('/blog/\.json', AllPostsJSON),
										('/blog/(\d+)(?:\.json)?', SinglePostJSON),
										('/blog/flush/?', FlushCache)
										],
										debug=True)