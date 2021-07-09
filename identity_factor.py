import ijson
import csv
from itertools import zip_longest

# File with data scraped
FILE_JSON_DATA = 'dataprueba.json'

# Files with struct
FILE_CSV_EXPERIENCE = 'data_process_experience.csv'
FILE_CSV_EDUCATION = 'data_process_education.csv'
FILE_CSV_CERTIFICATION = 'data_process_certification.csv'


def fact_ident_experience(filecsv):
    """
        Extract all data experiences of json, then process it and finally wirte the clean data to csv file
    """

    filename = "dataprueba.json"

    header = ["responsibility", "duration", "location"]

    # Extract all data of  key responsibility
    with open(filename, 'rb') as f:
        data_json_responsibility = ijson.items(f, 'item.work.item.responsibility')
        responsibility = [obj for obj in data_json_responsibility]

    # Extract all data of key responsibility but, extend
    with open(filename, 'rb') as f:
        data_json_responsibility_extend = ijson.items(f, 'item.work.item.description.item.responsibility')
        responsibility_extend = [obj for obj in data_json_responsibility_extend]

    # concat list of responsibility and responsibility_extend
    result_responsibility = responsibility + responsibility_extend

    # Extract all data from key duration in key work
    with open(filename, 'rb') as f:
        data_json_duration = ijson.items(f, 'item.work.item.duration')
        duration = [obj for obj in data_json_duration]

    # Extract all data from key duration extended in key work
    with open(filename, 'rb') as f:
        data_json_duration_extend = ijson.items(f, 'item.work.item.description.item.duration')
        duration_extend = [obj for obj in data_json_duration_extend]

    # concat list duration with duration extended
    result_duration = duration + duration_extend

    #
    with open(filename, 'rb') as f:
        data_json_location = ijson.items(f, 'item.work.item.description.item.location')
        location = [obj for obj in data_json_location]

    d = [result_responsibility, result_duration, location]

    export_data = zip_longest(*d, fillvalue='Null')

    with open(filecsv, 'w+', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(export_data)


def fact_ident_education(filecsv):
    """Extract all data education of json, then process it and finally wirte the clean data to csv file called
    data_process_education.csv"""

    header = ['institution', 'degree', 'duration']

    with open(FILE_JSON_DATA, 'rb') as f:
        data_json_institution = ijson.items(f, 'item.education.item.institution')
        institution = [obj for obj in data_json_institution]

    with open(FILE_JSON_DATA, 'rb') as f:
        data_json_degree = ijson.items(f, 'item.education.item.degree')
        degree = [obj for obj in data_json_degree]

    with open(FILE_JSON_DATA, 'rb') as f:
        data_json_duration = ijson.items(f, 'item.education.item.duration')
        duration = [obj for obj in data_json_duration]

    d = [institution, degree, duration]

    export_data = zip_longest(*d, fillvalue='Null')

    with open(filecsv, 'w+', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(export_data)


def fact_ident_certifications(filecsv):
    """Extract all data certifications of json, then process it and finally wirte the clean data to csv file called
    data_process_certification.csv"""

    header = ['certification', 'institution', 'duration']

    with open(FILE_JSON_DATA, 'rb') as f:
        data_json_certification = ijson.items(f, 'item.certification.item.certification')
        certification = [obj for obj in data_json_certification]

    with open(FILE_JSON_DATA, 'rb') as f:
        data_json_institution = ijson.items(f, 'item.certification.item.institution')
        institution = [obj for obj in data_json_institution]

    with open(FILE_JSON_DATA, 'rb') as f:
        data_json_duration = ijson.items(f, 'item.certification.item.duration')
        duration = [obj for obj in data_json_duration]

    d = [certification, institution, duration]

    export_data = zip_longest(*d, fillvalue='Null')

    with open(filecsv, 'w+', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(export_data)


if __name__ == '__main__':
    fact_ident_experience(FILE_CSV_EXPERIENCE)
    fact_ident_education(FILE_CSV_EDUCATION)
    fact_ident_certifications(FILE_CSV_CERTIFICATION)


