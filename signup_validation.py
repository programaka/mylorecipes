import re
from google.appengine.ext import db

USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile("^.{3,20}$") 
EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")


def validate_username(username):
    return USER_RE.match(username) and not db.GqlQuery("SELECT * FROM User WHERE username= :1", username).get()
          
def validate_password(password):
    return PASSWORD_RE.match(password)

def validate_email(email):
  if EMAIL_RE.match(email) or email == "":
    return True
  else:
    return False

def username_validation_message(username):
    '''(string) -> string
    
    Return validation message for username input
   
    >>> username_validation_message("")
    "That's not a valid username."
    >>> username_validation_message("d")
    "That's not a valid username."
    >>> username_validation_message("dar")
    ""
    '''
    if validate_username(username):
      return ""
    elif not USER_RE.match(username):
      return "That wasn't a valid username."
    else:
      return "The username already exists"

def password_validation_message(password):
    '''(string) -> string
    
    Return validation message for password input
   
    >>> password_validation_message("")
    "That wasn't a valid password."
    >>> password_validation_message("123")
    ""
    '''
    if validate_password(password):
      return ""
    else:
      return "That wasn't a valid password."

def password_match_message(password1, password2):
    if password1 == password2:
      return ""
    else:
      return "Your passwords didn't match."

def email_validation_message(email):
    if validate_email(email) or email == "":
      return ""
    else:
      return "That's not a valid email."