#!/usr/bin/env python3.7
from collections import defaultdict
from multiprocessing.pool import ThreadPool
import time
import requests
import sys
import argparse

results = defaultdict(list)
TIMEOUT = 5

region_info = {
    "Seoul"   : ".s3",
    "Tokyo"   : "-jp.s3",
    "Virginia": "-va.s3",
    "Hongkong": "-hk.s3.ap-east-1",
    "Singapore": "-sg.s3",
    "Mumbai"   : "-mb.s3",
    "Frankfurt": "-ff.s3",
}


def findFastestRegion():
    results = {}
    pool = ThreadPool(6)
    i = 0

    for region_name, region_code in region_info.items():
        URL=f'https://icon-leveldb-backup{region_code}.amazonaws.com/route_check'
        exec_func = "getTime"
        exec_args = ( f"{URL}", region_name )
        results[i]= {}
        results[i]["data"] = pool.apply_async(getattr(sys.modules[__name__], exec_func), exec_args)
        i += 1
    pool.close()
    pool.join()

    last_latency = {}
    for i, p in results.items():
        data = p['data'].get()
        if time is not None:
            if len(last_latency) == 0:
                last_latency = data
            if last_latency.get("time", 99999) >= data.get("time"):
                last_latency = data
        print(data) if args.verbose else False
    return last_latency


def getTime(url, name="NULL"):
    try:
        response = requests.get(f'{url}', timeout=3)
        response_text = response.text
        time = response.elapsed.total_seconds()
    except:
        time = None
        response_text = None
    return {"url": url, "time": time, "name": name, "text": response_text}


def disable_ssl_warnings():
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
    global args, fastpeer_domains
    disable_ssl_warnings()
    parser = argparse.ArgumentParser(prog='find_region')
    parser.add_argument('-v', '--verbose', action='count', help=f'verbose mode. view level', default=0)
    args = parser.parse_args()
    result = findFastestRegion()

    if "OK" in result.get("text"):
        print(result.get("url").replace("/route_check",""))
    else:
        sys.exit(127)

if __name__ == '__main__':
    main()
