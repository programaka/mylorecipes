import os
import webapp2
import jinja2
import time
from google.appengine.api import urlfetch
import urllib2
import logging
from xml.dom import minidom
from collections import namedtuple

from google.appengine.ext import db
from google.appengine.api import memcache

# make a basic Point class
#Point = namedtuple('Point', ["lat", "lon"])
#points = [Point(1,2),
#			Point(3,4),
#			Point(5,6)]

# implement the function gmaps_img(points) that returns the google maps 
# image for a map with the points passed in. An example of valid response
# looks like this:
#
# http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&markers=1,2&markers=3,4

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"

def gmaps_img(points):
	markers = '&'.join('markers=%s,%s' % (p.lat, p.lon)
						for p in points)
	return GMAPS_URL + markers

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
	ip  = "4.2.2.2"
	ip = "23.24.209.141"
	url = IP_URL + ip
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except URLError:
		return

	if content:
		# parse the xml and find the coordinates
		d = minidom.parseString(content)
		coords = d.getElementsByTagName("gml:coordinates")
		if coords and coords[0].childNodes[0].nodeValue:
			lon, lat = coords[0].childNodes[0].nodeValue.split(',')
			# Google App Engine data type for storing coordinates 
			return db.GeoPt(lat, lon)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	coords = db.GeoPtProperty()

def top_arts(update = False):
	key = 'top'

	arts = memcache.get(key)
	if arts is None or update:
		logging.error("DB QUERY")
		arts = db.GqlQuery("SELECT * "
							"FROM Art "
							"ORDER BY created DESC " 
							"LIMIT 10")
	#self.render("asciichan_front.html", title=title, art=art, error=error, arts=arts)

	# prevent the running of multiple queries
		arts = list(arts)
		memcache.set(key, arts)
	return arts


class MainPage(Handler):
	def render_front(self, title="", art="", error=""):
		arts = top_arts()

		# find which arts have coords
		points = []
		for a in arts:
			if a.coords:
				points.append(a.coords)
		# points = filter(None, (a.coords for a in arts))


		# if we have any coords, make an image url
		img_url = None
		if points:
			img_url = gmaps_img(points)

		# display the image url
		self.render('asciichan_front.html', title = title, art = art, 
					error = error, arts = arts, img_url = img_url)

	def get(self):
		self.write(repr(get_coords(self.request.remote_addr)))
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Art(title = title, art = art)
			# lookup the user's coordinates from their IP
			coords = get_coords(self.request.remote_addr)
			# if we have coordinated, add them to the Art
			if coords:
				a.coords = coords

			a.put()
			time.sleep(0.3)
			
			#return the query and update the cache
			top_arts(True)
			self.redirect("/unit3/asciichan")
		else:
			error = "we need both a title and some artwork!"
			self.render_front(title=title, art=art, error = error)


application = webapp2.WSGIApplication([("/unit3/asciichan", MainPage)], debug=True)
