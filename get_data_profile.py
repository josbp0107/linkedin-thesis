import json
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from files import Files


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
        elements_education = len(self._driver.find_elements_by_xpath('//section[@id="education-section"]/ul/li'))
        if elements_education == 1:
            university_name = ''
            university_name = (self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//h3').text).lower()
            print(f'Universidad: {university_name}')
            sleep(2)
            if university_name == "corporación universitaria del caribe":
                return True
            else:
                return False
        elif elements_education > 1:
            university_name = []
            for i in range(elements_education):
                university_name.append((self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i+1}]//h3').text).lower())
            print(f'Universidades: {university_name}')
            sleep(3)
            if "corporación universitaria del caribe" in university_name or "Corporación Universitaria del Caribe - CECAR" in university_name:
                return True
            else:
                return False

    # Validate if student contains a degree as System engineer, engineer or others
    def is_student_career(self):
        try:
            career = ['ingeniería de sistemas', 'ingeniería', 'ingeniero','ingeniero de sistemas', 'grado de ingeniería',
                      'grado en ingeniería de sistemas','grado en ingeniería', 'ciclo formativo de grado superior',
                      'ingeniería de software', 'diplomatura','desarrollo de aplicativos moviles', 'grado']
            elements_career = len(self._driver.find_elements_by_xpath('//section[@id="education-section"]/ul/li//div[@class="pv-entity__degree-info"]/p[contains(@class, "pv-entity__degree-name")]/span[@class="pv-entity__comma-item"]'))
            if elements_career == 1:
                career_degree = (self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//div[@class="pv-entity__degree-info"]/p[contains(@class, "pv-entity__degree-name")]/span[@class="pv-entity__comma-item"]').text).lower()
                print(career_degree)
                if career_degree in career:
                    return True
                else:
                    return False
            else:
                count = 0
                career_degree = [(self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i+1}]//div[@class="pv-entity__degree-info"]/p[contains(@class, "pv-entity__degree-name")]/span[@class="pv-entity__comma-item"]').text).lower() for i in range(elements_career)]
                print(f'Carreras: {career_degree}')
                sleep(2)
                for i in career_degree:
                    #career_degree.append((self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i+1}]//div[@class="pv-entity__degree-info"]/p[contains(@class, "pv-entity__degree-name")]/span[@class="pv-entity__comma-item"]').text).lower())
                    if i in career:
                        count += 1
                if count > 0:
                    return True
                else:
                    return False
        except NoSuchElementException as ex:
            print(ex.msg)

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
        # data = {}
        # experience = {}
        # certifications = {}

        list_experience = []
        list_description = []
        list_education = []
        list_certification = []

        elements_experience = len(self._driver.find_elements_by_xpath('//section[@id="experience-section"]/ul/li/section[starts-with(@id, 1) or starts-with(@id, 7) or starts-with(@id, 8)]'))
        elements_experience_extend = len(self._driver.find_elements_by_xpath('//section[@id="experience-section"]/ul/li/section[contains(@id, "ember")]'))
        elements_education = len(self._driver.find_elements_by_xpath('//section[@id="education-section"]/ul/li'))
        elements_certifications = len(self._driver.find_elements_by_xpath('//section[@id="certifications-section"]/ul/li'))

        name = self._driver.find_element_by_xpath('//div/div/h1').text
        if name == '':
            name = self._driver.find_element_by_xpath('//li[@class="inline t-24 t-black t-normal break-words"]').text

        #career = self._driver.find_element_by_xpath('//h2[@class="mt1 t-18 t-black t-normal break-words"]').text
        career = self._driver.find_element_by_xpath('//div[contains(@class, "break-words")]').text
        url_profile = self._driver.current_url
        print(f'Nombre: {name} --- URL: {url_profile}')

        if self.is_student() and self.is_student_career() and self._files.student_exists(name):
            try:
                self.exist_button()

                if elements_experience == 1:
                    experience_position = self._driver.find_element_by_xpath('//section[@id="experience-section"]/ul/li//h3').text
                    experience_company = self._driver.find_element_by_xpath('//section[@id="experience-section"]/ul/li//p[contains(@class, "pv-entity__secondary-title t-14")]').text
                    experience_date = self._driver.find_element_by_xpath('//section[@id="experience-section"]/ul/li//h4[contains(@class, "pv-entity__date-range")]/span[not(@class)]').text

                    experience = {
                        "responsibility": experience_position,
                        "company": experience_company,
                        "duration": experience_date
                    }
                    list_experience.append(experience)
                else:
                    for i in range(elements_experience):
                        experience_position = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]/section[starts-with(@id, 1) or starts-with(@id, 7) or starts-with(@id, 8)]//h3').text
                        experience_company = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]/section[starts-with(@id, 1) or starts-with(@id, 7) or starts-with(@id, 8)]//p[contains(@class, "pv-entity__secondary-title t-14")]').text
                        experience_date = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]/section[starts-with(@id, 1) or starts-with(@id, 7) or starts-with(@id, 8)]//h4[contains(@class, "pv-entity__date-range")]/span[not(@class)]').text

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
                elements_experience_extend_position = len(self._driver.find_elements_by_xpath('//ul[@class="pv-entity__position-group mt2"]/li'))

                if elements_experience_extend == 1:
                    experience_company = self._driver.find_element_by_xpath('//section[@id="experience-section"]/ul/li/section[contains(@id, "ember")]//div[@class="pv-entity__company-summary-info"]/h3/span[not(@class)]').text
                    experience_date = self._driver.find_element_by_xpath('//section[@id="experience-section"]/ul/li/section[contains(@id, "ember")]//div[@class="pv-entity__company-summary-info"]/h4/span[not(@class)]').text
                    for element in range(elements_experience_extend_position):
                        responsibility = self._driver.find_element_by_xpath(f'//ul[@class="pv-entity__position-group mt2"]/li[{element+1}]//h3/span[not (@class)]').text
                        duration = self._driver.find_element_by_xpath(f'//ul[@class="pv-entity__position-group mt2"]/li[{element+1}]//h4/span[not (@class)]').text
                        location = self._driver.find_element_by_xpath(f'//ul[@class="pv-entity__position-group mt2"]/li[{element+1}]//h4[contains(@class, "location")]/span[2]').text
                        description = {
                            "responsibility": responsibility,
                            "duration": duration,
                            "location": location,
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
                    education_name = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//h3').text

                    entity_degree_comma = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//div[@class="pv-entity__degree-info"]/p/span[@class="pv-entity__comma-item"]').text

                    education_description = entity_degree_comma

                    education_time_from = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//p[contains (@class, "pv-entity__dates")]/span/time[1]').text
                    education_time_to = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//p[contains (@class, "pv-entity__dates")]/span/time[2]').text
                    education_time = f'{education_time_from} - {education_time_to}'

                    education = {
                        "institution": education_name,
                        "degree": education_description,
                        "duration": education_time
                    }
                    list_education.append(education)
                else:
                    for i in range(elements_education):
                        education_name = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//h3').text
                        entity_degree_comma = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//div[@class="pv-entity__degree-info"]/p/span[@class="pv-entity__comma-item"]').text

                        education_description = entity_degree_comma

                        education_time_from = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//p[contains (@class, "pv-entity__dates")]/span/time[1]').text
                        education_time_to = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//p[contains (@class, "pv-entity__dates")]/span/time[2]').text
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