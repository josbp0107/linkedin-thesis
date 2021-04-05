from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep

USERNAME = 'keyex47744@whyflkj.com'
PASSWORD = 'josedavid'


class StartBrowser(object):

    def __init__(self, driver):
        self._driver = driver
        self._url = 'https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&source=hp&ei=GvddYP_FN9KQ5gLItJ_QBw&iflsig=AINFCbYAAAAAYF4FKsf4407zMvunBoCXNyefbhjDpZqA&oq=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&gs_lcp=Cgdnd3Mtd2l6EANQiSFY5kBg5URoBXAAeAGAAZEBiAHqA5IBAzAuNJgBAKABAqABAaoBB2d3cy13aXqwAQA&sclient=gws-wiz&ved=0ahUKEwj_upnenM7vAhVSiFkKHUjaB3oQ4dUDCAc&uact=5'
        # self.url_profile = url_profile
        self.search_locator = 'q'

    # Verifica que el sitio web de google haya cargado de forma correcta
    @property
    def is_loaded(self):
        WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))
        return True

    @property
    def keyword(self):
        input_field = self._driver.find_element_by_name('q')
        return input_field.get_attribute('value')

    # Llamada a la URL
    def open(self):
        self._driver.get(self._url)

    def type_search(self, keyword):
        input_field = self._driver.find_element_by_name(self.search_locator)
        input_field.send_keys(keyword)

    def click_submit(self):
        input_field = self._driver.find_element_by_name(self.search_locator)
        input_field.submit()

    def search(self, keyword):
        self.type_search(keyword)
        self.click_submit()

    def get_link_name_profile(self):
        for profile in range(10):
            get_profile = self._driver.find_element_by_xpath(f'/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div[{profile + 1}]/div/div[1]/a').get_attribute('href')
            get_name = self._driver.find_element_by_xpath(f'/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div[{profile + 1}]/div/div[1]/a/h3').text
            get_name = get_name[:get_name.find("-") - 1]
            print(f'{get_profile} -> {get_name} , {profile + 1}')
        print("#" * 100)

    def login(self):
        try:
            login_page = self._driver.find_element_by_css_selector('body > main > div > div > form.join-form > section > p > button')
            login_page.click()
            user_field = self._driver.find_element_by_name('session_key')
            user_field.send_keys(USERNAME)
            password_field = self._driver.find_element_by_name('session_password')
            password_field.send_keys(PASSWORD)
            button_send = self._driver.find_element_by_id('login-submit')
            button_send.click()
            self._driver.execute_script("window.history.go(-1)")
        except NoSuchElementException as ex:
            print(ex.msg)

    def get_data_profile(self):
        data = {}

        name = self._driver.find_element_by_tag_name('h1').text
        position = self._driver.find_element_by_xpath('//*[@id="main-content"]/section[1]/section/section[1]/div/div[2]/div[1]/h2').text
        experience = self._driver.find_elements_by_xpath('')

    def profile(self):

        page = 2

        while page <= 3:

            self.get_link_name_profile()

            for profile in range(10):
                try:
                    profile_student = self._driver.find_element_by_xpath(f'/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div[{profile + 1}]/div/div[1]/a')
                    profile_student.click()
                    sleep(2)
                    self.login()
                    sleep(3)
                    self._driver.execute_script("window.history.go(-1)")
                    sleep(2)
                except NoSuchElementException:
                    print(f'Error {NoSuchElementException}')

            navigator_page = self._driver.find_element_by_link_text(f'{page}')
            navigator_page.click()
            page += 1