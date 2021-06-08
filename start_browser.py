from selenium.common.exceptions import NoSuchElementException
from time import sleep
from get_data_profile import GetDataProfile
from files import Files


# Test branch
class StartBrowser:
    def __init__(self, driver):
        self._driver = driver
        self._files = Files()

    # call the url
    def open(self):
        self._driver.get('https://www.linkedin.com')

    # Method to login in linkedin and start to scraper
    def login(self):
        try:
            with open('account.txt', 'r') as f:
                line = f.readlines()
                username = line[0]
                password = line[1]

            self._driver.find_element_by_name('session_key').send_keys(username)
            self._driver.find_element_by_name('session_password').send_keys(password)
            sleep(14)
            self._driver.find_element_by_xpath('//button[@type="submit"]').click()
            sleep(4)
            self._driver.get('https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&source=hp&ei=GvddYP_FN9KQ5gLItJ_QBw&iflsig=AINFCbYAAAAAYF4FKsf4407zMvunBoCXNyefbhjDpZqA&oq=site%3Alinkedin.com%2Fin%2F+AND+%22ingenieria+de+sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&gs_lcp=Cgdnd3Mtd2l6EANQiSFY5kBg5URoBXAAeAGAAZEBiAHqA5IBAzAuNJgBAKABAqABAaoBB2d3cy13aXqwAQA&sclient=gws-wiz&ved=0ahUKEwj_upnenM7vAhVSiFkKHUjaB3oQ4dUDCAc&uact=5')

        except NoSuchElementException as ex:
            print(ex.msg)

    # Validate if url current is a student
    def is_url_student(self):
        url = self._driver.current_url
        url_content = ['https://www.linkedin.com/feed/?trk=people-guest_profile-result-card_result-card_full-click',
                       'https://www.linkedin.com/feed/']
        sleep(2)
        if url in url_content:
            return False
        else:
            return True

    def profile(self):
        url_current = ['https://www.linkedin.com/feed/?trk=people-guest_profile-result-card_result-card_full-click',
                       'https://www.linkedin.com/'
                       ]
        get_data = GetDataProfile(self._driver)
        elements_profile = len(self._driver.find_elements_by_xpath('//div[@id="rso"]/div[@class="g"]//a'))
        page = 2
        url = ''

        self._files.create_json_file()
        while page < 30:
            get_data.get_link_name_profile()
            sleep(1)
            print("*" * 100)
            print(page)
            print("*" * 100)
            try:
                for profile in range(elements_profile):
                    profile_student = self._driver.find_element_by_xpath(f'//div[@id="rso"]/div[@class="g"][{profile+1}]//a')
                    self._driver.execute_script("arguments[0].click();", profile_student)
                    sleep(6)
                    url = self._driver.current_url
                    print(url)
                    name = len(self._driver.find_elements_by_xpath('//main/div/section/div[2]/div[2]/div/div[1]/h1'))
                    print(f'Contador nombre: {name}')
                    if url in url_current or name == 0:
                        sleep(3)
                        self._driver.execute_script("window.history.go(-1)")
                    else:
                        sleep(6)
                        get_data.get_data_profile()
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)
                navigator_page = self._driver.find_element_by_link_text(f'{page}')
                self._driver.execute_script("arguments[0].click();", navigator_page)
                page += 1
            except NoSuchElementException as ex:
                print(ex.msg)

        self._driver.get('https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F+AND+%22sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&ei=eVy2YL6YG96CwbkP-ImU0Ak&oq=site%3Alinkedin.com%2Fin%2F+AND+%22sistemas%22+AND+%22Corporacion+Universitaria+del+Caribe%22&gs_lcp=Cgdnd3Mtd2l6EANQ9gxY2Q1gwhBoAXAAeACAAYMBiAHpApIBAzAuM5gBAKABAaoBB2d3cy13aXrAAQE&sclient=gws-wiz&ved=0ahUKEwj-uLDk6fbwAhVeQTABHfgEBZoQ4dUDCA4&uact=5')
        page = 2
        while page < 30:
            print("*" * 100)
            print(page)
            print("*" * 100)
            get_data.get_link_name_profile()
            sleep(2)
            try:
                for profile in range(elements_profile):
                    profile_student = self._driver.find_element_by_xpath(f'//div[@id="rso"]/div[@class="g"][{profile+1}]//a')
                    self._driver.execute_script("arguments[0].click();", profile_student)
                    sleep(6)
                    url = self._driver.current_url
                    print(url)
                    name = len(self._driver.find_elements_by_xpath('//main/div/section/div[2]/div[2]/div/div[1]/h1'))
                    print(f'Contador nombre: {name}')
                    if url in url_current or name == 0:
                        sleep(3)
                        self._driver.execute_script("window.history.go(-1)")
                    else:
                        sleep(6)
                        get_data.get_data_profile()
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)
                navigator_page = self._driver.find_element_by_link_text(f'{page}')
                self._driver.execute_script("arguments[0].click();", navigator_page)
                page += 1
            except NoSuchElementException as ex:
                print(ex.msg)

        self._driver.get('https://www.google.com/search?q=site:linkedin.com/in/+AND+%22desarrollador%22+AND+%22Corporacion+Universitaria+del+Caribe%22&ei=7o29YPTPI-Oq5NoPhfe3gAs&start=0&sa=N&ved=2ahUKEwj0_tb3xYTxAhVjFVkFHYX7DbA4KBDy0wN6BAgBEDo&biw=1440&bih=757')
        page = 2
        while page < 30:
            print("*" * 100)
            print(page)
            print("*" * 100)
            get_data.get_link_name_profile()
            sleep(2)
            try:
                for profile in range(elements_profile):
                    profile_student = self._driver.find_element_by_xpath(f'//div[@id="rso"]/div[@class="g"][{profile + 1}]//a')
                    self._driver.execute_script("arguments[0].click();", profile_student)
                    sleep(6)
                    url = self._driver.current_url
                    print(url)
                    name = len(self._driver.find_elements_by_xpath('//main/div/section/div[2]/div[2]/div/div[1]/h1'))
                    print(f'Contador nombre: {name}')
                    if url in url_current or name == 0:
                        sleep(3)
                        self._driver.execute_script("window.history.go(-1)")
                    else:
                        sleep(6)
                        get_data.get_data_profile()
                        self._driver.execute_script("window.history.go(-1)")
                        sleep(2)
                navigator_page = self._driver.find_element_by_link_text(f'{page}')
                self._driver.execute_script("arguments[0].click();", navigator_page)
                page += 1
            except NoSuchElementException as ex:
                print(ex.msg)