import requests
import os
import sys
import csv
from utils import download_file, unzip_file

# reference
# https://nces.ed.gov/ccd/pubschuniv.asp

def run_cmd(cmd):
    print cmd
    os.system(cmd)


def schools_2015():
    download_file("https://nces.ed.gov/ccd/Data/zip/ccd_sch_029_1415_w_0216601a_txt.zip", "schools-directory.zip")
    file_names = unzip_file("schools-directory.zip")
    file_name = file_names[0]
    run_cmd("psql %s -f schema/schools.school_directory_import_2015.sql" % (os.environ["PGSQL_URL"], ))
    run_cmd("cat %s | psql %s -c \"SET CLIENT_ENCODING='LATIN1'; COPY schools.school_directory_import_2015 FROM STDIN CSV HEADER DELIMITER E'\\t' NULL ''\"" % (file_name, os.environ["PGSQL_URL"]))
    run_cmd("psql %s -f schema/schools.school_directory_2015.sql" % (os.environ["PGSQL_URL"],))
    run_cmd("rm -rf schools-directory*")
    run_cmd("psql %s -c \"DROP TABLE schools.school_directory_import_2015\"" % (os.environ["PGSQL_URL"],))


def schools_2016():
    download_file("https://nces.ed.gov/ccd/Data/zip/ccd_sch_029_1516_txt_prel_tab.zip", "schools-directory.zip")
    file_names = unzip_file("schools-directory.zip")
    file_name = file_names[0]

    with open(file_name,'rb') as tsvin, open(file_name+'.csv', 'wb') as csvout:
        tsvin = csv.reader(tsvin, delimiter='\t')
        csvout = csv.writer(csvout)
        for row in tsvin:
            csvout.writerow(row)

    run_cmd("psql %s -f schema/schools.school_directory_import_2016.sql" % (os.environ["PGSQL_URL"], ))
    run_cmd("cat %s.csv | psql %s -c \"SET CLIENT_ENCODING='LATIN1'; COPY schools.school_directory_import_2016 FROM STDIN CSV HEADER NULL ''\"" % (file_name, os.environ["PGSQL_URL"]))
    run_cmd("psql %s -f schema/schools.school_directory_2016.sql" % (os.environ["PGSQL_URL"],))
    run_cmd("rm -rf schools-directory*")
    run_cmd("psql %s -c \"DROP TABLE schools.school_directory_import_2016\"" % (os.environ["PGSQL_URL"],))


def locations_2015():
    download_file("https://nces.ed.gov/ccd/Data/zip/EDGE_GEOIDS_201415_PUBLIC_SCHOOL_csv.zip", "schools-location.zip")
    file_names = unzip_file("schools-location.zip")
    file_name = file_names[0]

    run_cmd("psql %s -f schema/schools.school_location_import_2015.sql" % (os.environ["PGSQL_URL"], ))
    run_cmd("cat %s | psql %s -c \"SET CLIENT_ENCODING='LATIN1'; COPY schools.school_location_import_2015 FROM STDIN CSV HEADER NULL ''\"" % (file_name, os.environ["PGSQL_URL"]))
    run_cmd("psql %s -f schema/schools.school_location_2015.sql" % (os.environ["PGSQL_URL"],))
    run_cmd("rm -rf schools-location*")
    run_cmd("psql %s -c \"DROP TABLE schools.school_location_import_2015\"" % (os.environ["PGSQL_URL"],))


schools_2015()
schools_2016()
locations_2015()
