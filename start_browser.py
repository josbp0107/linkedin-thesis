from selenium.common.exceptions import NoSuchElementException
from time import sleep
from get_data_profile import GetDataProfile
from files import Files


class StartBrowser:
    def __init__(self, driver):
        self._driver = driver
        self._url = 'https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&source=hp&ei=GvddYP_FN9KQ5gLItJ_QBw&iflsig=AINFCbYAAAAAYF4FKsf4407zMvunBoCXNyefbhjDpZqA&oq=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&gs_lcp=Cgdnd3Mtd2l6EANQiSFY5kBg5URoBXAAeAGAAZEBiAHqA5IBAzAuNJgBAKABAqABAaoBB2d3cy13aXqwAQA&sclient=gws-wiz&ved=0ahUKEwj_upnenM7vAhVSiFkKHUjaB3oQ4dUDCAc&uact=5'
        self._files = Files()

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
        url_profile = self._driver.current_url
        get_data = GetDataProfile(self._driver)
        elements_profile = len(self._driver.find_elements_by_xpath('//div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div[1]/a'))
        page = 2

        while page < 25:
            get_data.get_link_name_profile()
            sleep(2)
            try:
                for profile in range(elements_profile):
                    profile_student = self._driver.find_element_by_xpath(f'//div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[{profile+1}]/div/div/div[1]/a')
                    if profile == 0 and page == 2:
                        self._files.create_json_file()
                        self._driver.execute_script("arguments[0].click();", profile_student) # Click element profile_student
                        sleep(8)
                        self.login()
                        sleep(7)
                        get_data.get_data_profile()
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)
                    else:
                        self._driver.execute_script("arguments[0].click();", profile_student)  # Click element profile_student
                        if url_profile == 'https://www.linkedin.com/feed/':
                            sleep(3)
                            self._driver.execute_script("window.history.go(-1)")
                        else:
                            sleep(5)
                            get_data.get_data_profile()
                            sleep(1)
                            self._driver.execute_script("window.history.go(-1)")
                            sleep(5)
                navigator_page = self._driver.find_element_by_link_text(f'{page}')
                self._driver.execute_script("arguments[0].click();", navigator_page)
                page += 1
            except NoSuchElementException as ex:
                print(ex.msg)

        self._driver.get('https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&ei=eVy2YL6YG96CwbkP-ImU0Ak&oq=site%3Alinkedin.com%2Fin%2F+AND+%22sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&gs_lcp=Cgdnd3Mtd2l6EANQ9gxY2Q1gwhBoAXAAeACAAYMBiAHpApIBAzAuM5gBAKABAaoBB2d3cy13aXrAAQE&sclient=gws-wiz&ved=0ahUKEwj-uLDk6fbwAhVeQTABHfgEBZoQ4dUDCA4&uact=5')
        page = 2
        while page < 30:
            get_data.get_link_name_profile()
            sleep(2)
            try:
                for profile in range(elements_profile):
                    profile_student = self._driver.find_element_by_xpath(f'//div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[{profile + 1}]/div/div/div[1]/a')
                    self._driver.execute_script("arguments[0].click();", profile_student)
                    sleep(8)
                    get_data.get_data_profile()
                    self._driver.execute_script("window.history.go(-1)")
                    sleep(3)
                navigator_page = self._driver.find_element_by_link_text(f'{page}')
                self._driver.execute_script("arguments[0].click();", navigator_page)
                page += 1
            except NoSuchElementException as ex:
                print(ex.msg)