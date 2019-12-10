#!/usr/bin/env python3

import time, sys
import subprocess, argparse
import select
import json
import requests

import os, string, re, signal, errno

colours = {
    'none'       :    "",
    'default'    :    "\033[0m",
    'bold'       :    "\033[1m",
    'underline'  :    "\033[4m",
    'blink'      :    "\033[5m",
    'reverse'    :    "\033[7m",
    'concealed'  :    "\033[8m",

    'black'      :    "\033[30m",
    'red'        :    "\033[31m",
    'green'      :    "\033[32m",
    'yellow'     :    "\033[33m",
    'blue'       :    "\033[34m",
    'magenta'    :    "\033[35m",
    'cyan'       :    "\033[36m",
    'white'      :    "\033[37m",

    'on_black'   :    "\033[40m",
    'on_red'     :    "\033[41m",
    'on_green'   :    "\033[42m",
    'on_yellow'  :    "\033[43m",
    'on_blue'    :    "\033[44m",
    'on_magenta' :    "\033[45m",
    'on_cyan'    :    "\033[46m",
    'on_white'   :    "\033[47m",

    'beep'       :    "\007",
    'previous'   :    "prev",
    'unchanged'  :    "unchanged",

    # non-standard attributes, supported by some terminals
    'dark'         :    "\033[2m",
    'italic'       :    "\033[3m",
    'rapidblink'   :    "\033[6m",
    'strikethrough':    "\033[9m",

    # aixterm bright color codes
    # prefixed with standard ANSI codes for graceful failure
    'bright_black'      :    "\033[30;90m",
    'bright_red'        :    "\033[31;91m",
    'bright_green'      :    "\033[32;92m",
    'bright_yellow'     :    "\033[33;93m",
    'bright_blue'       :    "\033[34;94m",
    'bright_magenta'    :    "\033[35;95m",
    'bright_cyan'       :    "\033[36;96m",
    'bright_white'      :    "\033[37;97m",

    'on_bright_black'   :    "\033[40;100m",
    'on_bright_red'     :    "\033[41;101m",
    'on_bright_green'   :    "\033[42;102m",
    'on_bright_yellow'  :    "\033[43;103m",
    'on_bright_blue'    :    "\033[44;104m",
    'on_bright_magenta' :    "\033[45;105m",
    'on_bright_cyan'    :    "\033[46;106m",
    'on_bright_white'   :    "\033[47;107m",
}


# ignore ctrl C - this is not ideal for standalone grcat, but
# enables propagating SIGINT to the other subprocess in grc
# signal.signal(signal.SIGINT, signal.SIG_IGN)

def add2list(clist, m, patterncolour):
    for group in range(0, len(m.groups()) + 1):
        if group < len(patterncolour):
            clist.append((m.start(group), m.end(group), patterncolour[group]))
        else:
            clist.append((m.start(group), m.end(group), patterncolour[0]))
    return clist


def get_colour(x):
    if x in colours:
        return colours[x]
    elif len(x) >= 2 and x[0] == '"' and x[-1] == '"':
        return eval(x)
    else:
        raise ValueError('Bad colour specified: ' + x)


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


def post(url, payload, elapsed=False):

    if not re.search('^http', url):
        url = f"http://{url}"

    data = None
    try:
        data = requests.post(url, json=payload, verify=False, timeout=5)
    except requests.exceptions.HTTPError as errh:
        kvPrint("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        kvPrint("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        kvPrint("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        kvPrint("OOps: Something Else", err)

    if data is not None:
        if data.status_code > 200:
            print(f"status_code: {data.status_code} , url: {url} , payload: {payload}")
        if elapsed and data.status_code:
            return {"data": data, "elapsed": data.elapsed.total_seconds()}
        else:
            return data


def get_parser():
    parser = argparse.ArgumentParser(description='Change peer_id to hostname in the loopchain log file')
    # positional argument for command
    parser.add_argument('command', nargs='?', help='cat, tail', default="tail")
    parser.add_argument('--url', metavar='url', help=f'loopchain API URL', default="http://localhost:9000")
    parser.add_argument('--conf', metavar='conf', help=f'configure file', default=None)
    parser.add_argument('-c', '--color', action='count', help=f'show colorful logging ', default=0)
    parser.add_argument('--logfile', metavar='logfile', help=f'log file', default="/app/prep/data/loopchain/log/loopchain.channel.icon_dex.log")
    return parser


def getNameByaddress():
    return_result = {}

    if args.conf:
        print(args.conf)
        conf_file = openJson(args.conf)
        for peer in conf_file['icon_dex']['peers']:
            if peer.get("name"):
                name = peer.get("name")
            else:
                name = peer.get("peer_target")
            address = peer.get("id")
            return_result[address] = name

    else:
        payload = genParam("getPReps")
        response = post(
            f"{args.url}/api/v3", payload=payload)
        return_result = {}
        if response:
            prep_list = response.json().get("result").get("preps")

            for i, v in enumerate(prep_list):
                name = v.get("name")
                address = v.get("address")
                return_result[address] = name

    return return_result


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


def file_exist(filename):
    try:
        f = open(filename)
        f.close()
    except FileNotFoundError:
        print(f'File does not exist - {filename}')
        return False
    except:
        print(f"{sys.exc_info()[0]}")
        return False
    return True


def changeMatchString(line, prep_address):

    for prep_hash in prep_address:
        if prep_hash in line:
            line = line.replace(prep_hash, f">> {prep_address[prep_hash]} << ({prep_hash}) ")
    return line


def getREGEX(data):
    regexplist = []

    is_last = 0
    split = str.split
    lower = str.lower
    letters = string.ascii_letters

    ll = {'count':"more"}

    for l in data.splitlines():
        if l in "===" and is_last == 1:
            regexplist.append(ll)
            ll = {'count':"more"}

        if "==" in l:
            is_last = 1
        elif l == "":
            is_last = 1
        elif not l[0] in letters:
            ll = {}
            # print(f"letters {l}")
            continue
        elif l[0] == "#" or l[0] == '\012':
            regexplist.append(ll)
            ll = {'count':"more"}
            continue
        else:
            # print(f" ELSE                           l={l} , is_last={is_last}, ll={ll}")
            is_last = 0

            fields = split(l, "=", 1)
            if len(fields) != 2:
                sys.stderr.write('Error in configuration, I expect keyword=value line\n')
                sys.stderr.write('But I got instead:\n')
                sys.stderr.write(repr(l))
                sys.stderr.write('\n')
                sys.exit(1)
            keyword, value = fields
            keyword = lower(keyword)


            if "==" in value:
                is_last = 1

                raise SystemExit()
                continue
            else:
                if keyword in ('colors', 'colour', 'color'):
                    keyword = 'colours'
                if not keyword in ["regexp", "colours", "count", "command", "skip", "replace", "concat"]:
                    raise ValueError("Invalid keyword")
                ll[keyword] = value
                # print(f"keyword ==== {keyword}")
                # cs = ll['count']
                if keyword == "count":
                    continue
                if 'colours' in ll:

                    colstrings = list(
                        [''.join([get_colour(x) for x in split(colgroup)]) for colgroup in split(ll['colours'], ',')]
                    )
                    ll['colours'] = colstrings

                elif 'regexp' in ll:
                    if ll.get("regexp", None) :
                        ll['regexp'] = re.compile(ll['regexp']).search

    return regexplist

def classdump(obj):
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    for attr in dir(obj):
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            print(bcolors.OKGREEN + f"obj.{attr} = " +
                  bcolors.WARNING + f"{value}" + bcolors.ENDC)


class GetOutOfLoop( Exception ):
    pass

def colorizing(line, regexplist):
    prevcolour = colours['default']
    prevcount = "more"
    blockflag = 0
    clist = []
    skip = 0

    for pattern in regexplist:
        pos = 0
        currcount = pattern.get('count')
        if currcount:
            if line == "":
                return
            if line[-1] in '\r\n':
                line = line[:-1]

            keepinnerloop = True

            while keepinnerloop:
                m = pattern['regexp'](line, pos)
                if m:
                    if 'replace' in pattern:
                        line = re.sub(m.re, pattern['replace'], line)
                        # m = pattern['regexp'](line, pos)
                        # if not m:
                        #    break
                    if 'colours' in pattern:
                        if currcount == "block":
                            blockflag = 1
                            blockcolour = pattern['colours'][0]
                            currcount = "stop"
                            keepinnerloop = False

                        elif currcount == "unblock":
                            blockflag = 0
                            blockcolour = colours['default']
                            currcount = "stop"

                        clist = add2list(clist, m, pattern['colours'])

                        if currcount == "previous":
                            currcount = prevcount

                        if currcount == "stop":
                            keepinnerloop = False

                        if currcount == "more":
                            prevcount = "more"
                            newpos = m.end(0)
                            # print(f"newpos={newpos}")
                            # special case, if the regexp matched but did not consume anything,
                            # advance the position by 1 to escape endless loop
                            if newpos == pos:
                                pos += 1
                            else:
                                pos = newpos
                        else:
                            prevcount = "once"
                            pos = len(line)

                    if 'concat' in pattern:
                        with open(pattern['concat'], 'a') as f:
                            f.write(line + '\n')
                        if 'colours' not in pattern:
                            keepinnerloop = False
                    if 'command' in pattern:
                        os.system(pattern['command'])
                        if 'colours' not in pattern:
                            keepinnerloop = False
                    if 'skip' in pattern:
                        skip = pattern['skip'] in ("yes", "1", "true")
                        if 'colours' not in pattern:
                            keepinnerloop = False
                else:
                    keepinnerloop = False

                if m and currcount == "stop":
                    prevcount = "stop"
                    keepinnerloop=False
                # keepinnerloop = False
                # print(m, keepinnerloop)

            if len(clist) == 0:
                prevcolour = colours['default']
            first_char = 0
            last_char = 0
            length_line = len(line)
            if blockflag == 0:
                cline = (length_line + 1) * [colours['default']]
                for i in clist:
                    # each position in the string has its own colour
                    if i[2] == "prev":
                        cline[i[0]:i[1]] = [colours['default'] + prevcolour] * (i[1] - i[0])
                    elif i[2] != "unchanged":
                        cline[i[0]:i[1]] = [colours['default'] + i[2]] * (i[1] - i[0])
                    if i[0] == 0:
                        first_char = 1
                        if i[2] != "prev":
                            prevcolour = i[2]
                    if i[1] == length_line:
                        last_char = 1
                if first_char == 0 or last_char == 0:
                    prevcolour = colours['default']
            else:
                cline = (length_line + 1) * [blockcolour]
            nline = ""
            clineprev = ""
            if not skip:
                # print(f"skip= {skip}")
                for i in range(len(line)):
                    if cline[i] == clineprev:
                        nline = nline + line[i]
                    else:
                        nline = nline + cline[i] + line[i]
                        clineprev = cline[i]
                nline = nline + colours['default']
    try:
        print(nline)
    except IOError as e:
        print(f" Error : {e}")



def main():
    filename = args.logfile
    prep_address = getNameByaddress()
    file_exist(args.logfile)

    print(f"args.url = {args.url}")
    if args.command is "tail":
        args.color = True

    regexplist = getREGEX(REGEX_DATA) if args.color > 0 else False

    # print(regexplist)
    if len(prep_address) == 0:
        print("[ERROR] peer_id dict not found")
        # raise SystemExit()

    if args.command == "cat":
        f = subprocess.Popen(['cat', filename],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in f.stdout:
            line = line.decode("utf-8").rstrip('\r\n')
            if len(prep_address) > 0:
                line = changeMatchString(line, prep_address)
            if args.color > 0:
                colorizing(line, regexplist)
            else:
                print(line)

            # print(line.decode().strip())

    elif args.command == "tail":
        f = subprocess.Popen(['tail', '-F', filename],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = select.poll()
        p.register(f.stdout)

        while True:
            if p.poll(1):
                readline = f.stdout.readline().decode("utf-8").rstrip('\r\n')
                line = changeMatchString(readline, prep_address)
                if args.color > 0:
                    colorizing(line, regexplist)
                else:
                    print(line)
            time.sleep(0.01)



REGEX_DATA = """
#WARINIG
regexp=WARNING.*
colours=red
count=more
======

#ERROR
regexp=ERROR.*
colours=bold red
count=more
======

#Last block count
regexp=Fail.*
colours=bold red
count=more
======

# name of node id
regexp=hx\w+
colours=yellow
count=once
======

#Last block count
regexp=(last_block\:)(\s+)(\d+)
colours=bold yellow, yellow
count=once
======

regexp=.*last message repeated \d+ times$
colours=yellow
count=stop
======

# this is date
regexp=^... (\d| )\d \d\d:\d\d:\d\d(\s[\w\d]+?\s)
colours=green, green, red
count=once
======

# everything in parentheses
regexp=\(.+?\)
colours=green
count=more
======

# everything in `'
regexp=\`.+?\'
colours=bold yellow
count=more
======

# this is probably a pathname
regexp=/[\w/\.]+
colours=bold green
count=more
======

# name of process and pid
regexp=([\w/\.\-]+)(\[\d+?\])
colours=bold blue, bold red
count=more
======

# ip number
regexp=\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}
colours=bold magenta
count=more
======

# connect requires special attention
regexp=connect
colours=on_red
count=more
=======

#CHANGED_NAME
regexp=(>>(.+?)<<)
colours=yellow, white
count=more
======

#VoteStatus
regexp=(True|Empty|Result|Quorum)(\s+)\:(.*)
colours=bright_blue, bold yellow
count=more
======

# this configuration file is suitable for displaying kernel log files
# example of text substitution
#regexp=\bda?emon
#replace=angel
#colours=red
#======
# example of text substitution
#regexp=(\d\d):(\d\d):(\d\d)
#replace=\1h\2m\3s
#======
# display this line in yellow and stop further processing

"""

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    print(args)
    main()
