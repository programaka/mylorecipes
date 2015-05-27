from selenium.webdriver.common.by import By

class MainPageLocators(object):
    USERNAME_INPUT = (By.NAME, 'username')
    PASSWORD_INPUT = (By.NAME, 'password')
    GO_BUTTON = (By.NAME, 'submit')


class SearchResultsPageLocators(object):
    pass