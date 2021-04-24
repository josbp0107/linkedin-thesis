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
            for profile in range(10):
                url_profile = self._driver.find_element_by_xpath(
                    f'//*[@id="rso"]/div/div[{profile + 1}]/div/div/div[1]/a').get_attribute('href')
                get_name = self._driver.find_element_by_xpath(f'//div[@id="rso"]/div/div[{profile + 1}]//h3').text
                get_name = get_name[:get_name.find("-") - 1]
                print(f'{url_profile} -> {get_name} , {profile + 1}')
            print("#" * 100)
        except NoSuchElementException as ex:
            print(ex.msg)

    # Validate if the student with university education at CECAR
    def is_student(self):
        elements_education = len(self._driver.find_elements_by_xpath('//section[@id="education-section"]/ul/li'))
        if elements_education == 1:
            university_name = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//h3').text
            if university_name == "Corporación Universitaria del Caribe":
                return True
            else:
                return False
        else:
            university_name = [
                self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//h3').text for i
                in range(elements_education)]
            if "Corporación Universitaria del Caribe" in university_name:
                return True
            else:
                return False

    def get_data_profile(self):
        data = {}
        experience = {}
        certifications = {}

        list_experience = []
        list_education = []
        list_certification = []

        elements_experience = len(self._driver.find_elements_by_xpath('//section[@id="experience-section"]/ul/li'))
        elements_education = len(self._driver.find_elements_by_xpath('//section[@id="education-section"]/ul/li'))
        elements_certifications = len(self._driver.find_elements_by_xpath('//section[@id="certifications-section"]/ul/li'))

        name = self._driver.find_element_by_xpath('//li[@class="inline t-24 t-black t-normal break-words"]').text
        career = self._driver.find_element_by_xpath('//h2[@class="mt1 t-18 t-black t-normal break-words"]').text
        url_profile = self._driver.current_url

        if self.is_student():
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
                        experience_position = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]//h3').text
                        experience_company = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]//p[contains(@class, "pv-entity__secondary-title t-14")]').text
                        experience_date = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]//h4[contains(@class, "pv-entity__date-range")]/span[not(@class)]').text

                        experience = {
                            "responsibility": experience_position,
                            "company": experience_company,
                            "duration": experience_date
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
                "element_experience": elements_experience,
                "elements_education": elements_education,
                "elements_certification": elements_certifications,
                "work": list_experience,
                "education": list_education,
                "certification": list_certification
            }
            data = json.dumps(data, ensure_ascii=False, indent=4)
            self._files.write_file(data)
            sleep(18)

