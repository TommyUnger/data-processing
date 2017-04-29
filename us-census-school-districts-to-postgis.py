import requests
import re
import os
import time
import sys
import subprocess
from utils import download_file, unzip_file


def census_school_districts_to_postgresql():
    if "PGSQL_URL" not in os.environ:
        print("Requires setting or environment variable: $PGSQL_URL")
        return

    os.system("psql %s -f schema/schools.school_district_import.sql" % (os.environ["PGSQL_URL"],))
    os.system("psql %s -f schema/schools.school_district.sql" % (os.environ["PGSQL_URL"],))

    base_tiger_url = "https://www2.census.gov/geo/tiger/TIGER2016/%s/"
    district_types = ['ELSD', 'SCSD', 'UNSD']
    for district_type in district_types:
        tiger_url = (base_tiger_url % (district_type, ))
        print("Download list of files from: " + tiger_url)
        resp = requests.get(tiger_url)
        ms = re.findall('href="([^"]*?.zip)"', resp.content)
        for i, m in enumerate(ms):
            data_path = "data/"
            zip_file_name = m
            short_name = zip_file_name.replace(".zip", "")
            print("Process: " + short_name)

            if not os.path.exists(data_path + zip_file_name):
                print("Download %s" % (zip_file_name, ))
                url = tiger_url + m
                download_file(url, data_path + zip_file_name)

            print("Unzip: " + data_path + zip_file_name)
            file_names = unzip_file(data_path + zip_file_name)

            create_flags = '-d'
            cmd = "shp2pgsql -D %s -s 4269 %s.shp schools.school_district_import > %s.sql" % (create_flags, data_path + short_name + "/" + short_name, data_path + short_name)
            print("Run shp2pgsql command")
            # print(cmd)
            os.system(cmd)

            cmd = "psql %s -f %s.sql" % (os.environ["PGSQL_URL"], data_path + short_name)
            print("Run psql command")
            # print(cmd)
            os.system(cmd)

            sql_cols = """gid, statefp::SMALLINT, %slea::INT, geoid::INT, name, lsad::INT, 
                        replace(replace(lograde, 'KG', '0'), 'PK', '-1')::SMALLINT, 
                        replace(replace(higrade, 'KG', '0'), 'PK', '-1')::SMALLINT, mtfcc, sdtyp, 
                        funcstat, aland, awater, intptlat, intptlon, geom""" % (district_type.lower())
            cmd = "psql %s -c \"INSERT INTO schools.school_district SELECT %s FROM schools.school_district_import\"" % (os.environ["PGSQL_URL"], sql_cols)
            print("Run psql command")
            # print(cmd)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
            output = process.communicate()
            is_success = 'INSERT 0 ' in output[0]
            print("Success? %s " % (is_success, ))
            if not is_success:
                sys.exit()

            print("Clean up all files")
            cmd = "rm -rf %s*" % (data_path + short_name, )
            # print(cmd)
            os.system(cmd)

            print "------------------------------------------\n"


def main():
    census_school_districts_to_postgresql()


if __name__ == '__main__':
    sys.exit(main())
