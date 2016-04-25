import csv
import re
import sys
import argparse
import dateutil.parser as date_parser
from collections import OrderedDict


class CsvToPostgres:
    delimiter = ','
    quotechar = '"'
    file_name = None
    table_name = None
    table_cols = OrderedDict()

    def __init__(self, options):
        self.file_name = options.f
        self.table_name = options.t

    def create_sql(self):
        fw_txt = open(self.file_name + ".txt", "w")
        with open(self.file_name, 'rb') as csvfile:
            csvr = csv.DictReader(csvfile, delimiter=self.delimiter, quotechar=self.quotechar)
            for col in csvr.fieldnames:
                self.table_cols[col] = {"int_count":0, "string_count":0, "min_len":999999999, "max_len":0, "null_count":0, "not_null_count":0, "datetime_count":0, "float_count":0, "total_count":0}
            for row_num, row in enumerate(csvr):
                row_data = []
                for col in csvr.fieldnames:
                    self.table_cols[col]["total_count"] += 1
                    if row[col] is None or row[col] == "":
                        self.table_cols[col]["null_count"] += 1
                        row_data.append("")
                    else:
                        self.table_cols[col]["not_null_count"] += 1
                        val = re.sub("[\r\n\t]+", " ", row[col].strip())
                        try:
                            if re.match("[/-]", val) is not None or len(val) >= 7:
                                date_parser.parse(val)
                                self.table_cols[col]["datetime_count"] += 1
                        except:
                            pass
                        if re.match(".*[^0-9].*", val):
                            self.table_cols[col]["string_count"] += 1
                        if re.match("[$-]*[0-9,]+[.][0-9].*", val):
                            self.table_cols[col]["float_count"] += 1
                        if re.match("[$-]*[0-9,]", val):
                            self.table_cols[col]["int_count"] += 1
                        if len(val) > self.table_cols[col]["max_len"]:
                            self.table_cols[col]["max_len"] = len(val)
                        if len(val) < self.table_cols[col]["min_len"]:
                            self.table_cols[col]["min_len"] = len(val)
                        row_data.append(val)

                fw_txt.write("\t".join(row_data) + "\n")
                if row_num % 10000 == 0 and row_num > 0:
                    print row_num
        fw_txt.close()

        sql = "DROP TABLE IF EXISTS " + self.table_name + ";\n"
        sql += "CREATE TABLE " + self.table_name + "(\n"
        col_num = 1
        for col in self.table_cols:
            if col_num > 1:
                sql += ", "
            col_name = re.sub("[^a-z0-9]+", " ", col.lower()).strip().replace(" ", "_")
            sql += "\"%s\"" % (col_name, )
            col_data = self.table_cols[col]
            data_type = ""
            for dt in ["int", "float", "string", "datetime", "null"]:
                col_data[dt + "_perc"] = (col_data[dt + "_count"] * 100.0 / col_data["not_null_count"])
            if col_data["datetime_perc"] >= 50:
                data_type = "TIMESTAMP"
            elif col_data["float_perc"] >= 50:
                data_type = "FLOAT"
            elif col_data["int_perc"] >= 50:
                data_type = "SMALLINT"
                if col_data["max_len"] >= 10:
                    data_type = "BIGINT"
                elif col_data["max_len"] >= 5:
                    data_type = "INT"
            elif col_data["string_perc"] >= 50:
                data_type = "VARCHAR(%s)" % (col_data["max_len"], )
                if col_data["max_len"] == col_data["min_len"]:
                    data_type = "CHAR(%s)" % (col_data["min_len"], )
                elif col_data["max_len"] >= 2000:
                    data_type = "TEXT"
            else:
                print self.table_cols[col]
                print ""
            col_num += 1
            sql += " " + data_type + "\n"
        sql += ");\n"

        sql_file_name = "create_" + self.table_name + ".sql"
        fw = open(sql_file_name, "w")
        fw.write(sql)
        fw.close()
        print "File created: %s" % (sql_file_name, )
        print "psql -U postgres -h pm5-10g -d work -f %s" % (sql_file_name, )
        print "cat %s | psql -U postgres -h pm5-10g -d work -c \"SET CLIENT_ENCODING='LATIN1'; COPY %s FROM STDIN NULL ''\"" % (self.file_name + ".txt", self.table_name)

# Custom argument parser class to better handle argument errors
class CustomArgParser(argparse.ArgumentParser):
    def error(self, message):
        print("")
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        print("")
        sys.exit(2)


def main():
    parser = CustomArgParser()
    parser.add_argument('-f', default=None, help='File name to analyze and import', required=True)
    parser.add_argument('-t', default=None, help='Tablename for postgresql', required=True)
    args = parser.parse_args()
    csv2psql = CsvToPostgres(args)
    csv2psql.create_sql()


if __name__ == '__main__':
    sys.exit(main())

