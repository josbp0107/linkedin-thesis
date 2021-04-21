import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from get_data_profile import GetDataProfile
from files import Files


class StartBrowser:
    def __init__(self, driver):
        self._driver = driver
        self._url = 'https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&source=hp&ei=GvddYP_FN9KQ5gLItJ_QBw&iflsig=AINFCbYAAAAAYF4FKsf4407zMvunBoCXNyefbhjDpZqA&oq=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&gs_lcp=Cgdnd3Mtd2l6EANQiSFY5kBg5URoBXAAeAGAAZEBiAHqA5IBAzAuNJgBAKABAqABAaoBB2d3cy13aXqwAQA&sclient=gws-wiz&ved=0ahUKEwj_upnenM7vAhVSiFkKHUjaB3oQ4dUDCAc&uact=5'
        self._files = Files()

    # Verifica que el sitio web de google haya cargado de forma correcta
    @property
    def is_loaded(self):
        WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))
        return True

    # call the url
    def open(self):
        self._driver.get(self._url)

    # Method to login in linkedin and start to scraper
    def login(self):

        try:
            self._driver.find_element_by_xpath('//p[starts-with(@class, "join")]/button').click()

            with open('account.txt', 'r') as f:
                line = f.readlines()
                username = line[0]
                password = line[1]

            self._driver.find_element_by_name('session_key').send_keys(username)
            self._driver.find_element_by_name('session_password').send_keys(password)

            sleep(15)

            self._driver.find_element_by_id('login-submit').click()

            self._driver.execute_script("window.history.go(-1)")

        except NoSuchElementException as ex:
            print(ex.msg)

    def profile(self):
        get_data = GetDataProfile(self._driver)
        page = 2

        while page < 3:

            get_data.get_link_name_profile()
            try:
                for profile in range(2):
                    profile_student = self._driver.find_element_by_xpath(f'//*[@id="rso"]/div/div[{profile + 1}]/div/div/div[1]/a')
                    if profile == 0 and page == 2:
                        self._files.create_json_file()
                        profile_student.click()
                        sleep(8)
                        self.login()
                        sleep(7)
                        get_data.get_data_profile()
                        sleep(1)
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)
                    else:
                        profile_student.click()
                        sleep(5)
                        get_data.get_data_profile()
                        sleep(1)
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(5)

                navigator_page = self._driver.find_element_by_link_text(f'{page}')
                navigator_page.click()
                page += 1
            except NoSuchElementException as ex:
                print(ex.msg)