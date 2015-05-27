import cgi
import webapp2

form = """
<form method="post">
    <h2>Enter some text to ROT13:</h2>
    <textarea autofocus name="text" cols="80" rows="10">%(input_text)s</textarea>
    <br>
    <input type="submit">
</form>
""" 

class MainPage(webapp2.RequestHandler):
    def escape_html(self, s):
        return cgi.escape(s, quote = True)

    def write_form(self, text=""):
        self.response.out.write(form % {"input_text": self.escape_html(text)})

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

    def post(self):
        textarea_input=self.request.get("text")
        #self.response.out.write(text)

        rot13text = textarea_input.encode("rot13")
        self.write_form(rot13text)

        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request)


application = webapp2.WSGIApplication([('/unit2/rot13', MainPage)],
                              debug=True)
