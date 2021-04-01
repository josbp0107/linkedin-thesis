import unittest
from selenium import webdriver
from start_browser import StartBrowser

SEARCH = 'site:linkedin.com/in/ AND "ingenieria de sistemas" AND "Corporacion Universitaria del Caribe"'


class GoogleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path=r'drivers/chromedriver.exe')
        cls.driver.maximize_window()

    def test_search(self):

        google = StartBrowser(self.driver, url_profile='')
        google.open()
        #google.search(SEARCH)
        #print(SEARCH)
        google.profile()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)