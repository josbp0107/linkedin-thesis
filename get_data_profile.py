import json
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from files import Files


# Test branch
class GetDataProfile:
    def __init__(self, driver):
        self._driver = driver
        self._files = Files()

    def get_link_name_profile(self):
        try:
            elements_profile = len(self._driver.find_elements_by_xpath('//div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div[1]/a'))
            for profile in range(elements_profile):
                url_profile = self._driver.find_element_by_xpath(f'//div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[{profile+1}]/div/div/div[1]/a').get_attribute('href')
                get_name = self._driver.find_element_by_xpath(f'//div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[{profile+1}]/div/div/div[1]/a/h3').text
                get_name = get_name[:get_name.find("-") - 1]
                print(f'{url_profile} -> {get_name} , {profile + 1}')
            print("#" * 100)
        except NoSuchElementException as ex:
            print(ex.msg)

    # Read a file csv and validate if the data which pass as arg exist at file
    # data -> data to validate
    # file -> file to read
    # length -> length of element found
    def is_data_exist(self, data, file, length):
        with open(file, "r+", encoding="utf-8") as f:
            count = 0
            line = f.readline()
            line = line.split(',')
            if length == 1:
                if data in line:
                    return True
                else:
                    return False
            else:
                for i in data:
                    if i in line:
                        count += 1
                if count > 0:
                    return True
                else:
                    return False

    # Validates if the student's profile studied at cecar
    def studied_at_university(self):
        elements_education = len(self._driver.find_elements_by_xpath('//section[@id="education-section"]/ul/li'))
        print('Numero de elementos de universidades de educacion encontrados:', elements_education)
        sleep(2)
        if elements_education == 1:
            university_name = ''
            university_name = (self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//h3').text).lower()
            print(f'Universidad: {university_name}')
            sleep(2)
            if self.is_data_exist(university_name, 'static/university.csv', 1):
                return True
            else:
                return False
        elif elements_education > 1:
            university_name = []
            for i in range(elements_education):
                university_name.append((self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//h3').text).lower())
            print(f'Universidades: {university_name}')
            sleep(3)
            if self.is_data_exist(university_name, 'static/university.csv', elements_education):
                return True
            else:
                return False

    # Validates if the student's profile is valid if the student studied at cecar and is studying systems engineering.
    def studied_career_at_university(self):
        try:
            elements_career = len(self._driver.find_elements_by_xpath('//section//section/ul/li/div/div/a/div[2]/div/p[1]/span[2]'))
            print('Numero de elementos de carreras encontrados:', elements_career)
            sleep(2)
            if elements_career == 1:
                career_degree = (self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//div[@class="pv-entity__degree-info"]/p[contains(@class, "pv-entity__degree-name")]/span[@class="pv-entity__comma-item"]').text).lower()
                print(f'Carrera: {career_degree}')
                sleep(2)
                # Is passed by parameters career_degree, file of career with a length of 1
                return self.is_data_exist(career_degree, 'static/career.csv', 1)
            else:
                career_degree = [(self._driver.find_element_by_xpath(f'//section//section/ul/li[{i + 1}]/div/div/a/div[2]/div/p[1]/span[2]').text).lower() for i in range(elements_career)]
                print(f'Carreras: {career_degree}')
                sleep(3)
                return self.is_data_exist(career_degree, 'static/career.csv', elements_career)
        except:
            print('Not found career degree')

    # Validate if the student with university education at CECAR
    def is_student(self):
        try:
            university = ['corporación universitaria del caribe', 'cecar', 'corporación universitaria del caribe cecar',
                          "corporación universitaria del caribe - cecar", 'corporación universitaria del caribe "cecar"']
            elements_education = len(self._driver.find_elements_by_xpath('//section[@id="education-section"]/ul/li'))
            if elements_education == 1:
                university_name = ''
                university_name = (self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//h3').text).lower()
                print(f'Universidad: {university_name}')
                sleep(2)
                if university_name in university:
                    return True
                else:
                    return False
            elif elements_education > 1:
                count = 0
                university_name = []
                for i in range(elements_education):
                    university_name.append((self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i+1}]//h3').text).lower())
                print(f'Universidades: {university_name}')
                sleep(3)
                for i in university_name:
                    if i in university:
                        count += 1
                if count > 0:
                    return True
                else:
                    return False
        except:
            print("Not found university name")

    # Validate if student contains a degree as System engineer, engineer or others
    def is_student_career(self):
        try:
            career = ['ingeniería de sistemas', 'ingeniería', 'ingeniero','ingeniero de sistemas', 'grado de ingeniería',
                      'grado en ingeniería de sistemas','grado en ingeniería', 'ciclo formativo de grado superior',
                      'ingeniería de software', 'ingeniero de software', 'diplomatura','desarrollo de aplicativos moviles',
                      'grado', 'ingeniera de sistemas', 'ingeníera de sistemas','ingenieria de sistemas', 'software enginner',
                      'ingeniera de sistemas (systems engineer)', "engineer's degree", 'ingenieria de software', 'grado en ingeniería']
            elements_career = len(self._driver.find_elements_by_xpath('//section//section/ul/li/div/div/a/div[2]/div/p[1]/span[2]'))
            if elements_career == 1:
                career_degree = (self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//div[@class="pv-entity__degree-info"]/p[contains(@class, "pv-entity__degree-name")]/span[@class="pv-entity__comma-item"]').text).lower()
                print(f'Carrera: {career_degree}')
                if career_degree in career:
                    return True
                else:
                    return False
            else:
                count = 0
                career_degree = [(self._driver.find_element_by_xpath(f'//section//section/ul/li[{i+1}]/div/div/a/div[2]/div/p[1]/span[2]').text).lower() for i in range(elements_career)]
                print(f'Carreras: {career_degree}')
                sleep(2)
                for i in career_degree:
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
            sleep(4)
        except:
            print('Not found Experience section Button')

    # Validate if exist button to more education section
    def exist_button_education(self):
        try:
            button_education = self._driver.find_element_by_xpath('//section[@id="education-section"]//button')
            button_education.click()
            sleep(3)
        except:
            print('Not found Education Section Button')

    # Validate if exist button to more certifications section
    def exist_button_certification(self):
        try:
            button_education = self._driver.find_element_by_xpath('//section[@id="certifications-section"]//button')
            button_education.click()
            sleep(3)
        except:
            print('Not found Certifications Section Button')

    def get_data_profile(self):

        list_experience = []
        list_description = []
        list_education = []
        list_certification = []

        print("*" * 100)
        name = self._driver.find_element_by_xpath('//main/div/section/div[2]/div[2]/div/div[1]/h1').text
        career = self._driver.find_element_by_xpath('//main/div/section/div[2]/div[2]/div/div[2]').text
        url_profile = self._driver.current_url
        print(f'Nombre: {name} --- URL: {url_profile}')

        self.exist_button()
        self.exist_button_education()
        self.exist_button_certification()

        elements_experience = len(self._driver.find_elements_by_xpath('//section[@id="experience-section"]/ul/li/section[starts-with(@id, 1) or starts-with(@id, 2) or starts-with(@id, 3) or starts-with(@id, 4) or starts-with(@id, 5) or starts-with(@id, 6) or starts-with(@id, 7) or starts-with(@id, 8) or starts-with(@id, 9)]'))
        elements_experience_extend = len(self._driver.find_elements_by_xpath('//section[@id="experience-section"]/ul/li/section[contains(@id, "ember")]'))
        elements_education = len(self._driver.find_elements_by_xpath('//section[@id="education-section"]/ul/li'))
        elements_certifications = len(self._driver.find_elements_by_xpath('//section[@id="certifications-section"]/ul/li'))

        if self.studied_at_university() and self.studied_career_at_university() and self._files.student_exists(name):
            # Experience section
            try:
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
                        experience_position = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]/section[starts-with(@id, 1) or starts-with(@id, 2) or starts-with(@id, 3) or starts-with(@id, 4) or starts-with(@id, 5) or starts-with(@id, 6) or starts-with(@id, 7) or starts-with(@id, 8) or starts-with(@id, 9)]//h3').text
                        experience_company = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]/section[starts-with(@id, 1) or starts-with(@id, 2) or starts-with(@id, 3) or starts-with(@id, 4) or starts-with(@id, 5) or starts-with(@id, 6) or starts-with(@id, 7) or starts-with(@id, 8) or starts-with(@id, 9)]//p[contains(@class, "pv-entity__secondary-title t-14")]').text
                        experience_date = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]/section[starts-with(@id, 1) or starts-with(@id, 2) or starts-with(@id, 3) or starts-with(@id, 4) or starts-with(@id, 5) or starts-with(@id, 6) or starts-with(@id, 7) or starts-with(@id, 8) or starts-with(@id, 9)]//h4[contains(@class, "pv-entity__date-range")]/span[not(@class)]').text

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
                        #entity_degree_comma = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//div[@class="pv-entity__degree-info"]/p/span[@class="pv-entity__comma-item"]').text
                        entity_degree_comma = self._driver.find_element_by_xpath(f'//section//section/ul/li[{i+1}]/div/div/a/div[2]/div/p[1]/span[2]').text

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