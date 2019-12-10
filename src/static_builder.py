#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from termcolor import cprint
import subprocess
import json
import argparse, binascii, sys, os
import timeit
from halo import Halo

# args.default_dir = "/build"

def openJson(filename):
    try:
        json_data = open(filename).read()
    except:
        print("Error Openning json : " + filename)
        json_data = None
    try:
        result = json.loads(json_data)
    except:
        print("Error Decoding json : " + filename)
        result = {}
    return result

def kvPrint(key, value, color="yellow"):
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    key_width = 9
    key_value = 3

    print(bcolors.OKGREEN + "{:>{key_width}} : ".format(key, key_width=key_width) + bcolors.ENDC, end="")
    print(bcolors.WARNING + "{:>{key_value}} ".format(str(value), key_value=key_value) + bcolors.ENDC)

def run_execute(text, cmd, status_check="OK"):
    global args

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    if args.verbose:
        spinner = Halo(text=text, spinner='dots')
        spinner.start()
    start = timeit.default_timer()
    res = subprocess.call(cmd, stdout=None,stderr=None,shell=True)
    end = round(timeit.default_timer() - start , 3)


    if args.verbose:
        if status_check == "OK":
            status_text = f'{text} -> {end}sec'
            if args.verbose:
                status_text = f'{text} / {cmd} -> {end}sec'
            if res != 0:
                spinner.fail(bcolors.FAIL + status_text + bcolors.ENDC)
                cprint(f"[FAIL] {text}","red")
                sys.exit()
            else:
                status_header = bcolors.WARNING + "[DONE]" + bcolors.ENDC
                spinner.succeed(f'{status_header} {status_text}')
        else:
            spinner.succeed(f'[SUCCEED] {text} -> {end}sec')
    else:
        if res != 0:
            cprint(f"[FAIL] {text}","red")
            subprocess.call(cmd, stdout=None, stderr=None, shell=True)



def git_clone(repo_name, url, revision=None):
    #  git - -no-pager  log --pretty = format: '%n%cd %Cred%H%Creset  -%C(yellow)%d%Creset %n  %s %Cgreen(%cr) %C(bold blue)<%an>%Creset %n' - -date = format: '%Y-%m-%d %H:%M:%S' - n 2
    GIT_OPTION = "--no-pager"
    GIT_LOGGER_OPTION = r"--date=format:'%Y-%m-%d %H:%M:%S' --pretty=format:'%n%cd %Cred%H%Creset  -%C(yellow)%d%Creset  %s %Cgreen(%cr) %C(bold blue)<%an>%Creset %n' -n 1"
    # GIT_LOGGER_OPTION = "--pretty=oneline -n 1"
    pwd = os.getcwd()
    repo_dir = f"{args.default_dir}/{repo_name}"
    os.system(f"rm -rf {repo_dir}")
    os.makedirs(repo_dir, exist_ok=True)
    kvPrint("\nRepository Name",repo_name)
    # os.system(f"git clone --quiet -n {url} {repo_dir} ")
    run_execute(f"[git clone] {repo_name} ",f"git clone --quiet -n {url} {repo_dir} ")
    os.chdir(repo_dir)
    revision_res = os.system(f"git checkout --quiet {revision}")
    if revision_res == 0 and revision is not None:
        os.system(f"git checkout --quiet -b {revision}")
        os.system(f"git {GIT_OPTION} log {GIT_LOGGER_OPTION}")
    else:
        cprint(f"Revision not found - {revision} ","red")
        cprint(f"Latest Version -> ","green")
        revision_res = os.system(f"git checkout ;git {GIT_OPTION} log {GIT_LOGGER_OPTION}")

    os.chdir(pwd)


def main():
    global args
    parser = argparse.ArgumentParser(description='Command Line Interface for deploy ')
    parser.add_argument('-v', '--verbose', action='count', help=f'verbose mode. view level', default=1)
    parser.add_argument('-d', '--default-dir', type=str, help=f'working directory', default="/build")
    parser.add_argument('-o', '--output-dir', type=str, help=f'output directory', default="/build/output")

    args = parser.parse_args()

    version_info_file = f'{args.default_dir}/static_version_info.json'
    if os.path.isfile(version_info_file) is False:
        run_execute("static_vesion_info.json not found.", f'cp /src/static_version_info.json {version_info_file}')

    version_info = openJson(f"{version_info_file}")

    for repo_name in version_info.keys():
        url = version_info[repo_name].get('url')
        revision = version_info[repo_name].get('revision')
        cprint(f" {repo_name} ,  {url} , {revision} ")
        git_clone(repo_name, url, revision)
        if repo_name == "icon_rc":
            run_execute(f"-- Build {repo_name}",f"cd {args.default_dir}/{repo_name} ;  curl -O https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz &&" +
                                                "tar zxf go1.12.7.linux-amd64.tar.gz && " +
                                                "rm go1.12.7.linux-amd64.tar.gz && "+
                                                "rm -rf /usr/local/go; mv go /usr/local/  && "+
                                                f"git checkout {revision}  && "+
                                                "make linux && "+
                                                f"make install DST_DIR={args.output_dir} && "+
                                                "cd .. && rm -rf rewardcalculator /usr/local/go ;")
        else:
            run_execute(f"Build {repo_name}", f"cd {args.default_dir}/{repo_name} &&  " +
                        f"pip3 install -r requirements.txt;export VERSION={revision} &&" +
                        f"python3 setup.py bdist_wheel --dist-dir {args.output_dir}")


def banner():
    print("="*57)
    print(' _____ _____ _____ ____  _____ _____    __    _____ _____')
    print('|   __|   __|   | |    \|     |   __|  |  |  |     |   __|')
    print('|__   |   __| | | |  |  | | | |   __|  |  |__|  |  |  |  |')
    print('|_____|_____|_|___|____/|_|_|_|_____|  |_____|_____|_____|')
    print("="*57)

    print('____                 ___       __')
    print("/\  _`\           __ /\_ \     /\ \\")
    print('\ \ \L\ \  __  __/\_\\//\ \    \_\ \     __   _ __')
    print(' \ \  _ <\'/\ \/\ \/\ \ \ \ \   /\'_` \  /\'__`\/\`\'__ \\')
    print('  \ \ \L\ \ \ \_\ \ \ \ \_\ \_/\ \L\ \/\  __/\ \ \/')
    print('   \ \____/\ \____/\ \_\/\____\ \___,_\ \____\\ \_ \\')
    print('    \/___/  \/___/  \/_/\/____/\/__,_ /\/____/ \/_/')

    print("")
    print("\t\t\t\t   by JINWOO")
    print("="*57)

if __name__ == '__main__':
    banner()
    main()

    for dirpath, dirnames, filenames in os.walk(args.output_dir):
        print("\n\t--- output files---")
        for dirname in dirnames:
            print ("\t", f"dirname")
        for filename in filenames:
            print("\t", f"{dirpath}/{filename}")