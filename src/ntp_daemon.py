#!/usr/local/bin/python3
#-*- coding: utf-8 -*-


import re
import os
import sys
import glob
import time
import argparse
import subprocess
import json

from datetime import datetime


def get_parser():
    parser = argparse.ArgumentParser(prog='ntp_daemon.py')
    parser.add_argument('cmd', type=str, choices=['start', 'stop'], help="cmd = [start, stop]")
    parser.add_argument('--check_time', type=int, help=f'Time term[min] (default=30)', default=30)
    return parser.parse_args()


class NTPDaemon:
    def __init__(self, ):
        self.chk = re.compile(r'(0\.\d+)')
        self.date_chk = re.compile(r'(\d{8})')
        self.check_time = os.getenv('HEALTH_CHECK_INTERVAL', 30)
        self.work_dir = '/tmp'
        self.log_dir = self.get_log_path()
        self.ntp_list = [
            "time.google.com",
            "time.cloudflare.com",
            "time.facebook.com",
            "time.apple.com",
            "time.euro.apple.com"
        ]


    def get_log_path(self, ):
        with open('/prep_peer/conf/configure.json', 'r') as f:
            config_dict = json.loads(f.read())
        return config_dict['LOG_FILE_LOCATION']


    def get_log_file(self, ):
        date_list = list()
        for log_file in glob.glob(os.path.join(self.log_dir, 'booting_*.log')):
            date_list.append(int(re.findall(self.date_chk, os.path.basename(log_file))[0]))
        return os.path.join(self.log_dir, f'booting_{sorted(date_list)[-1]}.log')


    def logger(self, msg):
        with open(self.get_log_file(), 'a') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] NTP DAEMON {msg} \n")


    def localtime(self, ):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


    def utctime(self, ):
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


    def sync_time(self, ):
        self.logger("NTP_SYNC Start")
        while True:
            self.logger(f"Local Time : {self.localtime()}")
            self.logger(f"UTC Time   : {self.utctime()}")
            best_ntp = os.getenv('NTP_SERVER', False)
            if best_ntp is False:
                best_ntp = self.compare_ntp()[0]
            self.logger(f"Best NTP is {best_ntp}")
            try:
                os.system(f"ntpdate {best_ntp}")
                self.logger("Time sync success!")
            except Exception as e:
                self.logger("Failed! Check NTP daemon.")
                sys.exit()
            time.sleep(self.check_time * 60)


    def compare_ntp(self, ):
        set_cmd = list()
        cmd = "nmap -sU -p 123 " + " ".join(self.ntp_list) + " | grep up -B 1"
        rs, _ = self.ntp_run(cmd)
        rs_dict = dict()
        for i, r in enumerate(rs):
            for ntp in self.ntp_list:
                if ntp in r:
                    if len(rs) == i+1:
                        break
                    rs_dict[ntp] = float(re.findall(self.chk, rs[i+1])[0])
        self.logger("---NTP Rank---")
        for key, val in rs_dict.items():
            self.logger(f"{key} | {val}")
        self.logger("--------------")
        return sorted(rs_dict.keys(), key=(lambda x: x[1]))


    def ntp_run(self, cmd):
        rs =  subprocess.check_output(cmd, shell=True, encoding='utf-8').split('\n')
        code = subprocess.check_output("echo $?", shell=True, encoding='utf-8').split('\n')
        return rs, code


    def run(self, ):
        self.sync_time()


if __name__ == "__main__":
    time.sleep(5)
    ND = NTPDaemon()
    ND.run()
