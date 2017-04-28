import requests
import re
import os
import sys
from utils import download_file, unzip_file

def census_tracts_to_postgresql():
    if "PGSQL_URL" not in os.environ:
        print("Requires setting or environment variable: $PGSQL_URL")
        return

    base_tiger_url = "https://www2.census.gov/geo/tiger/TIGER2016/TRACT/"

    print("Download list of files from: " + base_tiger_url)
    resp = requests.get(base_tiger_url)
    ms = re.findall('href="([^"]*?.zip)"', resp.content)
    for i, m in enumerate(ms):
        data_path = "data/"
        zip_file_name = m
        short_name = zip_file_name.replace(".zip", "")
        print("Process: " + short_name)
        if not os.path.exists(data_path + zip_file_name):
            print("Download %s" % (zip_file_name, ))
            url = "https://www2.census.gov/geo/tiger/TIGER2016/TRACT/" + m
            download_file(url, data_path + zip_file_name)

        print("Unzip: " + data_path + zip_file_name)
        file_names = unzip_file(data_path + zip_file_name)

        create_flags = '-c -I'
        if i > 0:
            create_flags = '-a'
        cmd = "shp2pgsql -D %s -s 4269 %s.shp geo.tract > %s.sql" % (create_flags, data_path + short_name + "/" + short_name, data_path + short_name)
        print("Run shp2pgsql command")
        print(cmd)
        os.system(cmd)

        cmd = "psql %s -f %s.sql" % (os.environ["PGSQL_URL"], data_path + short_name)
        print("Run psql command")
        print(cmd)
        os.system(cmd)

        print("Clean up all files")
        cmd = "rm -rf %s*" % (data_path + short_name, )
        print(cmd)
        os.system(cmd)



def main():
    census_tracts_to_postgresql()


if __name__ == '__main__':
    sys.exit(main())
