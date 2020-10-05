#!/usr/bin/env python3
import sys
import os
import requests
import json
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
    if isinstance(obj, dict):
        print('%s{' % (def_spacing + (nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing +(nested_level + 1) * spacing, k) + bcolors.ENDC, end="")
                dump(v, nested_level + 1, output)
            else:
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s' % v + bcolors.ENDC, file=output)
        print('%s}' % (def_spacing + nested_level * spacing), file=output)
    elif isinstance(obj, list):
        print('%s[' % (def_spacing+ (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print (bcolors.WARNING + '%s%s' % ( def_spacing + (nested_level + 1) * spacing, v) + bcolors.ENDC, file=output)
        print('%s]' % (def_spacing + (nested_level) * spacing), file=output)
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


def append_http(url, port=None):
    if "https://" in url:
        url = f"{url}"
    elif "http://" not in url:
        url = f"http://{url}:{port}"
    return url


def get_loopchain_state(ipaddr="localhost", port=os.environ.get('RPC_PORT', 9000)):
    url = append_http(ipaddr, port) + "/api/v1/status/peer"
    return_result = {}
    try:
        session = requests.Session()
        session.auth = ("guest", "guest")
        r = session.get(url, verify=False, timeout=10)
        return_result = r.json()
        return_result['prev_time'] = time.time()
        return_result['url'] = url

    except:
        print(f"error while connecting server... {url}")
        # sys.exit(1)
    # if r.status_code == 200:
    #     return_result=r.json()
    # else:
    #     print(f"status_code error={r.status_code}")
    #     sys.exit(1)
    return return_result


def disable_ssl_warnings():
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if __name__ == '__main__':
    disable_ssl_warnings()
    prev_blockheight = 0
    prev_total_tx = 0
    prev_time = 0

    try:
        ipaddr = sys.argv[1]
    except IndexError:
        ipaddr = "localhost"

    while True:
        now_dict = get_loopchain_state(ipaddr)
        now_blockheight = now_dict.get("block_height", 0)
        now_total_tx = now_dict.get("total_tx", 0)
        now_time = now_dict.get("prev_time", 0)

        if now_blockheight:
            time_diff = now_dict.get("prev_time", 0) - prev_time
            blockheight_tps = f"{(now_blockheight - prev_blockheight)/time_diff:.2f}"
            total_tx_tps = f"{(now_total_tx - prev_total_tx)/time_diff:.2f}"
            print_debug(f"BH:{now_blockheight:,}, TX:{now_total_tx:,}, bps:{blockheight_tps}, tps:{total_tx_tps}, " +
                        f"state:{now_dict.get('state')}, nid:{now_dict.get('nid')}, peer_target: {now_dict.get('peer_target')}")

        prev_blockheight = now_blockheight
        prev_total_tx = now_total_tx
        prev_time = now_time

        time.sleep(1)
