#!/usr/bin/env python3.7
import requests
import sys
import argparse
from timeit import default_timer
import asyncio
from concurrent.futures import ThreadPoolExecutor

results = []
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

def getTime(url, name="NULL"):
    START_TIME = default_timer()
    try:
        response = requests.get(f'{url}', timeout=3)
        response_text = response.text
        time = response.elapsed.total_seconds()
    except:
        time = None
        response_text = None
    elapsed = default_timer() - START_TIME

    data = {"url": url, "time": time, "run_time": elapsed, "name": name, "text": response_text}
    print(data) if args.verbose else False
    results.append(data)
    return data


async def findFastestRegion(region_info):
    tasks = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()

            for region_name, region_code in region_info.items():
                URL=f'https://icon-leveldb-backup{region_code}.amazonaws.com/route_check'
                tasks.append(loop.run_in_executor(executor, getTime, *(URL, region_name)))
            await asyncio.gather(*tasks)
    return


def disable_ssl_warnings():
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
    global args, fastpeer_domains, results
    disable_ssl_warnings()
    parser = argparse.ArgumentParser(prog='find_region')
    parser.add_argument('-v', '--verbose', action='count', help=f'verbose mode. view level', default=0)
    args = parser.parse_args()
    # result = findFastestRegion()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(findFastestRegion(region_info))
    loop.run_until_complete(future)
    # print(results[0])

    if "OK" in results[0].get("text"):
        print(results[0].get("url").replace("/route_check",""))
    else:
        sys.exit(127)

if __name__ == '__main__':
    main()
