import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from get_data_profile import GetDataProfile


class StartBrowser:
    def __init__(self, driver):
        self._driver = driver
        self._url = 'https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&source=hp&ei=GvddYP_FN9KQ5gLItJ_QBw&iflsig=AINFCbYAAAAAYF4FKsf4407zMvunBoCXNyefbhjDpZqA&oq=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&gs_lcp=Cgdnd3Mtd2l6EANQiSFY5kBg5URoBXAAeAGAAZEBiAHqA5IBAzAuNJgBAKABAqABAaoBB2d3cy13aXqwAQA&sclient=gws-wiz&ved=0ahUKEwj_upnenM7vAhVSiFkKHUjaB3oQ4dUDCAc&uact=5'

    # Verifica que el sitio web de google haya cargado de forma correcta
    @property
    def is_loaded(self):
        WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))
        return True

    # Llamada a la URL
    def open(self):
        self._driver.get(self._url)

    def type_search(self, keyword):
        input_field = self._driver.find_element_by_name(self.search_locator)
        input_field.send_keys(keyword)

    def search(self, keyword):
        self.type_search(keyword)
        self.click_submit()

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

        while page <= 3:

            get_data.get_link_name_profile()

            for profile in range(10):
                profile_student = self._driver.find_element_by_xpath(f'//div[@id="rso"]/div/div[{profile+1}]//a')
                try:

                    if profile == 0 and page == 2:
                        profile_student.click()
                        sleep(10)
                        self.login()
                        sleep(7)
                        get_data.get_data_profile()
                        sleep(2)
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)
                    else:
                        profile_student.click()
                        sleep(5)
                        get_data.get_data_profile()
                        sleep(2)
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(5)
                except NoSuchElementException as ex:
                    print(ex.msg)

            navigator_page = self._driver.find_element_by_link_text(f'{page}')
            navigator_page.click()
            page += 1