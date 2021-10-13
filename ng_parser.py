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
import git
from git import Repo
from subprocess import Popen, PIPE, STDOUT


tz = pytz.timezone('Europe/Kiev')

#filename = './access.log'

lineformat = re.compile(
    r"""(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] (["]((?P<method>GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""",
    re.IGNORECASE)


def write_csv(data, name='outfile.csv'):
    with open(name, '+w', newline='') as csvfile:
        fieldnames = ["ip", "timestamp", "method", "url", "statuscode", "bytessent", "refferer", "useragent"]
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
    'ip': 'ip',
    'time': 'timestamp',
    'method': 'method',
    'url': 'url',
    'status': 'statuscode',
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
            datadict = data.groupdict()
            ip = datadict["ip"]
            datetimeobj = datetime.strptime(datadict["timestamp"],
                                            "%d/%b/%Y:%H:%M:%S %z")  # Converting string to datetime obj
            method = datadict["method"]
            url = datadict["url"]
            bytessent = int(datadict["bytessent"])
            referrer = datadict["refferer"]
            useragent = datadict["useragent"]
            status = datadict["statuscode"]
        ng_log.append(datadict)
    ng_result = ng_log

    for i in ng_result: #конвертация строки в int
        i['statuscode'] = int(i['statuscode'])
        i['bytessent'] = int(i['bytessent'])
        #print(type(i['statuscode']))

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
                        choices=['ip', 'time', 'method', 'byte', 'url', 'status', 'agent'],
                        help='Select sort mode report')

    parser.add_argument('-t', '--time',
                        #action="count",
                        help="Get time-based report")

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if args.file:
        result = log_parser(args.file, args.sort)

    if args.output in dump_func:
        dump_func[args.output](result)
    else:
        print('For save results, please use argument --outuput select csv or json')


def check_dir():
    dir_in_curdir = filter(os.path.isdir, os.listdir(os.curdir))
    dir_list = list(dir_in_curdir)
    repo_url = os.environ['REPO_URL']
    git_dir = {}

    for i in dir_list:
        if is_git_repo(i):
            git_dir.update({i:True})

    repo_name = repo_url.split('/')[-1][:-4]
    if repo_name in git_dir:
        os.chdir(repo_name)
        repo = git.Git(repo_name)
        p = repo.fetch()
        print(f'We have Git repo')

    else:
        repo = git.Git(repo_name)
        git_clone(repo_name)
        os.chdir(repo_name)
        print('Clon repo')



def git_clone(path):
    repo = git.Git(path)
    gh_token = os.environ['GH_TOKEN']
    repo_url = os.environ['REPO_URL']
    url_clone = "https://" + gh_token + ":x-oauth-basic@github.com" + repo_url
    repo.clone(url_clone)


def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False

def git_push(path):
    repo = git.Git(path)
    p = repo.add('.')
    p = repo.commit(m='my commit message+')
    p = repo.push()

if __name__ == '__main__':

    my_dir = os.path.abspath(os.curdir)
    check_dir()
    my_dir1 = os.path.abspath(os.curdir)
    main()
    git_push(my_dir1)
