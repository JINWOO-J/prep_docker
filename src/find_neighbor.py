#!/usr/bin/env python3.7
import asyncio
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer

import json
import re
import requests
import sys
import os
import argparse

from python_hosts.hosts import Hosts, HostsEntry
from random import *

START_TIME = default_timer()
results = defaultdict(list)
TIMEOUT = 5


def disable_ssl_warnings():
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def fetch(session, ipaddr, args):
    base_url = f"http://{ipaddr}:9000/api/v1/avail/peer"  # return http status code
    # with session.get(base_url, verify=False) as response:
    try:
        response = session.get(base_url, verify=False, timeout=TIMEOUT)
        data = response.json()
        if response.status_code != 200:
            # print("FAILURE::{0}".format(ipaddr))
            data = {}

        elapsed = default_timer() - START_TIME
        time_completed_at = "{:5.3f}s".format(elapsed)
        # print(" -- {0:<30} {1:>20}".format(ipaddr, time_completed_at))

    except:
        # print(f"{ipaddr} error")
        data = {}

    if data:
        service_avail = data.get("service_available")
        state = data.get("state")
        # print("{0:<30} {1:>20} {2} {3}".format(ipaddr, elapsed, service_avail, state))
        if service_avail is True and (state == "Vote" or state == "BlockGenerate"):
            # print("{0:<30} {1:>20} {2} {3}".format(ipaddr, elapsed, service_avail, state))
            print(f"-- {ipaddr}, {elapsed}s, {service_avail}, {state}") if args.verbose > 0 else False
            results[elapsed].append(ipaddr)
    return data


async def get_data_asynchronous(args):
    API_SERVER = args.url

    ip_list = []

    if not re.search('^http', API_SERVER):
        API_SERVER = f"http://{API_SERVER}"
    try:
        response = getPRepTerm(API_SERVER)
        if response.status_code == 200:
            result = response.json().get("result").get("preps")
            for peer in result:
                if peer.get("grade") == "0x0":
                    ipaddr = peer.get("p2pEndpoint").split(":")[0]
                    ip_list.append(ipaddr)
        elif response.status_code == 400:
            payload = genParam("getPReps")
            response = post(
                f"{API_SERVER}/api/v3", payload=payload)

            preps_info = response.json()
            main_preps = []
            for peer in preps_info["result"]["preps"]:
                if peer.get("grade") == "0x0":
                    main_preps.append(peer.get("address"))
            ip_list = getPRep(API_SERVER, main_preps)

    except:
        kvPrint("Unexpected error:", sys.exc_info())
        # print("error")
        # ip_list = []
        # raise SystemExit()

    # print("{0:<30} {1:>20}".format("IPaddr", "Completed at"))
    if len(ip_list) > 0:
        with ThreadPoolExecutor(max_workers=10) as executor:
            with requests.Session() as session:
                # Set any session parameters here before calling `fetch`
                loop = asyncio.get_event_loop()
                START_TIME = default_timer()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        fetch,
                        # Allows us to pass in multiple arguments to `fetch`
                        *(session, ipaddr, args)
                    )
                    for ipaddr in ip_list
                ]
                for response in await asyncio.gather(*tasks):
                    pass


def getrepsHash(API_SERVER):
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_getBlock",
        "id": 1234
    }
    response = requests.post(
        f"{API_SERVER}/api/v3", payload=payload)
    LastBlock = response.json()
    return LastBlock['result']['repsHash']


def get_rep_getListByHash(API_SERVER, repsHash, params):
    payload = {
        "jsonrpc": "2.0",
        "method": "rep_getListByHash",
        "id": 1234,
        "params": params

    }
    response = post(
        f"{API_SERVER}/api/v3", payload=payload)
    list = response.json()
    print(list)


def call_api(API_SERVER, method, params, return_key=None):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1234,
        "params": params

    }
    response = post(
        f"{API_SERVER}/api/v3", payload=payload)
    if return_key is not None:
        return_value = find_the_key2(response.json(), return_key)
        # print(return_value)
        if len(return_value) == 1:
            return return_value[0]
    else:
        return_value = response.json()

    return return_value


def getPRepTerm(API_SERVER):
    payload = genParam("getPRepTerm")
    response = post(
        f"{API_SERVER}/api/v3", payload=payload)
    return response


def post(url, payload, elapsed=False):
    data = None
    try:
        data = requests.post(url, json=payload, verify=False, timeout=TIMEOUT)
    except requests.exceptions.HTTPError as errh:
        kvPrint("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        kvPrint("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        kvPrint("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        kvPrint("OOps: Something Else", err)

    if data:
        if data.status_code >= 200:
            print(f"status_code: {data.status_code} , url: {url} , payload: {payload}") if args.verbose > 0 else False

        if elapsed and data.status_code:
            # classdump(data)
            # cprint(f"data.elapsed.total_seconds()= {data.elapsed.total_seconds()}")
            return {"data": data, "elapsed": data.elapsed.total_seconds()}
        else:
            return data


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


def find_the_key(dictionary, findkey):
    findvalue = []
    # print(dictionary)
    if type(dictionary) == tuple:
        for f, v in enumerate(dictionary):
            if type(v) == dict:
                findvalue.append(find_the_key(v, findkey))
                return v

    elif type(dictionary) == list:
        for vvv in enumerate(dictionary):
            if type(vvv) == tuple:
                findvalue = find_the_key(vvv, findkey)
    else:
        for key, value in dictionary.items():
            print(key, type(value))
            if type(value) == dict:
                # print("-----dict")
                findvalue = find_the_key(value, findkey)

            elif type(value) == list:
                findvalue = find_the_key(value, findkey)
            else:
                if key == findkey:
                    findvalue.append(value)
                    return value
                    # findvalue = value
    # print(findvalue)
    return findvalue


def find_the_key2(dictionary, findkey):
    findvalue = []
    for key, value in dictionary.items():
        if type(value) == dict:
            findvalue = find_the_key2(value, findkey)
        else:
            if key == findkey:
                return value

    return findvalue


def getPRep(API_SERVER, main_reps):
    # print(prep_list)
    # repsHash=getrepsHash(API_SERVER)

    repsHash = call_api(API_SERVER, method="icx_getBlock", params={}, return_key="repsHash")
    rep_getListByHash = call_api(API_SERVER, method="rep_getListByHash", params={"repsHash": repsHash}, return_key="result")
    return_list = []
    for info in rep_getListByHash:
        ipaddr = info.get("p2pEndpoint").split(":")[0]
        if info.get("address") in main_reps:
            return_list.append(ipaddr)
    return return_list


def genParam(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "method": "icx_call",
        "id": 1234,
        "params":
            {
                "from": "hx0000000000000000000000000000000000000000",
                "to": "cx0000000000000000000000000000000000000000",
                "dataType": "call",
                "data":
                    {
                        "method": method
                    }
            }
    }
    if params is not None:
        payload['params']['data']['params'] = params
    return payload


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


def json_default(value):
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError('not JSON serializable')


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


def writeJson(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, default=json_default)
    if os.path.exists(filename):
        print("[OK] Write json file -> %s, %s" % (filename, file_size(filename)))


def getListCount(list, count=5):
    return_list = []
    for i, val in enumerate(list):
        return_list.append(f"{list[val][0]}:9000")
        r_i = i + 1
        if r_i >= int(count):
            break
    return return_list


def random_ip(count=2):
    random_list = []
    for i in range(0, count):
        ipaddr = '.'.join([str(randint(1, 255)) for x in range(4)])
        random_list.append(f"{ipaddr}:9000")
    return random_list


def main():
    global args, fastpeer_domains
    disable_ssl_warnings()

    parser = argparse.ArgumentParser(prog='find_neighbor')
    parser.add_argument('url')
    parser.add_argument('count', nargs="?", type=int, default=4)
    parser.add_argument('-v', '--verbose', action='count', help=f'verbose mode. view level', default=0)
    parser.add_argument('-b', '--blockheight', metavar='blockheight',type=int, help=f'blockheight', default=0)
    parser.add_argument('-w', '--writeconfig', action='count', help=f'write to configure json', default=0)
    args = parser.parse_args()

    # fastpeer_domains = ["fastpeer1.icon", "fastpeer2.icon", "fastpeer3.icon", "fastpeer4.icon"]
    fastpeer_domains = [ f"fastpeer{x}.icon" for x in range(0, args.count) ]

    print(f"Arguments={args}") if args.verbose > 0 else False

    configure_json_file = os.environ.get('configure_json', "/prep_peer/conf/configure.json")
    configure_json = openJson(configure_json_file)

    if configure_json.get("CHANNEL_OPTION"):
        if configure_json['CHANNEL_OPTION']['icon_dex'].get("radiostations", None) is None:
            configure_json['CHANNEL_OPTION']['icon_dex']['radiostations'] = []

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(args))
    loop.run_until_complete(future)

    if args.writeconfig:
        # modify configure file
        ip_list = getListCount(results, args.count)
        print(f"List={ip_list}, List_length={len(ip_list)}") if args.verbose > 0 else False
        # if len(ip_list) >= 0:
        default_endpoint = os.environ.get('ENDPOINT_URL', None)
        default_fastpeer = []
        if default_endpoint:
            default_fastpeer.append(default_endpoint)
            for i, fastpeer_domain in enumerate(fastpeer_domains):
                print(f">> fastpeer_domain={fastpeer_domain}, ENDPOINT_URL={default_endpoint}") if args.verbose > 0 else False
                default_fastpeer.append(f"{fastpeer_domain}:9000")
            # default_fastpeer = default_fastpeer + list
            configure_json['CHANNEL_OPTION']['icon_dex']['radiostations'] = default_fastpeer
            writeJson(configure_json_file, configure_json)
            add_alive_peer(ip_list, default_fastpeer)

        else:
            print(f"[ERROR] ENDPOINT_URL not found = {default_endpoint}")
        # else:
        #     print("Can't find neighbor [LIST]")
    else:
        # modify hosts file
        if len(results) > 0:
            ip_list = getListCount(results, len(fastpeer_domains))
            add_alive_peer(ip_list,fastpeer_domains)
        else:
            print("Can't find neighbor [HOSTS]")


def add_alive_peer(ip_list,fastpeer_domains):
    print(f"Alive peer_list={ip_list}, fastpeer_domains={fastpeer_domains}")
    alive_peer = None
    for i, fastpeer_domain in enumerate(fastpeer_domains):
        try:
            fastpeer_info = ip_list[i]
            fastpeer_ip, port = re.findall('([\d.]+)', fastpeer_info)
            if args.blockheight > 0:
                blockhash = call_api(f"http://{fastpeer_ip}:9000", method="icx_getBlockByHeight", params={"height": hex(args.blockheight)}, return_key="block_hash")
                print(f"[ {args.blockheight} BH ] {fastpeer_ip} / {blockhash}")
            else:
                add_host(fastpeer_ip, fastpeer_domain)
                alive_peer = fastpeer_ip
        except:
            if alive_peer is not None:
                add_host(alive_peer, fastpeer_domain)

def split_ip_port(ipaddr):
    ip, port = re.findall('([\d.]+)', ipaddr)
    if ip == None:
        return [ ipaddr ]
    else:
        return [ ip, port ]

def remove_port(ipaddr):
    return ipaddr.split(":")[0]

def add_host(ipaddr, domain):
    hosts = Hosts(path='/etc/hosts')
    if domain == os.environ.get('ENDPOINT_URL'):
        pass
    else:
        print(f"===={domain}") if args.verbose > 0 else False
        domain = remove_port(domain)
        new_entry = HostsEntry(entry_type='ipv4', address=ipaddr, names=[domain])
        # print(new_entry)
        hosts.add([new_entry], force=True, allow_address_duplication=True)
        hosts.write()
        print(f"Modify hosts file -> {ipaddr} {domain}") if args.verbose > 0 else False

if __name__ == '__main__':
    main()
