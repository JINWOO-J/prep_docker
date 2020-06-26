#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys
import os
import io
import argparse
import json
import re
import socket
import time
from random import randint
from datetime import datetime
from python_hosts.hosts import Hosts, HostsEntry
from halo import Halo
import pycurl

CURL_TIME_ATTRS = ('NAMELOOKUP_TIME', 'CONNECT_TIME', 'APPCONNECT_TIME',
                   'PRETRANSFER_TIME', 'REDIRECT_TIME', 'STARTTRANSFER_TIME', 'TOTAL_TIME')

TIMEOUT = 2

def todaydate(date_type=None):
    """
    :param date_type:
    :return:
    """
    if date_type == "ms":
        return '[%s]' % datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return '%s' % datetime.now().strftime("%Y%m%d")


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def json(self):
        return {}


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


def get_bcolors(text, color, bold=False, width=None):
    if width and len(text) <= width:
        text = text.center(width, ' ')
    return_text = f"{getattr(bcolors, color)}{text}{bcolors.ENDC}"
    if bold:
        return_text = f"{bcolors.BOLD}{return_text}"
    return str(return_text)


def print_debug(text, color="WHITE"):
    if args.verbose > 0:
        time_string = todaydate('ms')
        print(f"{get_bcolors(time_string, color='WHITE',bold=True)} {get_bcolors(text, color)}")


def kvPrint(key, value, color="yellow"):
    key_width = 9
    key_value = 3
    print(bcolors.OKGREEN + "{:>{key_width}} : ".format(key, key_width=key_width) + bcolors.ENDC, end="")
    print(bcolors.WARNING + "{:>{key_value}} ".format(str(value), key_value=key_value) + bcolors.ENDC)


def classdump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            print(bcolors.OKGREEN + f"obj.{attr} = " + bcolors.WARNING + f"{value}" + bcolors.ENDC)


def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    def_spacing = '   '
    if type(obj) == dict:
        print('%s{' % (def_spacing + (nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(bcolors.OKGREEN + '%s%s:' %
                       (def_spacing +(nested_level + 1) * spacing, k) + bcolors.ENDC, end="")
                dump(v, nested_level + 1, output)
            else:
                print( bcolors.OKGREEN + '%s%s:' %
                       (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s' % v + bcolors.ENDC, file=output)
        print('%s}' % ( def_spacing + nested_level * spacing), file=output)
    elif type(obj) == list:
        print('%s[' % (def_spacing+ (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print( bcolors.WARNING + '%s%s' % ( def_spacing + (nested_level + 1) * spacing, v) + bcolors.ENDC, file=output)
        print('%s]' % ( def_spacing + (nested_level) * spacing), file=output)
    else:
        print(bcolors.WARNING + '%s%s' %  ( def_spacing + nested_level * spacing, obj) + bcolors.ENDC)


def check_peer(ipaddr, options=None):
    base_url = append_http(f"{ipaddr}:9000/api/v1/avail/peer")  # return http status code
    try:
        response = pycurl_request(base_url, "get")
        data = response.get("json")
        elapsed = response.get("TOTAL_TIME")
        if response.get("status_code") != 200:
            data = {}
    except Exception as e:
        data = {}

    if data:
        service_avail = data.get("service_available")
        state = data.get("state")
        blockheight = data.get("block_height")
        if service_avail is True and \
            state in ("Vote", "BlockGenerate", "Watch") and \
            icon_nid == data.get('nid'):
            if args.verbose > 1:
                data['location'] = get_location(ipaddr)
                print_debug(f"IPADDR: {ipaddr:<18}, {data.get('location')}, ResponseTime: {elapsed:>3}ms, Avail: {service_avail}, State: {state}, BlockHeight: {blockheight}")
            data['elapsed'] = elapsed
            data['peer_ip'] = ipaddr
        else:
            print_debug(f"[UNAVAIL] fail health -> {ipaddr} - {data}", "FAIL") if args.verbose > 1 else False
            data = {}
            # results_dict.append(data)
    else:
        print_debug(f"[UNAVAIL] data is null -> {ipaddr} - {data}", "FAIL") if args.verbose > 1 else False
    return data


def check_port(ipaddr, port=9000):
    if port is None:
        port = 9000
    result, return_result,  ip_address, status, error = (None, {}, None, None, None)
    timeout = 1
    start_time = time.time()
    try:
        if is_valid_ipv4(ipaddr):
            ip_address = ipaddr
        else:
            ip_address = socket.gethostbyname(ipaddr)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            # result = sock.connect_ex((ip_address, port))
            sock.connect((ip_address, int(port)))
            sock.shutdown(socket.SHUT_RDWR)
            result = 0
        except:
            error = "timeout"
        finally:
            sock.close()
    except:
        error = "connect error"

    if result == 0:
        status = "ok"

    end_time = time.time() - start_time
    data = {
        "elapsed": int(end_time * 1000),
        "peer_ip": ip_address,
        "url": ipaddr,
        "port": port,
        "status": status,
        "error": error
    }
    if status == "ok":
        return_result = data
    return return_result


def peer_ipaddr(p2pEndpoint):
    return p2pEndpoint.split(":")[0]


def is_append_list(grade):
    if args.type == "main" and grade == "0x0":
        return True
    elif args.type == "sub" and grade == "0x1":
        return True
    elif args.type == "all" and grade != "0x2":
        return True
    else:
        return False


def get_ip_list():
    ip_list = []
    API_SERVER = args.url
    try:
        response = call_api(API_SERVER, method="getPRepTerm", call_type="icx_call")
        if response.get("status_code") == 200:
            result = response.get("json").get("result").get("preps")
            for peer in result:
                if is_append_list(peer.get("grade")):
                    ip_list.append(peer_ipaddr(peer.get("p2pEndpoint")))
        elif response.get("status_code") == 400:
            response = call_api(API_SERVER, method="getPReps", call_type="icx_call")
            preps_info = response.get("json")
            for peer in preps_info["result"]["preps"]:
                # if is_append_list(peer.get("grade")):
                ip_list.append(remove_port(peer.get("p2pEndpoint")))
    except:
        kvPrint("Unexpected error get_ip_list():", sys.exc_info())

    return ip_list


async def run_async_function(function, ip_list, options=None):
    # ip_list = get_ip_list()
    result_data = []
    if args.verbose:
        spinner = Halo(text=f"", spinner='dots')
        spinner.start()
    if len(ip_list) > 0:
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Set any session parameters here before calling `fetch`
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    function,
                    *(ipaddr, options)
                )
                for ipaddr in ip_list
            ]
            for response in await asyncio.gather(*tasks):
                if response:
                    result_data.append(response)
                # pass
    if args.verbose:
        spinner.stop()

    return result_data


def getPRep(API_SERVER, main_reps):
    repsHash = call_api(API_SERVER, method="icx_getBlock", params={}, return_key="repsHash")
    rep_getListByHash = call_api(API_SERVER, method="rep_getListByHash", params={"repsHash": repsHash}, return_key="result")
    return_list = []
    for info in rep_getListByHash:
        ipaddr = info.get("p2pEndpoint").split(":")[0]
        if info.get("address") in main_reps:
            return_list.append(ipaddr)
    return return_list


def call_api(API_SERVER, method, params=None, call_type=None, return_key=None):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1234,
        "params": params

    }
    if call_type == "icx_call":
        payload['method'] = "icx_call"
        payload['params'] = {
                                "from": "hx0000000000000000000000000000000000000000",
                                "to": "cx0000000000000000000000000000000000000000",
                                "dataType": "call",
                                "data": {
                                    "method": method
                                }
                            }
    response = pycurl_request(append_api_url(API_SERVER), method="post", payload=payload, timeout=10)

    if return_key is not None:
        return_value = find_the_key2(response.get("json"), return_key)
        if len(return_value) == 1:
            return return_value[0]
    else:
        return_value = response

    return return_value


def append_http(url):
    if "http://" not in url and "https://" not in url:
        url = f"http://{url}"
    return url


def append_api_url(url, version="3"):
    api_version = f"api/v{version}"
    if api_version not in url:
        url = append_http(url)
        return f"{url}/{api_version}"

    return url


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

def extract_keys(data_list, key):
    return_reslut = []
    for row in data_list:
        if row.get(key):
            return_reslut.append(row.get(key))
    return return_reslut

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


def openFile(filename):
    try:
        file = open(filename).read()
    except:
        print("Error open file:" + filename)
        file = None
    return file


def is_docker():
    if os.path.isfile("/.dockerenv"):
        return True
    return False


def openJson(filename):
    json_data = openFile(filename)
    try:
        result = json.loads(json_data)
    except:
        print("Error Decoding json : " + filename)
        result = {}
    return result


def writeFile(filename, data):
    with open(filename, 'w') as outfile:
        outfile.write(data)


def writeJson(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, default=json_default)
    if os.path.exists(filename):
        print("[OK] Write json file -> %s, %s" % (filename, file_size(filename)))


def getListCount(list, count=5):
    return_list = []
    for i, val in enumerate(list):
        return_list.append(f"{val['peer_ip']}:9000")
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


def split_ip_port(ipaddr):
    ip, port = re.findall(r'([\d.]+)', ipaddr)
    if ip is None:
        return [ipaddr]
    return [ip, port]


def remove_port(ipaddr):
    return ipaddr.split(":")[0]


def is_valid_ipv4(ip):
    """Validates IPv4 addresses.
    """
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None


def pycurl_request(url, method="get", payload={}, timeout=TIMEOUT):
    """
    :param url:
    :param elapesd_type: (each | cumulative)
    :return:
    """
    m = {}
    method = method.upper()
    buffer = io.BytesIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.TIMEOUT, timeout)
    curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
    curl.setopt(pycurl.CUSTOMREQUEST, method.upper())
    curl.setopt(pycurl.HTTPHEADER, ['User-Agent: prep-tool', 'Content-Type: application/json'])
    curl.setopt(pycurl.SSL_VERIFYPEER, False)
    # curl.setopt(pycurl.FOLLOWLOCATION, 1)

    if payload and method == "POST":
        body_as_json_string = json.dumps(payload) # dict to json
        body_as_file_object = io.StringIO(body_as_json_string)
        curl.setopt(pycurl.POST, True)
        curl.setopt(pycurl.READDATA, body_as_file_object)
        curl.setopt(pycurl.POSTFIELDSIZE, len(body_as_json_string))

    try:
        curl.perform()
        response = buffer.getvalue().decode('UTF-8')
        try:
            json_response = json.loads(response)
        except json.decoder.JSONDecodeError:
            json_response = None

        m['effective-url'] = curl.getinfo(pycurl.EFFECTIVE_URL)
        m['status_code'] = curl.getinfo(pycurl.HTTP_CODE)

        last_elapsed = 0
        elapsed_time = 0
        elapsed_each = 0
        total_elapsed_each_sum = 0
        """
        https://curl.haxx.se/libcurl/c/curl_easy_getinfo.html
         |
         |--NAMELOOKUP
         |--|--CONNECT
         |--|--|--APPCONNECT
         |--|--|--|--PRETRANSFER
         |--|--|--|--|--STARTTRANSFER
         |--|--|--|--|--|--TOTAL
         |--|--|--|--|--|--REDIRECT
        """
        for attr_name in CURL_TIME_ATTRS:
            pycurl_attr = getattr(pycurl, attr_name)
            elapsed_time = int(curl.getinfo(pycurl_attr) * 1000)
            # elapsed_time = curl.getinfo(pycurl_attr)
            if attr_name == "TOTAL_TIME":
                elapsed_each = elapsed_time
            elif elapsed_time > 0:
                elapsed_each = elapsed_time - last_elapsed
            else:
                elapsed_each = 0
            total_elapsed_each_sum += elapsed_each
            if elapsed_time > 0:
                last_elapsed = elapsed_time
            m[attr_name] = elapsed_each
        m['redirect-count'] = curl.getinfo(pycurl.REDIRECT_COUNT)
        m['header-size'] = curl.getinfo(pycurl.HEADER_SIZE)

        # m['size-upload'] = curl.getinfo(pycurl.SIZE_UPLOAD)
        # m['size-download'] = curl.getinfo(pycurl.SIZE_DOWNLOAD)
        # m['speed-upload'] = curl.getinfo(pycurl.SPEED_UPLOAD)
        #
        # m['request-size'] = curl.getinfo(pycurl.REQUEST_SIZE)
        # m['content-length-download'] = curl.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
        # m['content-length-upload'] = curl.getinfo(pycurl.CONTENT_LENGTH_UPLOAD)
        #
        # m['content-type'] = curl.getinfo(pycurl.CONTENT_TYPE)
        # m['response-code'] = curl.getinfo(pycurl.RESPONSE_CODE)
        # m['speed-download'] = curl.getinfo(pycurl.SPEED_DOWNLOAD)
        # m['ssl-verifyresult'] = curl.getinfo(pycurl.SSL_VERIFYRESULT)
        # m['filetime'] = curl.getinfo(pycurl.INFO_FILETIME)
        #
        #
        # m['http-connectcode'] = curl.getinfo(pycurl.HTTP_CONNECTCODE)
        # # m['httpauth-avail'] = curl.getinfo(pycurl.HTTPAUTH_AVAIL)
        # # m['proxyauth-avail'] = curl.getinfo(pycurl.PROXYAUTH_AVAIL)
        # m['os-errno'] = curl.getinfo(pycurl.OS_ERRNO)
        # m['num-connects'] = curl.getinfo(pycurl.NUM_CONNECTS)
        # m['ssl-engines'] = curl.getinfo(pycurl.SSL_ENGINES)
        # m['cookielist'] = curl.getinfo(pycurl.INFO_COOKIELIST)
        # m['lastsocket'] = curl.getinfo(pycurl.LASTSOCKET)

        m['json'] = json_response
        if m.get("json") is None:
            m['response'] = response
    except Exception as error:
        response = None
        json_response = None
        if args.verbose > 2:
            print_debug(f"{url} , {error.args[1]}", "FAIL")
        m['error'] = error.args[1]

    buffer.close()
    curl.close()
    return m


def get_location(ipaddr):
    res = pycurl_request(f"https://api.ipgeolocation.io/ipgeo?apiKey=04121b22f4244f55a04a496edcc8fd9a&ip={ipaddr}")
    if res.get("status_code") == 200:
        return res['json']['country_code3']


def str2bool(v):
    true_list = ("yes", "true", "t", "1", "True", "TRUE")
    if type(v) == bool:
        return v
    if type(v) == str:
        return v.lower() in true_list
    return eval(f"{v}") in true_list


def get_public_ip():
    response = pycurl_request("http://checkip.amazonaws.com")
    if response.get("response"):
        ipaddr = response.get("response").replace("\n","")
        if is_valid_ipv4(ipaddr):
            return ipaddr


def get_docker_info():
    try:
        if os.path.isfile("/.docker_info"):
            docker_info = openJson("/.docker_info")
        else:
            docker_info = dict(
                public_ip=get_public_ip(),
                network_id=pycurl_request(f"{args.url}/api/v1/status/peer")['json']['nid']
            )
            if is_docker():
                writeJson("/.docker_info", docker_info)
    except:
        docker_info = {}
    return docker_info


def parse_data(data_list, limit=5, sort_key="elapsed",   return_key="peer_ip"):
    data_list[:] = [d for d in data_list if d.get(sort_key) is not None]
    sorted_list = sorted(data_list, key=lambda k: (k[sort_key]))
    return_result = []

    for row in sorted_list[:limit]:
        if row.get(return_key):
            return_result.append(row.get(return_key))
    return return_result

    # return sorted_list[:limit]


def main():
    global args, fastpeer_domains, icon_nid, public_ip
    # IS_DOCKER = is_docker() #TODO replace to IS_DOCKER
    parser = argparse.ArgumentParser(prog='find_neighbor')
    parser.add_argument('url')
    parser.add_argument('count', nargs="?", type=int, default=4)
    parser.add_argument('-v', '--verbose', action='count', help=f'verbose mode. view level', default=0)
    parser.add_argument('-b', '--blockheight', metavar='blockheight', type=int, help=f'blockheight', default=0)
    parser.add_argument('-w', '--writeconfig', action='count', help=f'write to configure json', default=0)
    parser.add_argument('-t', '--type', type=str, help=f'prep grade type (all|main|sub)', default="main")
    args = parser.parse_args()
    args.url = append_http(args.url)

    docker_info = get_docker_info()
    icon_nid = docker_info.get("network_id")
    public_ip = docker_info.get("public_ip")

    if args.verbose:
        endpoint_status = pycurl_request(f"{args.url}/api/v1/status/peer")
        if endpoint_status.get('json'):
            endpoint_elapsed = ', '.join([f" \n {item:<16}: {endpoint_status.get(item)}ms" for item in CURL_TIME_ATTRS])
            print_debug(f"url = {args.url} {endpoint_elapsed}")
            icon_nid = endpoint_status["json"].get('nid')
            print_debug(f"NID = {icon_nid}")

    fastpeer_domains = [ f"fastpeer{x}.icon" for x in range(0, args.count) ]
    print(f"Arguments={args}") if args.verbose > 0 else False

    configure_json_file = os.environ.get('configure_json', "/prep_peer/conf/configure.json")
    configure_json = openJson(configure_json_file)

    if configure_json.get("CHANNEL_OPTION"):
        if configure_json['CHANNEL_OPTION']['icon_dex'].get("radiostations", None) is None:
            configure_json['CHANNEL_OPTION']['icon_dex']['radiostations'] = []

    check_targets = get_ip_list()
    print_debug(f"Target IP length = {len(check_targets)}")

    if not check_targets:
        print(f"IP targets is null")
        sys.exit()
    # total_start_time = time.time()
    # print_debug(f"len = {len(ip_list)}", "FAIL")
    # start_time = time.time()
    # loop = asyncio.get_event_loop()
    # future = asyncio.ensure_future(run_async_function(check_port, check_targets))
    # opened_peer = loop.run_until_complete(future)
    # end_time = time.time() - start_time
    # print_debug(f" check_port = {end_time}")
    # open_ip_list = parse_data(opened_peer, limit=10)

    # ip_list = extract_keys(checked_peer, "peer_ip")

    # dump(results_dict)
    # open_ip_list = ip_list
    start_time = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run_async_function(check_peer, check_targets))
    results_dict = loop.run_until_complete(future)
    end_time = time.time() - start_time
    print_debug(f" check_peer time= {end_time}")


    if args.writeconfig:
        # modify configure file
        ip_list = getListCount(results_dict, args.count)
        print(f"List={ip_list}, List_length={len(ip_list)}") if args.verbose > 0 else False

        # if len(ip_list) >= 0:
        default_endpoint = os.environ.get('ENDPOINT_URL', None)
        default_fastpeer = []
        if default_endpoint:
            default_fastpeer.append(default_endpoint)
            for i, fastpeer_domain in enumerate(fastpeer_domains):
                print(f">> fastpeer_domain={fastpeer_domain}, ENDPOINT_URL={default_endpoint}") if args.verbose > 0 else False
                default_fastpeer.append(f"{fastpeer_domain}:9000")
            configure_json['CHANNEL_OPTION']['icon_dex']['radiostations'] = default_fastpeer
            writeJson(configure_json_file, configure_json)
            add_alive_peer(ip_list, default_fastpeer)

        else:
            print(f"[ERROR] ENDPOINT_URL not found = {default_endpoint}")
        # else:
        #     print("Can't find neighbor [LIST]")
    else:
        # modify hosts file
        sorted_list = sorted(results_dict, key=lambda k: (k["elapsed"], -k["block_height"]))
        if args.verbose:
            print("Sorted Values ")
            for i, item in enumerate(sorted_list):
                # print_debug(f"[{i}] {item['elapsed']}ms , {item['peer_ip']}, {item['block_height']} ")
                print_debug(f"[{i:>2}] {item.get('location')}, IPADDR: {item['peer_ip']:<18}, ResponseTime: {item['elapsed']:>3}ms, Avail: {item['service_available']}, State: {item['state']}, BlockHeight: {item['block_height']}")

        # if len(sorted_list) > 0:

        if sorted_list:
            ip_list = getListCount(sorted_list, len(fastpeer_domains))
            add_alive_peer(ip_list, fastpeer_domains)
        else:
            print("Can't find neighbor [HOSTS]")


def add_alive_peer(ip_list, fastpeer_domains):
    print(f"Alive peer_list={ip_list}, fastpeer_domains={fastpeer_domains}")
    alive_peer = None
    for i, fastpeer_domain in enumerate(fastpeer_domains):
        try:
            fastpeer_info = ip_list[i]
            fastpeer_ip, port = re.findall(r'([\d.]+)', fastpeer_info)
            if args.blockheight > 0:
                blockhash = call_api(f"http://{fastpeer_ip}:9000", method="icx_getBlockByHeight", params={"height": hex(args.blockheight)}, return_key="block_hash")
                print(f"[ {args.blockheight} BH ] {fastpeer_ip} / {blockhash}")
            else:
                add_host(fastpeer_ip, fastpeer_domain)
                alive_peer = fastpeer_ip
        except:
            if alive_peer is not None:
                add_host(alive_peer, fastpeer_domain)


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