import pandas as pd
import ijson
import csv
from itertools import zip_longest

# File with data scraped
FILE_JSON_DATA = 'dataprocess/dataprueba.json'

# Files with struct
FILE_CSV_EXPERIENCE = 'dataprocess/data_process_experience.csv'
FILE_CSV_EDUCATION = 'dataprocess/data_process_education.csv'
FILE_CSV_CERTIFICATION = 'dataprocess/data_process_certification.csv'

# List to compare
LIST_ING_DESARROLLO_ANALISIS = ['desarrollador', 'ingeniero de sistemas', 'ingeniero', 'sistemas', 'freelance', 'programador', 'web', 'developer', 'software', 'ingenieria']
"""LIST_ADM_BD = ['dato', 'datos']
LIST_ADM_REDES = ['redes', 'administrador de redes', 'administrador', 'soporte de red', 'red']
LIST_ING_SOPORTE = ['soporte', 'mantenimiento']
LIST_ADM_SERIVICIO = ['administrador de servicio', 'servicio', 'informaticos', 'informatico', 'servicio informatico', 'servicios informaticos']
LIST_DEV_SOLUCIONES = ['desarrolador de soluciones', 'soluciones']
DEV_SIS_INFORMATICOS = ['sistemas informaticos', 'desarrollador de soluciones informaticos']
INVESTIGADOR = ['investigador']
GESTOR_PROYECTO = ['gestor', 'gestor de proyectos', 'gestora de proyectos']
"""

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


def data_classification():
    desarrollador, admin_bd, admin_red, soporte, admin_servicio, dev_soluciones, dev_sistemas, investigador, gestor_proyec = [], [], [], [], [], [], [], [], []
    count_desarrollador, count_admin_bd, count_admin_red, count_soporte, count_adm_servicio, count_dev_solucion, count_dev_sistemas, count_investigador, count_gest_proyect = 0, 0, 0, 0, 0, 0, 0, 0, 0
    contador_total = 0
    with open(FILE_CSV_EXPERIENCE, "r", encoding="utf-8") as file_csv:
        reader = csv.DictReader(file_csv)
        for row in reader:
            contador_total += 1
            row_res = row["responsibility"].lower().split(" ")
            if row_res[0] in LIST_ING_DESARROLLO_ANALISIS and not row_res.__contains__("bases"):
                count_desarrollador += 1
                desarrollador.append(row["responsibility"])
            elif row_res.__contains__('dato') or row_res.__contains__('datos') or row_res.__contains__('bases'):
                count_admin_bd += 1
                admin_bd.append(row["responsibility"])
            elif row_res.__contains__('redes') or row_res.__contains__('red'):
                count_admin_red += 1
                admin_red.append(row["responsibility"])
            elif row_res.__contains__('soporte') or row_res.__contains__('tecnico') and not row_res.__contains__("desarrollador") and not row_res.__contains__("desarrollo"):
                count_soporte += 1
                soporte.append(row["responsibility"])
            elif row_res.__contains__('administrador') and not row_res.__contains__("bases") and not row_res.__contains__("red"):
                count_adm_servicio += 1
                admin_servicio.append(row["responsibility"])
            elif row_res.__contains__("soluciones") or row_res.__contains__("arquitecto"):
                count_dev_solucion += 1
                dev_soluciones.append(row["responsibility"])
            elif row_res.__contains__("informatico") or row_res.__contains__("informatica") or row_res.__contains__("sistemas") or row_res.__contains__("webmaster"):
                count_dev_sistemas += 1
                dev_sistemas.append(row["responsibility"])
            elif row_res.__contains__("docente") or row_res.__contains__("investigador"):
                count_investigador += 1
                investigador.append(row["responsibility"])
            elif row_res.__contains__('proyecto') or row_res.__contains__('gestor'):
                count_gest_proyect += 1
                gestor_proyec.append(row["responsibility"])

    print("*"*20, "Total de desarrollador: ", "*"*20)
    print(count_desarrollador)
    print("*"*20, " DESARROLLADOR ", "*"*20)
    print(desarrollador)

    print("*"*20, "Total de administrador de bd: ", "*"*20)
    print(count_admin_bd)
    print("*" * 20, " ADMINISTRADOR DE BASE DE DATOS ", "*" * 20)
    print(admin_bd)

    print("*" * 20, "Total de administrador de red: ", "*" * 20)
    print(count_admin_red)
    print("*" * 20, " ADMINISTRADOR DE REDES ", "*" * 20)
    print(admin_red)

    print("*" * 20, "Total de Soporte: ", "*" * 20)
    print(count_soporte)
    print("*" * 20, " SOPORTE ", "*" * 20)
    print(soporte)

    print("*" * 20, "Total de Administrador de servicios informaticos: ", "*" * 20)
    print(count_adm_servicio)
    print("*" * 20, " ADMINISTRADOR DE SERVICIOS INFORMATICOS", "*" * 20)
    print(admin_servicio)

    print("*" * 20, "Total de Desarrollador de Soluciones Integrales: ", "*" * 20)
    print(count_dev_solucion)
    print("*" * 20, " DESARROLLADOR DE SOLUCIONES INTEGRALES", "*" * 20)
    print(dev_soluciones)

    print("*" * 20, "Total de Desarrollador de Sistemas Informáticos: ", "*" * 20)
    print(count_dev_sistemas)
    print("*" * 20, " DESARROLLADOR DE SISTEMAS INFORMATICOS ", "*" * 20)
    print(dev_sistemas)

    print("*" * 20, "Total de Investigador: ", "*" * 20)
    print(count_investigador)
    print("*" * 20, " INVESTIGADOR ", "*" * 20)
    print(investigador)

    print("*" * 20, "Total de Gestor de proyectos de ingenieria: ", "*" * 20)
    print(count_gest_proyect)
    print("*" * 20, " GESTOR DE PROYECTOS DE INGENIERIA ", "*" * 20)
    print(gestor_proyec)

    print(contador_total)
    print(count_gest_proyect + count_desarrollador + count_admin_bd + count_admin_red + count_soporte + count_adm_servicio + count_dev_solucion + count_dev_sistemas + count_investigador)


if __name__ == '__main__':
    # fact_ident_experience(FILE_CSV_EXPERIENCE)
    # fact_ident_education(FILE_CSV_EDUCATION)
    # fact_ident_certifications(FILE_CSV_CERTIFICATION)
    data_classification()

