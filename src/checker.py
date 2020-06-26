#!/usr/bin/env python3.6
import sys, os
import requests, json
import time
from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'

def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    def_spacing = '   '
    if type(obj) == dict:
        print('%s{' % ( def_spacing + (nested_level) * spacing ))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print( bcolors.OKGREEN + '%s%s:' % (def_spacing +(nested_level + 1) * spacing, k) + bcolors.ENDC, end="")
                dump(v, nested_level + 1, output)
            else:
                print( bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s' % v + bcolors.ENDC, file=output)
        print('%s}' % ( def_spacing + nested_level * spacing), file=output)
    elif type(obj) == list:
        print('%s[' % (def_spacing+ (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print ( bcolors.WARNING + '%s%s' % ( def_spacing + (nested_level + 1) * spacing, v) + bcolors.ENDC, file=output)
        print('%s]' % ( def_spacing + (nested_level) * spacing), file=output)
    else:
        print(bcolors.WARNING + '%s%s' % (def_spacing + nested_level * spacing, obj) + bcolors.ENDC)

def get_bcolors(text, color, bold=False, width=None):
    if width and len(text) <= width:
        text = text.center(width, ' ')
    return_text = f"{getattr(bcolors, color)}{text}{bcolors.ENDC}"
    if bold:
        return_text = f"{bcolors.BOLD}{return_text}"
    return str(return_text)

def print_debug(text, color="WHITE"):
    time_string = todaydate('ms')
    print(f"{get_bcolors(time_string, color='WHITE',bold=True)} {get_bcolors(text, color)}")


def todaydate(date_type=None):
    """
    :param date_type:
    :return:
    """
    if date_type == "ms":
        return '[%s]' % datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return '%s' % datetime.now().strftime("%Y%m%d")



def getLoopchainState(ipaddr="localhost", port=os.environ.get('RPC_PORT', 9000)):
    url = f"http://{ipaddr}:{port}/api/v1/status/peer"
    return_result = {}
    try:
        session = requests.Session()
        session.auth = ("guest", "guest")
        r = session.get(url, verify=False, timeout=15)
        return_result=r.json()
    except:
        print("error while connecting server...")
        sys.exit(1)
    # if r.status_code == 200:
    #     return_result=r.json()
    # else:
    #     print(f"status_code error={r.status_code}")
    #     sys.exit(1)
    return return_result


if __name__ == '__main__':
    prev_blockheight = None
    prev_total_tx = None
    while True:
        res = getLoopchainState(sys.argv[1])
        now_blockheight = res.get("block_height")
        now_total_tx = res.get("total_tx")
        print_debug(f"{now_blockheight}/{prev_blockheight}, {now_total_tx}/{prev_total_tx} ")
        prev_blockheight = now_blockheight
        prev_total_tx = now_total_tx
        time.sleep(1)