import unittest
from selenium import webdriver
from start_browser import StartBrowser
from files import Files

SEARCH = 'site:linkedin.com/in/ AND "ingenieria de sistemas" AND "Corporacion Universitaria del Caribe"'


class GoogleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path=r'drivers/chromedriver.exe')
        cls.driver.maximize_window()

    def test_search(self):

        linkedin = StartBrowser(self.driver)
        file = Files()

        file.delete_json()

        linkedin.open()
        linkedin.login()
        linkedin.profile()

        file.close_json_file()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)