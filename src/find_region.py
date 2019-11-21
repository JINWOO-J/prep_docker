#!/usr/bin/env python3.7
from collections import defaultdict
from multiprocessing.pool import ThreadPool
import requests
import sys
import argparse
from random import randint
from timeit import default_timer
from datetime import *

results = defaultdict(list)
TIMEOUT = 5

region_info = {
    "Seoul": ".s3",
    "Tokyo": "-jp.s3",
    "Virginia": "-va.s3",
    "Hongkong": "-hk.s3.ap-east-1",
    "Singapore": "-sg.s3",
    "Mumbai"   : "-mb.s3",
    "Frankfurt": "-ff.s3",
}

AWSRegions = {
    "Seoul": "ap-northeast-2",
    "Tokyo": "ap-northeast-1",
    "Virginia": "us-east-1",
    "Hongkong": "ap-east-1",
    "Singapore": "ap-southeast-1",
    "Mumbai": "ap-south-1",
    "Frankfurt": "eu-central-1",
    "Ohio": "us-east-2",
    "California": "us-west-1",
    "US-West": "us-west-2",
    "Ceentral":"ca-central-1",
    "Ireland": "eu-west-1",
    "London": "eu-west-2",
    "Sydney": "ap-southeast-2",
    "São Paulo": "sa-east-1",
    "Beijing": "cn-north-1",
}

def todaydate(type=None):
    if type is None:
        return '%s' % datetime.now().strftime("%Y%m%d")
    elif type == "log":
        return '%s' % datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    elif type == "ms":
        return '%s' % datetime.now().strftime("%Y%m%d_%H%M%S.%f")[:-3]

def findFastestRegion():
    results = {}
    pool = ThreadPool(6)
    i = 0
    for region_name, region_code in region_info.items():
        URL=f'https://icon-leveldb-backup{region_code}.amazonaws.com/route_check?x=%s' % todaydate("ms")
        exec_func = "getTime"
        exec_args = ( f"{URL}", region_name )
        results[i]= {}
        results[i]["data"] = pool.apply_async(getattr(sys.modules[__name__], exec_func), exec_args)
        i += 1

    for region_name, region_code in AWSRegions.items():
        URL=f'https://s3.{AWSRegions.get(region_name)}.amazonaws.com/ping?x=%s' % todaydate("ms")
        exec_func = "getTime"
        exec_args = ( f"{URL}", region_name )
        results[i]= {}
        results[i]["data"] = pool.apply_async(getattr(sys.modules[__name__], exec_func), exec_args)
        i += 1

    pool.close()
    pool.join()
    return_data = []
    for i, p in results.items():
        data = p['data'].get()
        if data:
            return_data.append(data)
    return return_data


def getTime(url, name="NULL"):
    START_TIME = default_timer()
    try:
        response = requests.get(f'{url}', timeout=3)
        response_text = response.text
        time = response.elapsed.total_seconds()
        status_code = response.status_code
    except:
        time = None
        response_text = None
        status_code = 999
    elapsed = default_timer() - START_TIME

    data = {"url": url, "time": time, "run_time": elapsed, "name": name, "text": response_text, "status_code": status_code}
    # print(data) if args.verbose else False
    if data.get('time') and data.get("run_time") and data.get("status_code") == 200:
        return data
    # return data


def disable_ssl_warnings():
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
    global args, fastpeer_domains
    disable_ssl_warnings()
    parser = argparse.ArgumentParser(prog='find_region')
    parser.add_argument('-v', '--verbose', action='count', help=f'verbose mode. view level', default=0)
    args = parser.parse_args()
    results = findFastestRegion()

    sort_data = sorted( results, key=(lambda x: x['run_time']), reverse=False )
    return_data = []

    for i, v in enumerate(sort_data):
        print(i,v) if args.verbose else False
        region_code = region_info.get(v["name"])
        if region_code:
            DOWNLOAD_URL=f'https://icon-leveldb-backup{region_code}.amazonaws.com'
            v['url'] = DOWNLOAD_URL
            return_data.append(v)
    # if "OK" in return_data[0].get("text"):
    if return_data[0].get("status_code") == 200:
        print(results[0].get("url").replace("/route_check",""))
        if args.verbose:
            print(f"{return_data[0].get('name')} / {results[0].get('url')} / {results[0].get('run_time')} ")
    else:
        sys.exit(127)

if __name__ == '__main__':
    main()