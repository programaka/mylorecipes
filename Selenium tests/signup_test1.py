import unittest

from selenium import webdriver
from locators import MainPageLocators

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

#driver.get("http://mylorecipes.appspot.com/blog/signup")
driver.get("http://localhost:8080/blog/signup")


# TO DO: to try unittest, helper functions, and more tests.
class Signup_invalid(unittest.TestCase):
    def tearDown(self):
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("email").clear()

    def test_driver_title(self):
        assert driver.title == "Blog - Signup"

    def test_blank_password(self):
        usernameInputElement = driver.find_element_by_name("username")
        usernameInputElement.send_keys("angel")
        driver.find_element_by_name("submit").click()
        errorMessage = driver.find_element_by_id("blank-password-id")

        assert errorMessage.text == "That wasn't a valid password."
        

    def test_blank_verify(self):
        usernameInputElement = driver.find_element_by_name("username")
        usernameInputElement.send_keys("angel")
        passwordInputElement = driver.find_element_by_name("password")
        passwordInputElement.send_keys("12345")
        driver.find_element_by_name("submit").click()
        errorMessage = driver.find_element_by_id("blank-verify-id")

        assert errorMessage.text == "Your passwords didn't match."

    def test_password_dismatch(self):
        usernameInputElement = driver.find_element_by_name("username")
        usernameInputElement.send_keys("angel")
        passwordInputElement = driver.find_element_by_name("password")
        passwordInputElement.send_keys("12345")
        passwordInputElement = driver.find_element_by_name("verify")
        passwordInputElement.send_keys("123456")
        driver.find_element_by_name("submit").click()
        errorMessage = driver.find_element_by_id("blank-verify-id")

        assert errorMessage.text == "Your passwords didn't match."

    def test_invalid_email(self):
        usernameInputElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME,"username")))
        #usernameInputElement = driver.find_element_by_name("username")
        usernameInputElement.send_keys("angel")
        passwordInputElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME,"password")))
        passwordInputElement.send_keys("12345")
        passwordInputElement = driver.find_element_by_name("verify")
        passwordInputElement.send_keys("12345")
        passwordInputElement = driver.find_element_by_name("email")
        passwordInputElement.send_keys("daria.kgmail.com")
        driver.find_element_by_name("submit").click()
        errorMessage = driver.find_element_by_id("invalid-email-id")

        self.assertEqual(errorMessage.text, "That's not a valid email.")

class Signup_valid(unittest.TestCase):
    def test_valid_inputs(self):
        usernameInputElement = driver.find_element_by_name("username")
        usernameInputElement.send_keys("angel")
        passwordInputElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME,"password")))
        passwordInputElement.send_keys("12345")
        passwordInputElement = driver.find_element_by_name("verify")
        passwordInputElement.send_keys("12345")
        driver.find_element_by_name("submit").click()

        welcomeMessage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"welcome-id")))

        self.assertTrue("Welcome, angel!" in welcomeMessage.text)


if __name__ == '__main__':
    unittest.main()

#try:
#   print driver.title
#finally:
#   driver.quit()