import json
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from files import Files


# Scraper without login
class GetDataProfile:
    def __init__(self, driver):
        self._driver = driver
        self._files = Files()

    def get_link_name_profile(self):
        try:
            elements_profile = len(self._driver.find_elements_by_xpath('//div[@id="rso"]/div[starts-with(@class,"g")]//a'))
            for profile in range(elements_profile):
                url_profile = self._driver.find_element_by_xpath(f'//div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[{profile+1}]/div/div/div[1]/a').get_attribute('href')
                get_name = self._driver.find_element_by_xpath(f'//div[@id="rso"]/div[@class="g"][{profile+1}]//div[@class="yuRUbf"]/a/h3').text
                get_name = get_name[:get_name.find("-") - 1]
                print(f'{url_profile} -> {get_name} , {profile + 1}')
            print("#" * 100)
        except NoSuchElementException as ex:
            print(ex.msg)

    # Validate if the student with university education at CECAR
    def is_student(self):
        elements_education = len(self._driver.find_elements_by_xpath('//section[@class="education pp-section"]/ul/li'))
        if elements_education == 1:
            university_name = ''
            university_name = (self._driver.find_element_by_xpath('//section[@class="education pp-section"]/ul/li//h3').text).lower()
            print(f'Universidad: {university_name}')
            sleep(2)
            if university_name == "corporación universitaria del caribe":
                return True
            else:
                return False
        elif elements_education > 1:
            university_name = []
            for i in range(elements_education):
                university_name.append((self._driver.find_element_by_xpath(f'//section[@class="education pp-section"]/ul/li[{i+1}]//h3').text).lower())
                print(university_name)
            print(f'Universidades: {university_name}')
            sleep(3)
            if "corporación universitaria del caribe" in university_name:
                return True
            else:
                return False

    # Validate if student contains a degree as System engineer, engineer or others
    def is_student_career(self):
        career = ['ingeniería de sistemas', 'ingeniería', 'ingeniero', 'desarrollador de software',
                  'ingeniero de sistemas', 'grado de ingeniería', 'grado en ingeniería de sistemas',
                  'grado en ingeniería', 'ciclo formativo de grado superior', 'ingeniería de software']
        elements_career = len(self._driver.find_elements_by_xpath('//section[5]/ul/li/div/h4/span[1]'))
        if elements_career == 1:
            career_degree = ''
            career_degree = self._driver.find_element_by_xpath('//section[5]/ul/li/div/h4/span[1]').text
            career_degree = career_degree.lower()
            print(f'Carrera: {career_degree}')
            if career_degree in career:
                return True
            else:
                return False
        else:
            career_degree = []
            count = 0
            career_degree = [(self._driver.find_element_by_xpath(f'//section[5]/ul/li[{i+1}]/div/h4/span[1]').text).lower() for i in range(elements_career)]
            print(f'Carreras: {career_degree}')
            sleep(1)
            for i in career_degree:
                if i in career:
                    count += 1
            if count > 0:
                return True
            else:
                return False

    # Validate if exist button to more experience section
    def exist_button(self):
        try:
            button_see_more = self._driver.find_element_by_xpath('//section[@id="experience-section"]/div/button')
            button_see_more.click()
            print("#"*30)
            sleep(4)
        except:
            print('Not found Experience section Button')
            print("#" * 30)

    def get_data_profile(self):
        data = {}
        experience = {}
        certifications = {}

        list_experience = []
        list_description = []
        list_education = []
        list_certification = []

        elements_education = len(self._driver.find_elements_by_xpath('//section[@class="education pp-section"]/ul/li'))
        elements_certifications = len(self._driver.find_elements_by_xpath('//section[@class="certifications pp-section"]/ul/li'))

        name = self._driver.find_element_by_xpath('//div/div/h1').text

        career = self._driver.find_element_by_xpath('//div/div/h2').text
        url_profile = self._driver.current_url

        print(f'Nombre: {name} --- URL: {url_profile}')

        if self.is_student() and self.is_student_career() and self._files.student_exists(name):
            # Experience section
            elements_experience_extend = len(self._driver.find_elements_by_xpath('//section[@class="experience pp-section"]/ul/li[@class="experience-group experience-item"]'))
            elements_experience = len(self._driver.find_elements_by_xpath('//section[@class="experience pp-section"]/ul/li'))
            try:
                #self.exist_button()
                if elements_experience == 1:
                    experience_position = self._driver.find_element_by_xpath('//section[@class="experience pp-section"]/ul/li//h3').text
                    experience_company = self._driver.find_element_by_xpath('//section[@class="experience pp-section"]/ul/li//h4').text
                    experience_date = self._driver.find_element_by_xpath('//section[@class="experience pp-section"]/ul/li/div/div/p/span/span').text

                    experience = {
                        "responsibility": experience_position,
                        "company": experience_company,
                        "duration": experience_date
                    }
                    list_experience.append(experience)
                else:
                    for i in range(elements_experience):
                        experience_position = self._driver.find_element_by_xpath(f'//section[@class="experience pp-section"]/ul/li[{i + 1}]//h3').text
                        experience_company = self._driver.find_element_by_xpath(f'//section[@class="experience pp-section"]/ul/li[{i + 1}]//h4').text
                        experience_date = self._driver.find_element_by_xpath(f'//section[@class="experience pp-section"]/ul/li[{i + 1}]/div/div/p/span/span').text

                        experience = {
                            "responsibility": experience_position,
                            "company": experience_company,
                            "duration": experience_date
                        }
                        list_experience.append(experience)
            except NoSuchElementException as ex:
                print(ex.msg)

            # Experience extended format
            try:
                elements_experience_extend_position = len(self._driver.find_elements_by_xpath('//ul[@class="experience-group__positions"]/li'))

                if elements_experience_extend == 1:
                    experience_company = self._driver.find_element_by_xpath('//section[@class="experience pp-section"]/ul/li[@class="experience-group experience-item"]/a/div/div[2]/h4').text
                    experience_date = self._driver.find_element_by_xpath('//section[@class="experience pp-section"]/ul/li[@class="experience-group experience-item"]/a/div/div[2]/p').text
                    for element in range(elements_experience_extend_position):
                        responsibility = self._driver.find_element_by_xpath(f'//ul/li[@class="experience-group experience-item"]/ul[@class="experience-group__positions"]/li[{element+1}]/div/h3').text
                        duration = self._driver.find_element_by_xpath(f'//ul[@class="pv-entity__position-group mt2"]/li[{element+1}]//h4/span[not (@class)]').text
                        location = self._driver.find_element_by_xpath(f'//ul/li[@class="experience-group experience-item"]/ul[@class="experience-group__positions"]/li[{element+1}]/div/div/p//span[@class="date-range__duration"]').text
                        description_position = self._driver.find_element_by_xpath(f'//ul/li[@class="experience-group experience-item"]/ul[@class="experience-group__positions"]/li[{element+1}]/div//p[@class="show-more-less-text__text--less"]')
                        description = {
                            "responsibility": responsibility,
                            "duration": duration,
                            "location": location,
                            "description_position": description_position
                            }

                        list_description.append(description)

                    experience = {
                        "company": experience_company,
                        "duration": experience_date,
                        "description": list_description
                    }
                    list_experience.append(experience)
            except NoSuchElementException as ex:
                print(ex.msg)

            # Section Education
            try:
                if elements_education == 1:
                    education_name = self._driver.find_element_by_xpath('//section[@class="education pp-section"]/ul/li//h3').text
                    education_description = self._driver.find_element_by_xpath('//section[@class="education pp-section"]/ul/li/div/h4/span[1]').text

                    education_time_from = self._driver.find_element_by_xpath('//section[@class="education pp-section"]/ul/li/div/div//time[1]').text
                    education_time_to = self._driver.find_element_by_xpath('//section[@class="education pp-section"]/ul/li/div/div//time[2]').text
                    education_time = f'{education_time_from} - {education_time_to}'

                    education = {
                        "institution": education_name,
                        "degree": education_description,
                        "duration": education_time
                    }
                    list_education.append(education)
                else:
                    for i in range(elements_education):
                        education_name = self._driver.find_element_by_xpath(f'//section[@class="education pp-section"]/ul/li[{i + 1}]//h3').text
                        education_description = self._driver.find_element_by_xpath(f'//section[@class="education pp-section"]/ul/li[{i + 1}]/div/h4/span[1]').text

                        education_time_from = self._driver.find_element_by_xpath(f'//section[@class="education pp-section"]/ul/li[{i + 1}]div/div//time[1]').text
                        education_time_to = self._driver.find_element_by_xpath(f'//section[@class="education pp-section"]/ul/li[{i + 1}]/div/div//time[2]').text
                        education_time = f'{education_time_from} - {education_time_to}'

                        education = {
                            "institution": education_name,
                            "degree": education_description,
                            "duration": education_time
                        }
                        list_education.append(education)
            except NoSuchElementException as ex:
                print(ex.msg)

            # Certifications section
            try:
                if elements_certifications == 1:
                    name_certification = self._driver.find_element_by_xpath('//section[@id="certifications-section"]//h3').text
                    institution_certification = self._driver.find_element_by_xpath('//section[@id="certifications-section"]//p[1]/span[2]').text
                    duration_certification = self._driver.find_element_by_xpath('//section[@id="certifications-section"]//p[2]/span[2]').text
                    certifications = {
                        "certification": name_certification,
                        "institution": institution_certification,
                        "duration": duration_certification
                    }
                    list_certification.append(certifications)
                else:
                    for i in range(elements_certifications):
                        name_certification = self._driver.find_element_by_xpath(f'//section[@id="certifications-section"]/ul/li[{i+1}]//h3').text
                        institution_certification = self._driver.find_element_by_xpath(f'//section[@id="certifications-section"]/ul/li[{i+1}]//p[1]/span[2]').text
                        duration_certification = self._driver.find_element_by_xpath(f'//section[@id="certifications-section"]/ul/li[{i+1}]//p[2]/span[2]').text
                        certifications = {
                            "certification": name_certification,
                            "institution": institution_certification,
                            "duration": duration_certification
                        }
                        list_certification.append(certifications)
            except NoSuchElementException as ex:
                print(ex.msg)

            data = {
                "name": name,
                "career": career,
                "url": url_profile,
                "element_experience": elements_experience + elements_experience_extend,
                "elements_education": elements_education,
                "elements_certification": elements_certifications,
                "work": list_experience,
                "education": list_education,
                "certification": list_certification
            }
            data = json.dumps(data, ensure_ascii=False, indent=4)
            self._files.write_file(data)
            sleep(19)