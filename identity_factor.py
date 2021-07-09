import ijson
import csv
from itertools import zip_longest


FILECSV = 'data_process.csv'


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

        # for row in responsibility:
        #     print(responsibility[row],",",duration[row],",","Null")


def run():
    file = 'dataprueba.json'

    with open(file, 'rb') as f:
        data_json = ijson.items(f, 'item.work.item.responsibility')

        responsibility = [obj for obj in data_json]

    with open(file, 'rb') as f:
        data_json_extend = ijson.items(f, 'item.work.item.description.item.responsibility')

        responsibility_extends = [obj for obj in data_json_extend]

    return responsibility + responsibility_extends


if __name__ == '__main__':
    fact_ident_experience(FILECSV)

