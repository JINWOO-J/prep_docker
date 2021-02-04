#!/usr/bin/env python3
from datetime import datetime
from urllib.parse import urlparse
import sys
import os
import time
import argparse
import requests


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
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.ENDC, end="")
                dump(v, nested_level + 1, output)
            else:
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s' % v + bcolors.ENDC,
                      file=output)
        print('%s}' % (def_spacing + nested_level * spacing), file=output)
    elif isinstance(obj, list):
        print('%s[' % (def_spacing + (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print(bcolors.WARNING + '%s%s' % (def_spacing + (nested_level + 1) * spacing, v) + bcolors.ENDC, file=output)
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
    print(f"{get_bcolors(time_string, color='WHITE', bold=True)} {get_bcolors(text, color)}")


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
        o = urlparse(f"http://{url}")
        if o.port:
            url = f"http://{url}"
        else:
            url = f"http://{url}:{port}"
    return url


def get_loopchain_state(ipaddr="localhost", port=os.environ.get('RPC_PORT', 9000)):
    url = append_http(ipaddr, port) + "/api/v1/status/peer"
    return_result = {}
    try:
        session = requests.Session()
        r = session.get(url, verify=False, timeout=10)
        return_result = r.json()
        return_result['prev_time'] = time.time()
        return_result['url'] = url

    except:
        print(f"error while connecting server... {url}")
        return_result = {
            "block_height": 0
        }
    return return_result


def second_to_dayhhmm(input_time):
    day = int(input_time // (24 * 3600))
    input_time = int(input_time % (24 * 3600))
    hour = input_time // 3600
    input_time %= 3600
    minutes = input_time // 60
    input_time %= 60
    seconds = input_time
    return f"{day}d {append_zero(hour)}:{append_zero(minutes)}:{append_zero(seconds)}"


def append_zero(value):
    if value < 10:
        value = f"0{value}"
    return value


def disable_ssl_warnings():
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if __name__ == '__main__':
    disable_ssl_warnings()
    parser = argparse.ArgumentParser(prog='checker')
    parser.add_argument('url', nargs='?', default="localhost:9000")
    parser.add_argument('-n', '--network', type=str, help=f'parent network type (mainnet|testnet|bicon|zicon)', default="mainnet")
    parser.add_argument('-v', '--verbose', action='count', help=f'verbose mode. view level', default=0)

    args = parser.parse_args()

    network_info = {
        "mainnet": "https://ctz.solidwallet.io",
        "testnet": "https://test-ctz.solidwallet.io",
        "bicon": "https://bicon.net.solidwallet.io",
        "zicon": "https://zicon.net.solidwallet.io",
    }

    if os.environ.get('SERVICE', None):
        args.network = os.environ['SERVICE']
    elif os.environ.get('NETWORK_ENV', None):
        args.network = os.environ['NETWORK_ENV']

    if args.network in network_info.keys():
        parent_network_url = network_info.get(args.network)
    else:
        parent_network_url = args.network

    bh_count = 0
    reset_count = 20
    bps_sum = 0
    bps_mean = 0

    prev_blockheight = 0
    prev_total_tx = 0
    prev_time = 0
    blockheight_tps = 0
    total_tx_tps = 0

    print_debug(f"Target peer: {args.url}")
    if args.verbose > 0:
        print_debug(f"Get parent status from {parent_network_url}")

    while True:
        now_dict = get_loopchain_state(args.url)
        now_blockheight = now_dict.get("block_height", 0)
        now_total_tx = now_dict.get("total_tx", 0)
        now_time = now_dict.get("prev_time", 0)

        if now_blockheight:
            time_diff = now_dict.get("prev_time", 0) - prev_time
            blockheight_tps = f"{(now_blockheight - prev_blockheight) / time_diff:.2f}"
            total_tx_tps = f"{(now_total_tx - prev_total_tx) / time_diff:.2f}"

            if prev_blockheight != 0:
                if bh_count >= reset_count:
                    bh_count = 0
                    bps_sum = 0
                    bps_mean = 0

                bh_count += 1
                bps_sum += float(blockheight_tps)
                bps_mean = round(bps_sum / bh_count, 1)

            if args.verbose > 0:
                parent_network_info = get_loopchain_state(parent_network_url, port="")
                left_block = parent_network_info.get("block_height") - now_blockheight
                if float(left_block) > 0 and float(blockheight_tps) > 0 and bps_mean > 0:
                    left_time = second_to_dayhhmm(left_block / bps_mean)
                else:
                    left_time = 0
                    left_block = 0

                left_string = f"left_block: {left_block:,}, left_time: {left_time}"
            else:
                left_string = ""

        if blockheight_tps:
            print_debug(f"BH:{now_blockheight:,}, TX:{now_total_tx:,}, bps:{blockheight_tps}, tps:{total_tx_tps}, " +
                        f"state:{now_dict.get('state')}, nid:{now_dict.get('nid')}, bps_mean:{bps_mean}, {left_string}")

        prev_blockheight = now_blockheight
        prev_total_tx = now_total_tx
        prev_time = now_time
        time.sleep(1)
