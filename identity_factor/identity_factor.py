import pandas as pd
import ijson
import csv
import xlsxwriter
from itertools import zip_longest

# File with data scraped
FILE_JSON_DATA = 'dataprocess/dataprueba.json'

# Files with struct
FILE_CSV_EXPERIENCE = '../dataprocess/data_process_experience.csv'
FILE_CSV_EDUCATION = '../dataprocess/data_process_education.csv'
FILE_CSV_CERTIFICATION = '../dataprocess/certificaciones.csv'

# List to compare
LIST_ING_DESARROLLO_ANALISIS = ['desarrollador', 'ingeniero de sistemas', 'ingeniero', 'sistemas', 'freelance',
                                'programador', 'web', 'developer', 'software', 'ingenieria', 'implementador', 'android',
                                'movil', 'ingeniera', 'ingeniero', 'analista', 'desarrolladora', 'backend', 'desarrollo',
                                'programadora', 'capacitador', 'react']


def fact_ident_experience(filecsv):
    """
        Extract all data experiences of json, then process it and finally wirte the clean data to csv file
    """

    filename = "../dataprueba.json"

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


def data_classification_experience():
    desarrollador, admin_bd, admin_red, soporte, admin_servicio, dev_soluciones, dev_sistemas, investigador, gestor_proyec, others = [], [], [], [], [], [], [], [], [], []
    count_desarrollador, count_admin_bd, count_admin_red, count_soporte, count_adm_servicio, count_dev_solucion, count_dev_sistemas, count_investigador, count_gest_proyect, count_others = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    contador_total = 0
    with open(FILE_CSV_EXPERIENCE, "r", encoding="utf-8") as file_csv:
        reader = csv.DictReader(file_csv)
        for row in reader:
            row_res = row["responsibility"].lower().split(" ")

            if row_res.__contains__("null"):
                continue

            # Ingeniero de Desarrollo y Análisis de Software.
            if row_res[0] in LIST_ING_DESARROLLO_ANALISIS or row_res.__contains__("consultor") or row_res.__contains__("developer") or row_res.__contains__("analyst") or row_res.__contains__("senior") or row_res.__contains__("engineer") or row_res.__contains__("web") or row_res.__contains__("desarrollo") and not row_res.__contains__("bases"):
                count_desarrollador += 1
                desarrollador.append(row["responsibility"])
            # Administrador de Bases de datos
            elif row_res.__contains__('dato') or row_res.__contains__('datos') or row_res.__contains__('bases'):
                count_admin_bd += 1
                admin_bd.append(row["responsibility"])
            # Administrador redes de computadores
            elif row_res.__contains__('redes') or row_res.__contains__('red') or row_res.__contains__('sysadmin') or row_res.__contains__('systems'):
                count_admin_red += 1
                admin_red.append(row["responsibility"])
            # Ingeniero de Soporte y/o mantenimiento
            elif row_res.__contains__('soporte') or row_res.__contains__('tecnico') or row_res.__contains__('técnico') and not row_res.__contains__("desarrollador") and not row_res.__contains__("desarrollo"):
                count_soporte += 1
                soporte.append(row["responsibility"])
            # Administrador de servicios informáticos
            elif row_res.__contains__('administrador') or row_res.__contains__('coordinador') or row_res.__contains__('seguridad') or row_res.__contains__('security') or row_res.__contains__('sysadmin') or row_res.__contains__('jefe') or row_res.__contains__('servicios') and not row_res.__contains__("bases") and not row_res.__contains__("red"):
                count_adm_servicio += 1
                admin_servicio.append(row["responsibility"])
            # Desarrollador de Soluciones Integrales
            elif row_res.__contains__("soluciones") or row_res.__contains__("arquitecto") or row_res.__contains__("innovación"):
                count_dev_solucion += 1
                dev_soluciones.append(row["responsibility"])
            # Desarrollador de Sistemas Informáticos
            elif row_res.__contains__("informatico") or row_res.__contains__("informatica") or row_res.__contains__("sistemas") or row_res.__contains__("webmaster") or row_res.__contains__("frontend") or row_res.__contains__("software") and not row_res.__contains__('seguridad'):
                count_dev_sistemas += 1
                dev_sistemas.append(row["responsibility"])
            # Investigador
            elif row_res.__contains__("docente") or row_res.__contains__("investigador") or row_res.__contains__("docencia"):
                count_investigador += 1
                investigador.append(row["responsibility"])
            # Gestor de proyectos de ingeniería
            elif row_res.__contains__('proyecto') or row_res.__contains__('gestor') or row_res.__contains__('proyectos'):
                count_gest_proyect += 1
                gestor_proyec.append(row["responsibility"])
            else:
                count_others += 1
                others.append(row["responsibility"])
            contador_total += 1  # Count line of csv file

    #print(contador_total)
    #print(count_others + count_gest_proyect + count_desarrollador + count_admin_bd + count_admin_red + count_soporte + count_adm_servicio + count_dev_solucion + count_dev_sistemas + count_investigador)

    work_profile = desarrollador + admin_bd + admin_red + soporte + admin_servicio + dev_soluciones + dev_sistemas + investigador + gestor_proyec

    # Write all work profile that extract from data_process_experience.csv
    with open('identity_factor.csv', 'w+', encoding='utf-8') as f:
        header = ["responsibility"]
        writer = csv.writer(f)
        d = [work_profile]
        export_data = zip_longest(*d)
        writer.writerow(header)
        writer.writerows(export_data)

    # Write others professional profiles that doesnt belong in the university
    with open('otros.csv', 'w+', encoding='utf-8') as f:
        header = ["responsibility"]
        writer = csv.writer(f)
        d = [others]
        export_data = zip_longest(*d)
        writer.writerow(header)
        writer.writerows(export_data)

    return count_desarrollador, count_admin_bd, count_admin_red, count_soporte, count_adm_servicio, count_dev_solucion, count_dev_sistemas, count_investigador, count_gest_proyect, count_others, contador_total


def data_classification_certification():
    desarrollador, admin_bd, admin_red, soporte, admin_servicio, dev_soluciones, dev_sistemas, investigador, gestor_proyec, others = [], [], [], [], [], [], [], [], [], []
    count_desarrollador, count_admin_bd, count_admin_red, count_soporte, count_adm_servicio, count_dev_solucion, count_dev_sistemas, count_investigador, count_gest_proyect, count_others = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    contador_total = 0
    write_csv = []

    with open(FILE_CSV_CERTIFICATION, "r", encoding="utf-8") as file_csv:
        reader = csv.DictReader(file_csv)
        for row in reader:
            write_csv.append(row["certification"].lower())
            row_res = row["certification"].lower().split(" ")

            # Ingeniero de Desarrollo y Análisis de Software.
            if row_res.__contains__("program") or row_res.__contains__("git") or row_res.__contains__("github") or row_res.__contains__("programming") or row_res.__contains__("javascript") or row_res.__contains__("html") or row_res.__contains__("css") or row_res.__contains__("programación") or row_res.__contains__("programacion") or row_res.__contains__("developer") or row_res.__contains__("web") or row_res.__contains__("java") or row_res.__contains__("engineer") or row_res.__contains__("python") or row_res.__contains__("php") or row_res.__contains__("laravel") or row_res.__contains__("web") or row_res.__contains__("react") or row_res.__contains__("desarrollo") and not row_res.__contains__("bases"):
                count_desarrollador += 1
                desarrollador.append(row["certification"])
            # Administrador de Bases de datos
            elif row_res.__contains__('dato') or row_res.__contains__('datos') or row_res.__contains__('bases') or row_res.__contains__('sql') or row_res.__contains__('postgresql') or row_res.__contains__('mongodb') or row_res.__contains__('mysql') or row_res.__contains__('oracle') and not row_res.__contains__('python'):
                count_admin_bd += 1
                admin_bd.append(row["certification"])
            # Administrador redes de computadores
            elif row_res.__contains__('redes') or row_res.__contains__('networking') or row_res.__contains__('support') or row_res.__contains__('cloud') or row_res.__contains__('red') or row_res.__contains__('sysadmin') or row_res.__contains__('systems') or row_res.__contains__('network'):
                count_admin_red += 1
                admin_red.append(row["certification"])
            # Ingeniero de Soporte y/o mantenimiento
            elif row_res.__contains__('soporte') or row_res.__contains__('tecnico') or row_res.__contains__('técnico') and not row_res.__contains__("desarrollador") and not row_res.__contains__("desarrollo"):
                count_soporte += 1
                soporte.append(row["certification"])
            # Administrador de servicios informáticos
            elif row_res.__contains__('administrador') or row_res.__contains__('devops') or row_res.__contains__('ciberseguridad') or row_res.__contains__('coordinador') or row_res.__contains__('seguridad') or row_res.__contains__('security') or row_res.__contains__('sysadmin') or row_res.__contains__('jefe') or row_res.__contains__('servicios') and not row_res.__contains__("bases") and not row_res.__contains__("red"):
                count_adm_servicio += 1
                admin_servicio.append(row["certification"])
            # Desarrollador de Soluciones Integrales
            elif row_res.__contains__("soluciones") or row_res.__contains__("data") or row_res.__contains__("arquitecto") or row_res.__contains__("innovación") or row_res.__contains__("it") or row_res.__contains__("Infrastructure") or row_res.__contains__("scrum"):
                count_dev_solucion += 1
                dev_soluciones.append(row["certification"])
            # Desarrollador de Sistemas Informáticos
            elif row_res.__contains__("informatico") or row_res.__contains__("wordpress") or row_res.__contains__("node.js") or row_res.__contains__("nokia") or row_res.__contains__("informatica") or row_res.__contains__("sistemas") or row_res.__contains__("webmaster") or row_res.__contains__("frontend") or row_res.__contains__("software") and not row_res.__contains__('seguridad'):
                count_dev_sistemas += 1
                dev_sistemas.append(row["certification"])
            # Investigador
            elif row_res.__contains__("investigador"):
                count_investigador += 1
                investigador.append(row["certification"])
            # Gestor de proyectos de ingeniería
            elif row_res.__contains__('proyecto') or row_res.__contains__('gestor') or row_res.__contains__('proyectos'):
                count_gest_proyect += 1
                gestor_proyec.append(row["certification"])
            else:
                count_others += 1
                others.append(row["certification"])
            contador_total += 1  # Count line of csv file

    # print("*"*20, "Total de desarrollador: ", "*"*20)
    # print(count_desarrollador)
    # print("*"*20, " DESARROLLADOR ", "*"*20)
    # print(desarrollador)

    # print("*"*20, "Total de administrador de bd: ", "*"*20)
    # print(count_admin_bd)
    # print("*" * 20, " ADMINISTRADOR DE BASE DE DATOS ", "*" * 20)
    # print(admin_bd)

    # print("*" * 20, "Total de administrador de red: ", "*" * 20)
    # print(count_admin_red)
    # print("*" * 20, " ADMINISTRADOR DE REDES ", "*" * 20)
    # print(admin_red)

    # print("*" * 20, "Total de Soporte: ", "*" * 20)
    # print(count_soporte)
    # print("*" * 20, " SOPORTE ", "*" * 20)
    # print(soporte)

    # print("*" * 20, "Total de Administrador de servicios informaticos: ", "*" * 20)
    # print(count_adm_servicio)
    # print("*" * 20, " ADMINISTRADOR DE SERVICIOS INFORMATICOS", "*" * 20)
    # print(admin_servicio)

    # print("*" * 20, "Total de Desarrollador de Soluciones Integrales: ", "*" * 20)
    # print(count_dev_solucion)
    # print("*" * 20, " DESARROLLADOR DE SOLUCIONES INTEGRALES", "*" * 20)
    # print(dev_soluciones)

    # print("*" * 20, "Total de Desarrollador de Sistemas Informáticos: ", "*" * 20)
    # print(count_dev_sistemas)
    # print("*" * 20, " DESARROLLADOR DE SISTEMAS INFORMATICOS ", "*" * 20)
    # print(dev_sistemas)

    # print("*" * 20, "Total de Investigador: ", "*" * 20)
    # print(count_investigador)
    # print("*" * 20, " INVESTIGADOR ", "*" * 20)
    # print(investigador)

    # print("*" * 20, "Total de Gestor de proyectos de ingenieria: ", "*" * 20)
    # print(count_gest_proyect)
    # print("*" * 20, " GESTOR DE PROYECTOS DE INGENIERIA ", "*" * 20)
    # print(gestor_proyec)

    # print("*" * 20, "Total de Otros perfiles: ", "*" * 20)
    # print(count_others)
    # print("*" * 20, " OTROS PERFILES ", "*" * 20)
    # print(others)

    # print("")

    # print(contador_total)
    # print("")
    # print(count_others + count_gest_proyect + count_desarrollador + count_admin_bd + count_admin_red + count_soporte + count_adm_servicio + count_dev_solucion + count_dev_sistemas + count_investigador)

    work_profile = desarrollador + admin_bd + admin_red + soporte + admin_servicio + dev_soluciones + dev_sistemas + investigador + gestor_proyec + others
    
    # with open('identity_factor_certification.csv', 'w+', encoding='utf-8') as f:
    #     header = ["certification"]
    #     writer = csv.writer(f)
    #     d = [work_profile]
    #     export_data = zip_longest(*d)
    #     writer.writerow(header)
    #     writer.writerows(export_data)

    return count_desarrollador, count_admin_bd, count_admin_red, count_soporte, count_adm_servicio, count_dev_solucion, count_dev_sistemas, count_investigador, count_gest_proyect, count_others, contador_total


def calculate_percentage():
    percentage_experience, percentage_certification = [], []
    desarrollador, admin_bd, admin_red, soporte, adm_servicio, dev_solucion, dev_sistemas, investigador, gest_proyect, others, contador_total = data_classification_experience()
    c_desarrollador, c_admin_bd, c_admin_red,c_soporte,  c_adm_servicio, c_dev_solucion, c_dev_sistemas, c_investigator, c_gestor_proyect, c_others, c_contador_total = data_classification_certification()
    
    # Calculate percentage of all professional profiles
    # % = (cantidad / total) * 100%

    # Percentage experience section
    print("""
            #################################################
                            EXPERIENCE
            #################################################               
    """)
    
    total = round((desarrollador / contador_total)*100, 2) 
    percentage_experience.append(total)

    total = round((admin_bd / contador_total)*100, 2) 
    percentage_experience.append(total)
    
    total = round((admin_red / contador_total)*100, 2) 
    percentage_experience.append(total)

    total = round((soporte / contador_total)*100, 2) 
    percentage_experience.append(total)

    total = round((adm_servicio / contador_total)*100, 2) 
    percentage_experience.append(total)

    total = round((dev_solucion / contador_total)*100, 2) 
    percentage_experience.append(total)

    total = round((dev_sistemas / contador_total)*100, 2) 
    percentage_experience.append(total)

    total = round((investigador / contador_total)*100, 2) 
    percentage_experience.append(total)

    total = round((gest_proyect / contador_total)*100, 2) 
    percentage_experience.append(total)

    total = round((others / contador_total)*100, 2) 
    percentage_experience.append(total)

    df = pd.DataFrame({'Profiles':['Ingeniero de Desarrollo y Análisis de Software',
                                    'Administrador de Bases de datos',
                                    'Administrador redes de computadores',
                                    'Ingeniero de Soporte y/o mantenimiento',
                                    'Administrador de servicios informáticos',
                                    'Desarrollador de Soluciones Integrales', 
                                    'Desarrollador de Sistemas Informáticos',
                                    'Investigador',
                                    'Gestor de proyectos de ingeniería',
                                    'Otros perfiles'
                                    ],
                        'Percentage':[
                                percentage_experience[0], 
                                percentage_experience[1],
                                percentage_experience[2],
                                percentage_experience[3],
                                percentage_experience[4],
                                percentage_experience[5],
                                percentage_experience[6],
                                percentage_experience[7],
                                percentage_experience[8],
                                percentage_experience[9],
                                
                        ]
    })
    df.to_excel('experience.xlsx', engine='xlsxwriter')
    #print(df)

    print("""
            #################################################
                            CERTIFICATIONS
            #################################################               
    """)

    c_total = round((c_desarrollador / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)

    c_total = round((c_admin_bd / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)
    
    c_total = round((c_admin_red / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)
    
    c_total = round((c_soporte / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)
    
    c_total = round((c_adm_servicio / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)

    c_total = round((c_dev_solucion / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)
    
    c_total = round((c_dev_sistemas / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)

    c_total = round((c_investigator / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)

    c_total = round((c_gestor_proyect / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)

    c_total = round((c_others / c_contador_total)*100, 2) 
    percentage_certification.append(c_total)

    df = pd.DataFrame({'Profiles':['Ingeniero de Desarrollo y Análisis de Software',
                                    'Administrador de Bases de datos',
                                    'Administrador redes de computadores',
                                    'Ingeniero de Soporte y/o mantenimiento',
                                    'Administrador de servicios informáticos',
                                    'Desarrollador de Soluciones Integrales', 
                                    'Desarrollador de Sistemas Informáticos',
                                    'Investigador',
                                    'Gestor de proyectos de ingeniería',
                                    'Otros perfiles'
                                    ],
                        'Percentage':[
                                percentage_certification[0], 
                                percentage_certification[1],
                                percentage_certification[2],
                                percentage_certification[3],
                                percentage_certification[4],
                                percentage_certification[5],
                                percentage_certification[6],
                                percentage_certification[7],
                                percentage_certification[8],
                                percentage_certification[9],
                                
                        ]
    })
    df.to_excel('certifications.xlsx', engine='xlsxwriter')
    #print(df)

    print("""
            #################################################
                            WORKS LOCATION 
            #################################################               
    """)


if __name__ == '__main__':
    # fact_ident_experience(FILE_CSV_EXPERIENCE)
    # fact_ident_education(FILE_CSV_EDUCATION)
    # fact_ident_certifications(FILE_CSV_CERTIFICATION)
    # data_classification_experience()
    #data_classification_certification()
    # Calculate percentage
    calculate_percentage()
