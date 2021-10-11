import argparse
import gzip
import os
import sys
import re
from datetime import datetime
import pytz
import csv
import json
import collections
from git import Repo


tz = pytz.timezone('Europe/Kiev')

#filename = './access.log'

lineformat = re.compile(
    r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""",
    re.IGNORECASE)


def write_csv(data, name='outfile.csv'):
    with open(name, '+w', newline='') as csvfile:
        fieldnames = ["ipaddress", "dateandtime", "url", "statuscode", "bytessent", "refferer", "useragent"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in data:
            writer.writerow(d)


def write_json(data, name='outfile.json'):
    with open(name, '+w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=3)


dump_func = {
    'csv': write_csv,
    'json': write_json
}

sort_mode = {
    'ip': 'ipaddress',
    'date': 'dateandtime',
    'method': 'method',
    'url': 'url',
    'status': 'status',
    'byte': 'bytessent',
    'ref': 'refferer',
    'user': 'useragent'
}

def open_nginx_log(filename):
    try:
        with open(filename, 'r') as f:
            list_of_file = f.readlines()
            return list_of_file
    except Exception as exp:
        print(f'{exp}')
        exit()


def log_parser(filename=str, sort=False, filter=False, time=False):
    list = open_nginx_log(filename)
    ng_log = []
    for l in list:
        data = re.search(lineformat, l)
        if data:
            if data:
                datadict = data.groupdict()
                ip = datadict["ipaddress"]
                datetimeobj = datetime.strptime(datadict["dateandtime"],
                                                "%d/%b/%Y:%H:%M:%S %z")  # Converting string to datetime obj
                url = datadict["url"]
                bytessent = datadict["bytessent"]
                referrer = datadict["refferer"]
                useragent = datadict["useragent"]
                status = datadict["statuscode"]
                method = data.group(6)
        ng_log.append(datadict)
    ng_result = ng_log
    if sort in sort_mode:
        ng_sorted = sorted(ng_log, key=lambda k: k[sort_mode[sort]])
        ng_result = ng_sorted

    return ng_result

def main():
    parser = argparse.ArgumentParser(
        description='using log format: \'$remote_addr - - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"',
        prog='nginx_parse',
        # usage='%(prog)s [options] ',
        epilog='Script for parsing log - %(prog)s')

    parser.add_argument('-f', '--file',
                        # type=str,
                        help="NGINX log file")

    parser.add_argument('-o', '--output',
                        choices=['csv', 'json'],
                        help='Select CSV or JSON format file')

    parser.add_argument('-s', '--sort',
                        choices=['ip', 'url', 'statuscode', 'agent'],
                        help='Select sort mode report')

    parser.add_argument('-t', '--time',
                        #action="count",
                        help="Get time-based report")

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if args.file:
        result = log_parser(args.file)

    if args.output in dump_func:
        dump_func[args.output](result)
    else:
        print('For save results, please use argument --outuput select csv or json')


if __name__ == '__main__':
    main()
