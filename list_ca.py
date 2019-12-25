# -*- coding: UTF-8 -*-

import fire
from os import listdir
from os.path import isfile, join
import ssl

import sys
reload(sys)
sys.setdefaultencoding('utf8')


g_issue_field_list = ["countryName","organizationName","organizationalUnitName","commonName"]
g_subject_field_list = ["organizationName","commonName"
    ,"stateOrProvinceName","countryName","emailAddress","localityName"]


def load_ca_list(path,out_file="ca_list.csv"):
    with open(out_file, "w") as myfile:
        myfile.truncate(0)

    output_csv_title(out_file)

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f in onlyfiles:
        try:
            cert_dict = ssl._ssl._test_decode_cert(join(path, f))
        except Exception as e:
            print("Error decoding certificate: {0:}".format(e))
        else:
            output_ca_list(f,cert_dict,out_file)

    pass

def read_issuer(issuer):
    issuer_table = {}
    for field in g_issue_field_list:
        issuer_table[field] = ""
    for i in issuer:
        for j in i:
            issuer_table[j[0]] = j[1]

    return issuer_table

def read_subject(subject):
    subject_table = {}
    for field in g_subject_field_list:
        subject_table[field] = ""

    for i in subject:
        for j in i:
            subject_table[j[0]] = j[1]

    return subject_table
    pass


def output_csv_title(out_file):
    line = ""
    line += "alias"

    for i in g_issue_field_list:
        line +=  "," + "issuer." + i

    for i in g_subject_field_list:
        line +=  "," + "subject." + i

    line += "\n"

    with open(out_file, "a") as myfile:
        myfile.write(line)

def output_ca_list(cert_name,cert_dict,out_file):
    issuer_table = read_issuer(cert_dict['issuer'])
    subject_table = read_subject(cert_dict['subject'])

    line = ""
    line += cert_name

    for i in g_issue_field_list:
        line += "," + "\"" + issuer_table[i] + "\""

    for i in g_subject_field_list:
        line += "," + "\"" + subject_table[i] + "\""

    line += "\n"

    with open(out_file, "a") as myfile:
        myfile.write(line)


    pass



    # line = "{},{}\n".format(cert_name,cn)
    # with open(out_file, "a") as myfile:
    #     myfile.write(line)
    


if __name__ == "__main__":
    fire.Fire(load_ca_list)
    pass