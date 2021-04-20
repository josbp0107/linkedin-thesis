import json
from time import sleep
from selenium.common.exceptions import NoSuchElementException


class GetDataProfile:
    def __init__(self, driver):
        self._driver = driver

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

    def write_file(self, data):
        with open("data.json", "a+", encoding="utf-8") as f:
            f.write(f'{data},')

    def get_data_profile(self):
        data = {}
        experience = {}
        list_experience = []
        list_education = []

        if self.is_student():
            try:
                name = self._driver.find_element_by_xpath('//li[@class="inline t-24 t-black t-normal break-words"]').text
                career = self._driver.find_element_by_xpath('//h2[@class="mt1 t-18 t-black t-normal break-words"]').text
                url_profile = self._driver.current_url
                elements_experience = len(self._driver.find_elements_by_xpath('//section[@id="experience-section"]/ul/li'))
                elements_education = len(self._driver.find_elements_by_xpath('//section[@id="education-section"]/ul/li'))

                for i in range(elements_experience):
                    experience_position = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]//h3').text
                    experience_company = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]//p[contains(@class, "pv-entity__secondary-title t-14")]').text
                    experience_date = self._driver.find_element_by_xpath(f'//section[@id="experience-section"]/ul/li[{i + 1}]//h4[contains(@class, "pv-entity__date-range")]/span[not(@class)]').text

                    experience = {
                        "position": experience_position,
                        "company": experience_company,
                        "time": experience_date
                    }
                    list_experience.append(experience)
            except NoSuchElementException as ex:
                print(ex.msg)

            # Section Education
            try:
                if elements_education == 1:
                    education_name = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//h3').text

                    entity_degree_comma = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//div[@class="pv-entity__degree-info"]/p/span[@class="pv-entity__comma-item"]').text
                    # entity_secondary = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//p[contains(@class, "pv-entity__fos")]/span[@class="pv-entity__comma-item"]').text
                    education_description = entity_degree_comma

                    education_time_from = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//p[contains (@class, "pv-entity__dates")]/span/time[1]').text
                    education_time_to = self._driver.find_element_by_xpath('//section[@id="education-section"]/ul/li//p[contains (@class, "pv-entity__dates")]/span/time[2]').text
                    education_time = f'{education_time_from} - {education_time_to}'

                    education = {
                        "universidad": education_name,
                        "titulo": education_description,
                        "time": education_time
                    }
                    list_education.append(education)
                    sleep(18)
                else:
                    for i in range(elements_education):
                        education_name = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//h3').text
                        entity_degree_comma = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//div[@class="pv-entity__degree-info"]/p/span[@class="pv-entity__comma-item"]').text

                        # entity_secondary = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i+1}]//p[contains(@class, "pv-entity__fos")]/span[@class="pv-entity__comma-item"]').text
                        education_description = entity_degree_comma

                        education_time_from = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//p[contains (@class, "pv-entity__dates")]/span/time[1]').text
                        education_time_to = self._driver.find_element_by_xpath(f'//section[@id="education-section"]/ul/li[{i + 1}]//p[contains (@class, "pv-entity__dates")]/span/time[2]').text
                        education_time = f'{education_time_from} - {education_time_to}'

                        education = {
                            "universidad": education_name,
                            "titulo": education_description,
                            "time": education_time
                        }
                        list_education.append(education)
                    sleep(18)
            except NoSuchElementException as ex:
                print(ex.msg)
            data = {
                "name": name,
                "career": career,
                "url": url_profile,
                "element_experience": elements_experience,
                "elements_education": elements_education,
                "experience": list_experience,
                "education": list_education
            }
            data = json.dumps(data, ensure_ascii=False, indent=4)
            self.write_file(data)
