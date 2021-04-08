import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep


class StartBrowser(object):
    def __init__(self, driver):
        self._driver = driver
        self._url = 'https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&source=hp&ei=GvddYP_FN9KQ5gLItJ_QBw&iflsig=AINFCbYAAAAAYF4FKsf4407zMvunBoCXNyefbhjDpZqA&oq=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&gs_lcp=Cgdnd3Mtd2l6EANQiSFY5kBg5URoBXAAeAGAAZEBiAHqA5IBAzAuNJgBAKABAqABAaoBB2d3cy13aXqwAQA&sclient=gws-wiz&ved=0ahUKEwj_upnenM7vAhVSiFkKHUjaB3oQ4dUDCAc&uact=5'
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
            self._driver.find_element_by_css_selector('body > main > div > div > form.join-form > section > p > button').click()

            with open('account.txt', 'r') as f:
                line = f.readlines()
                username = line[0]
                password = line[1]

            self._driver.find_element_by_name('session_key').send_keys(username)
            self._driver.find_element_by_name('session_password').send_keys(password)

            sleep(3)

            self._driver.find_element_by_id('login-submit').click()

            self._driver.execute_script("window.history.go(-1)")

        except NoSuchElementException as ex:
            print(ex.msg)

    def get_data_profile(self):
        data = {}
        experience = {}
        sleep(10)
        try:
            name = self._driver.find_element_by_xpath('//li[@class="inline t-24 t-black t-normal break-words"]').text
            career = self._driver.find_element_by_xpath('//h2[@class="mt1 t-18 t-black t-normal break-words"]').text

            # experience_position = self._driver.find_elements_by_css_selector('#main-content > section.core-rail > section > section.experience.pp-section > ul > li:nth-child(1) > div > h3').text
            # experience_company = self._driver.find_elements_by_css_selector('#main-content > section.core-rail > section > section.experience.pp-section > ul > li:nth-child(1) > div > h4 > a').text
            # experience_date = self._driver.find_elements_by_css_selector('#main-content > section.core-rail > section > section.experience.pp-section > ul > li:nth-child(1) > div > div > p > span').text
            # experience = {
            #     'position': experience_position,
            #     'company': experience_company,
            #     'time': experience_date
            # }
            data = {
                'name': name,
                'career': career
                # 'experience': experience
            }
            parse_json = json.dumps(data, indent=4)
            print(parse_json)

            sleep(4)
        except NoSuchElementException as ex:
            print(ex.msg)

    def profile(self):
        page = 2

        while page <= 3:

            self.get_link_name_profile()

            for profile in range(10):
                profile_student = self._driver.find_element_by_xpath(f'/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div[{profile + 1}]/div/div[1]/a')

                try:
                    if profile == 0:
                        profile_student.click()
                        sleep(5)
                        self.login()
                        sleep(7)
                        self.get_data_profile()
                        sleep(2)
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)
                    else:
                        profile_student.click()
                        sleep(5)
                        self.get_data_profile()
                        sleep(2)
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)

                except NoSuchElementException as ex:
                    print(ex.msg)

            navigator_page = self._driver.find_element_by_link_text(f'{page}')
            navigator_page.click()
            page += 1
