# webapp2 - a lightweight framework that allows you quickly
# build simple web applications for the Python 2.7 runtime.
import webapp2
import signup_validation

form = """
<form method="post">
	<h1>Signup</h1>

	<label>
		Username
		<input type="text" name="username" value="%(username_input)s">
	</label>
    <div style="color: red">%(username_error)s</div>
    <br>

	<label>
		Password
		<input type="text" name="password" value="%(password_input)s">
	</label>
    <div style="color: red">%(password_error)s</div>
    <br>

	<label>
		Verify Password
		<input type="text" name="verify" value="%(verify_password_input)s">
	</label>
    <div style="color: red">%(verify_error)s</div>
    <br>

    <label>
        Email (optional)
        <input type="text" name="email" value="%(email_input)s">
    </label>
    <div style="color: red">%(email_error)s</div>
	<br>
	<input type="submit" name="submit">
</form>
"""


class MainPage(webapp2.RequestHandler):
    def write_form(self, username="", username_error="",
                        password="", password_error="",
                        verify="", verify_error="",
                        email="", email_error=""):
    	self.response.out.write(form % {"username_input": username,
                                        "username_error": username_error,
    									"password_input": password,
                                        "password_error": password_error,
    									"verify_password_input": verify,
                                        "verify_error": verify_error,
    									"email_input": email,
                                        "email_error": email_error})

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password1 = self.request.get('password')
        password2 = self.request.get('verify')
        email = self.request.get('email')

        
        valid_username = signup_validation.validate_username(username)
        valid_password = signup_validation.validate_password(password1)
        passwords_match = (password1 == password2)
        valid_email = signup_validation.validate_email(email)

        if not (valid_username and valid_password and passwords_match and valid_email):
            self.write_form(username, signup_validation.username_validation_message(username),
                        password1, signup_validation.password_validation_message(password1),
                        password2, signup_validation.password_match_message(password1, password2),
                        email, signup_validation.email_validation_message(email))
        else:
            self.redirect("/unit2/welcome?username="+username)

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
            username=self.request.get('username')
            self.response.out.write("Welcome, "+username+"!")

application = webapp2.WSGIApplication([('/unit2/signup', MainPage),
                                        ('/unit2/welcome', WelcomeHandler)
                                        ],
                              debug=True)