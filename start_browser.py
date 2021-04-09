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

    def get_link_name_profile(self):
        try:
            for profile in range(10):
                url_profile = self._driver.find_element_by_xpath(f'//div[@id="rso"]/div/div[{profile+1}]//a').get_attribute('href')
                get_name = self._driver.find_element_by_xpath(f'//div[@id="rso"]/div/div[{profile+1}]//h3').text
                get_name = get_name[:get_name.find("-") - 1]
                print(f'{url_profile} -> {get_name} , {profile + 1}')
            print("#" * 100)
        except NoSuchElementException as ex:
            print(ex.msg)

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

    def get_data_profile(self):
        data = {}
        experience = {}
        try:
            name = self._driver.find_element_by_xpath('//li[@class="inline t-24 t-black t-normal break-words"]').text
            career = self._driver.find_element_by_xpath('//h2[@class="mt1 t-18 t-black t-normal break-words"]').text
            elements_experience = len(self._driver.find_elements_by_xpath('//section[@id="experience-section"]/ul/li'))
            for i in range(elements_experience):
                experience_position = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i+1}]//h3').text
                experience_company = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i+1}]//p[contains(@class, "pv-entity__secondary-title t-14")]').text
                experience_date = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i+1}]//h4[contains(@class, "pv-entity__date-range")]/span[not(@class)]').text
                experience = {
                    'position': experience_position,
                    'company': experience_company,
                    'time': experience_date
                }
                print(experience)
            data = {
                'name': name,
                'career': career,
                'element_experience': elements_experience,
                'experience': experience
            }
            parse_json = json.dumps(data, indent=4)
            print(parse_json)

            sleep(18)
        except NoSuchElementException as ex:
            print(ex.msg)

    def profile(self):
        page = 2

        while page <= 3:

            self.get_link_name_profile()

            for profile in range(10):
                profile_student = self._driver.find_element_by_xpath(f'//div[@id="rso"]/div/div[{profile+1}]//a')

                try:
                    if profile == 0:
                        profile_student.click()
                        sleep(5)
                        self.login()
                        sleep(7)
                        self.get_data_profile()
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)
                    else:
                        profile_student.click()
                        sleep(5)
                        self.get_data_profile()
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)

                except NoSuchElementException as ex:
                    print(ex.msg)

            navigator_page = self._driver.find_element_by_link_text(f'{page}')
            navigator_page.click()
            page += 1
