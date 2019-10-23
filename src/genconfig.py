#!/usr/bin/env python
import json
# from termcolor import colored, CPrint
import sys,os,time,io

# from loop_config import *
import yaml

from collections import OrderedDict

# non order
# https://stackoverflow.com/questions/16782112/can-pyyaml-dump-dict-items-in-non-alphabetical-order
yaml.add_representer(dict, lambda self, data: yaml.representer.SafeRepresenter.represent_dict(self, data.items()))

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)


def load_compose(filename="docker-compose.yml"):
    with open(path+"/"+filename, 'r') as stream:
        data_loaded = yaml.load(stream)
        dump(data_loaded)    
        return data_loaded

def write_compose(data, filename="docker-compose_tmp.yml"):
    with io.open(filename, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

def main():
    try: 
        IPADDR = sys.argv[1]
    except (UnboundLocalError,IndexError):
        IPADDR = None
        
    if IPADDR:
        IPADDR = sys.argv[1]
    else:    
        IPADDR = ask_parameter("Input IP address ")
        CPrint("Yours IPaddr:  %s" %IPADDR)

    global config, loopchain_conf
    config = config_fn()   
    loopchain_conf = loopchain_conf_fn()

    compose_yml = load_compose()
    dump(compose_yml)   
    compose_file = config["LOOPCHAIN_APP_DIR"] + "/docker-compose.yml"
    write_compose( compose_yml, compose_file)

    for item in config:        
        directory = config[item]    
        if "DIR" in item:        
            if not os.path.exists(directory):            
                CPrint("make dirs")
                dump(directory)
                os.makedirs(directory)

    CPrint("generate json files")
  
    dump(loopchain_conf)
    loop_conf = looppeer_conf(IPADDR)
    writeJson(loopchain_conf["CONFIGURE_JSON"], loop_conf)
    writeJson(loopchain_conf["CONFIGURE_CHANNEL_JSON"], loop_conf)
    writeJson(loopchain_conf["ICON_SERVICE_JSON"], iconservice_conf() )
    writeJson(loopchain_conf["ICON_RPCSERVER_JSON"], iconrpcserver_conf() )

    # writeEnv(loopchain_conf["ENV_LIST_PEER"], env_list_peer())
    writeEnv(loopchain_conf["ENV_LIST_PEER"], env_list_peer())
    writeEnv(config["LOOPCHAIN_APP_DIR"] + "/.env", loopchain_conf)
    CPrint("make a cert key")

    PUBLIC_FILENAME = config["LOOPCHAIN_CONF_DIR"] + "/" + config["SERVICE"]+"_public"
    PRIVATE_FILENAME = config["LOOPCHAIN_CONF_DIR"] + "/" + config["SERVICE"]+"_private"

    os.system("openssl ecparam -genkey -name secp256k1 | openssl ec -aes-256-cbc -out %(PRIVATE_FILENAME)s.pem -passout pass:%(PASSWORD)s" %
        {'PRIVATE_FILENAME': PRIVATE_FILENAME, 'PASSWORD': config["KEY_PASSWORD"]})
    os.system("openssl ec -in %(PRIVATE_FILENAME)s.pem  -pubout -out %(PUBLIC_FILENAME)s.pem -passin pass:%(PASSWORD)s" %
            {'PRIVATE_FILENAME': PRIVATE_FILENAME,
                'PUBLIC_FILENAME': PUBLIC_FILENAME, 'PASSWORD': config["KEY_PASSWORD"]})
    os.system("openssl pkcs8 -topk8  -in %(PRIVATE_FILENAME)s.pem -out %(PRIVATE_FILENAME)s.der  -outform der -passout pass:%(PASSWORD)s -passin pass:%(PASSWORD)s" %
            {'PRIVATE_FILENAME': PRIVATE_FILENAME,
                'PUBLIC_FILENAME':  PUBLIC_FILENAME, 'PASSWORD': config["KEY_PASSWORD"]})
    os.system("openssl ec -in %(PRIVATE_FILENAME)s.pem -pubout -outform DER -out %(PUBLIC_FILENAME)s.der -passin pass:%(PASSWORD)s" %
            {'PRIVATE_FILENAME': PRIVATE_FILENAME,
                'PUBLIC_FILENAME': PUBLIC_FILENAME, 'PASSWORD': config["KEY_PASSWORD"]})
    os.system("rm -f /app/loopchain/conf/*.pem")

    CPrint("rs_install")
    writeJson(loopchain_conf["CHANNEL_MANAGE_DATA_JSON"] ,make_channel_manage_data_json([IPADDR]))
    writeJson(loopchain_conf["CONFIGURE_RS_JSON"], configure_rs_json() )
    writeJson(loopchain_conf["GEN"], genesis() )


class bcolors:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    light_purple = '\033[94m'
    purple = '\033[95m'

    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'       

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'    
    
def CPrint(msg,color="green"):    
    print (getattr(bcolors, color) + '%s' %msg  + bcolors.ENDC)        

def writeEnv(filename, dict):    
    dump(dict)
    with open(filename, "w") as f:
        for i in dict.keys():            
            f.write(i + "=" +  str(dict[i]) + "\n")

def writeJson(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    if os.path.exists(filename):
        CPrint("[OK] Write json file -> %s, %s" %(filename, file_size(filename)))

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

def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    def_spacing = '   '

    if type(obj) == dict:
        print ('%s{' % ( def_spacing + (nested_level) * spacing ))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print ( bcolors.OKGREEN + '%s%s:' % (def_spacing +(nested_level + 1) * spacing, k) + bcolors.ENDC, end="")                
                dump(v, nested_level + 1, output)                
            else:        
                print ( bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s' % v + bcolors.ENDC, file=output)
        print ('%s}' % ( def_spacing + nested_level * spacing), file=output)
    elif type(obj) == list:
        print  ('%s[' % (def_spacing+ (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print ( bcolors.WARNING + '%s%s' % ( def_spacing + (nested_level + 1) * spacing, v) + bcolors.ENDC, file=output)
        print ('%s]' % ( def_spacing + (nested_level) * spacing), file=output)
    else:
        print (bcolors.WARNING + '%s%s' %  ( def_spacing + nested_level * spacing, obj) + bcolors.ENDC)
def ask_confirm(msg, value="y",type="info"):
    if type == "warn":
        msg = bcolors.FAIL+msg+bcolors.ENDC
    answer = prompt(msg)        
    if answer != value:
        CPrint("Stopped script, your answer:'%s'" % answer, "red")
        raise SystemExit()


def ask_parameter(question):
    reply = str(input(question+' : ')).lower().strip()

    if len(reply) == 0:
        CPrint("Stopped script", "red")
        raise SystemExit
        return False

    return reply

def make_channel_manage_data_json(peer_ipaddr_list):
    global loopchain_conf
    dest_file = loopchain_conf['CHANNEL_MANAGE_DATA_JSON']
    CPrint(dest_file, "red")
    # sudo("mkdir -p %s" % dest_file)
    channel_manage_data = channel_manage_data_json() 
    
    for channel_key in channel_manage_data:
        peer_list = []
        for peer_ipaddr in peer_ipaddr_list:
            peer_list.append({"peer_target": peer_ipaddr+":7100"})
        channel_manage_data[channel_key]["peers"] = peer_list
    dump(channel_manage_data)
    return channel_manage_data


def config_fn():
    env_dict = dict(
        tag="1809201731xb77159",
        tag_service="1809201731xb77159",
        SERVICE = "default",
        KEY_PASSWORD = "test",
        VERSION="default_20180815",        
        docker_repo="repo.devnet.icx",
        LOOPCHAIN_APP_DIR = "/app/loopchain/bin",
        LOOPCHAIN_CONF_DIR = "/app/loopchain/conf",
        LOOPCHAIN_DATA_DIR = "/app/loopchain/data",
        # LOOPCHAIN_LOG_DIR = "/data/",
    )
    return env_dict

def loopchain_conf_fn():       
    env_dict = config_fn()
    IMAGE_PREFIX = "loop-v1.2-rel"
    loopchain_conf_dict = dict(
        TAG = env_dict["tag"],
        TAG_SERVICE = env_dict["tag_service"],
        REPO_DOMAIN = env_dict["docker_repo"],        
        IMAGE_PEER="%s/loop_peer" % IMAGE_PREFIX,
        IMAGE_RS="%s/loop_rs" % IMAGE_PREFIX,
        IMAGE_LOG="%s/loop_logger" % IMAGE_PREFIX,
        IMAGE_QUEUE="%s/loop_queue" % IMAGE_PREFIX,
        IMAGE_RPC="%s/iconrpcserver" % IMAGE_PREFIX,
        IMAGE_ICON="%s/iconservice" % IMAGE_PREFIX,
        RADIO_STATION = "127.0.0.1",
        LOG_SERVER = "127.0.0.1",
        DNS_SERVER="8.8.8.8",
        QUEUE_SERVER = "127.0.0.1",
        LOG_PATH = "/data/loopchain/log",        

        CITIZEN_ENDPOINT='13.124.150.34:9000',        
        # CITIZEN_ENDPOINT='https://testwallet.icon.foundation',        
        # old version
        SCORE_PATH = "%s/.storage" % env_dict["LOOPCHAIN_DATA_DIR"],
        ICON_SCORE_ROOT_PATH="%s/.score_data/score" % env_dict["LOOPCHAIN_DATA_DIR"],
        ICON_SCORE_STATE_DB_ROOT_PATH="%s/.score_data/db" % env_dict["LOOPCHAIN_DATA_DIR"],       

        PUB_KEY = "%s/%s_public.der" % ( env_dict["LOOPCHAIN_CONF_DIR"], env_dict["SERVICE"] ),
        PRIV_KEY = "%s/%s_private.der" % ( env_dict["LOOPCHAIN_CONF_DIR"], env_dict["SERVICE"] ),
        GEN = "%s/%s_genesis.json" % ( env_dict["LOOPCHAIN_CONF_DIR"], env_dict["SERVICE"]  ),
        ENV_LIST_PEER = "%s/env_list.peer" % ( env_dict["LOOPCHAIN_CONF_DIR"] ),
        ENV_LIST_RS = "%s/env_list.rs" % ( env_dict["LOOPCHAIN_CONF_DIR"] ),

        CONFIGURE_CHANNEL_JSON = "%s/configure_channel.json"% ( env_dict["LOOPCHAIN_CONF_DIR"] ),
        CONFIGURE_JSON = "%s/configure.json" % ( env_dict["LOOPCHAIN_CONF_DIR"] ),

        CONFIGURE_RS_JSON = "%s/configure_rs.json" % ( env_dict["LOOPCHAIN_CONF_DIR"] ),
        CHANNEL_MANAGE_DATA_JSON = "%s/channel_manage_data.json" % ( env_dict["LOOPCHAIN_CONF_DIR"] ),

        ICON_RPCSERVER_JSON = "%s/iconrpcserver_config.json" % ( env_dict["LOOPCHAIN_CONF_DIR"] ),
        ICON_SERVICE_JSON="%s/iconservice_config.json" % ( env_dict["LOOPCHAIN_CONF_DIR"] ),
        
    )
    if 'https://' in loopchain_conf_dict["CITIZEN_ENDPOINT"]:
        print("SUBSCRIBE_USE_HTTPS \n")
        loopchain_conf_dict["SUBSCRIBE_USE_HTTPS"] = "true"

    return loopchain_conf_dict

def env_list_peer():    
    env_list_peer = dict(
        ALLOW_LOAD_SCORE_IN_DEVELOP="allow",
        LOOPCHAIN_LOG_LEVEL="DEBUG",
        LEADER_BLOCK_CREATION_LIMIT="999999",
        MONITOR_LOG="true",
        MONITOR_LOG_HOST="127.0.0.1",        
        # new version  -- OOOO
        ## 
        DEFAULT_STORAGE_PATH="/.storage",
        DEFAULT_SCORE_STORAGE_PATH="/.storage/score",
        # MONITOR_LOG="false",        
        USE_GUNICORN_HA_SERVER="true",
        MAX_BLOCK_TX_NUM="500",
        RADIO_STATION=loopchain_conf_fn()["RADIO_STATION"],
        LOG_SERVER=loopchain_conf_fn()["LOG_SERVER"],
        DNS_SERVER=loopchain_conf_fn()["DNS_SERVER"],
        QUEUE_SERVER=loopchain_conf_fn()["QUEUE_SERVER"],
        AMQP_KEY=7100,
        AMQP_TARGET=loopchain_conf_fn()["QUEUE_SERVER"],
        # DEPLOY_SCORE="score/certificate"
    )
    env_list_peer.update(loopchain_conf_fn())
    return env_list_peer

def looppeer_conf(IPADDR):
    env_dict = config_fn()
    looppeer_conf = dict({
        "VERSION": env_dict["VERSION"],
        "LOOPCHAIN_HOST": IPADDR,
        "LOOPCHAIN_DEFAULT_CHANNEL": "icon_dex",
        "PEER_NAME": "LOOPCHAIN_CTZ",
        # "MONITOR_LOG": True,
        # "MONITOR_LOG_HOST": "127.0.0.1",
        "USE_GUNICORN_HA_SERVER": True,
        ##### delete "INITIAL_GENESIS_BLOCK_DATA_FILE_PATH": "/conf/init_genesis.json",
        "CHANNEL_BUILTIN": False,
        "MAX_TX_COUNT_IN_ADDTX_LIST": 500,
        ## ADD
        "USE_EXTERNAL_SCORE": True,
        "USE_EXTERNAL_REST": True,
        "PORT_PEER": 7100,
        "AMQP_KEY": "7100",
        "AMQP_TARGET": "127.0.0.1",
        ### 
        "ALLOW_MAKE_EMPTY_BLOCK": False,
        "CHANNEL_OPTION": {
            "icon_dex": {
                "store_valid_transaction_only": True,
                "send_tx_type": 2,
                "load_cert": False,
                "consensus_cert_use": False,
                "tx_cert_use": False,
                ## ADD
                "tx_hash_version": 1,
                "genesis_tx_hash_version": 0,
                ##
                "key_load_type": 0,
                "public_path": "/resources/default_pki/public.der",
                "private_path": "/resources/default_pki/private.der",
                "private_password": env_dict["KEY_PASSWORD"],
                ## change setting!!!!
                "genesis_data_path": "/conf/init_genesis.json"
            }
        }
    })
    return looppeer_conf


def iconservice_conf():
    iconservice = {
        "log": {
                "logger": "iconservice",
                "colorLog": True,
                "level": "info",
                "filePath": "/log/iconservice.log",
                "outputType": "console|file",
                "rotate": {
                            "type": "period|bytes",
                            "period": "daily",
                            "interval": 1,
                            "backupCount": 10,
                            "maxBytes": 1048576000                            
                        }
        },
        # "scoreRootPath": ".score",
        # "stateDbRootPath": ".statedb",
        "scorePackageValidator": False,
        "channel": "icon_dex",
        "amqpKey": "7100",
        "amqpTarget": "127.0.0.1",
        # "builtinScoreOwner": "hxebf3a409845cd09dcb5af31ed5be5e34e2af9433",
        "builtinScoreOwner": "hx6e1dd0d4432620778b54b2bbc21ac3df961adf89",
        "service": {
            "fee": True,
            "audit": False
        }
    }
    return iconservice

def iconrpcserver_conf():
    iconrpcserver = {
        "log": {
                "logger": "iconrpcserver",
                    "colorLog": True,
                    "level": "info",
                    "filePath": "/log/iconrpcserver.log",
                    "outputType": "console|file",
                    "rotate": {
                                "type": "period|bytes",
                                "period": "daily",
                                "interval": 1,
                                "backupCount": 10,
                                "maxBytes": 1048576000
                            }
        },
        "channel": "icon_dex",
        "port": 9000,
        "amqpTarget": "127.0.0.1",
        "amqpKey": "7100",
        "gunicornWorkerCount": 1
    }
    loopchain_conf_dict = loopchain_conf_fn()
    if 'https://' in loopchain_conf_dict["CITIZEN_ENDPOINT"]:
        iconrpcserver["subscribeUseHttps"] = True
    return iconrpcserver
    
def env_list_rs():
    env_list_rs = dict(
        LOOPCHAIN_LOG_LEVEL="DEBUG",
        MONITOR_LOG="true",
        MONITOR_LOG_HOST="127.0.0.1",
        USE_GUNICORN_HA_SERVER="true"
    )
    return env_list_rs

def channel_manage_data_json():    
    return {
        "icon_dex": {
            "score_package": "icon/icon_dex",
            # "score_package": "loopchain/default",
            "peers": []
        }
    }

def genesis():
    genesis = dict(
        {
            "transaction_data": {
                # "nid": mainnet -> 0x1, testnet-> 0x2, default -> 0x3
                "nid": "0x3",
                "accounts": [
                    {
                        "balance": "0x2961fff8ca4a62327800000",
                        "name": "god",
                        "address": "hx5a05b58a25a1e5ea0f1d5715e1f655dffc1fb30a"
                    },
                    {
                        "balance": "0x0",
                        "name": "treasury",
                        "address": "hx1000000000000000000000000000000000000000"
                    },
                    {
                        "balance": "0x2961fff8ca4a62327800000",
                        "name": "test_1",
                        "address": "hx6e1dd0d4432620778b54b2bbc21ac3df961adf89"
                    }
                ],
                "message": "SoloNet"
            }
        }
    )
    return genesis


def configure_rs_json():
    dict_config = config_fn()
    json = {
        "CHANNEL_MANAGE_DATA_PATH": "/loopchain/channel_manage_data.json",
        "ENABLE_CHANNEL_AUTH": False,
        "SLEEP_SECONDS_IN_RADIOSTATION_HEARTBEAT": 30,
        "NO_RESPONSE_COUNT_ALLOW_BY_HEARTBEAT": 2,
        "LOOPCHAIN_DEFAULT_CHANNEL": "icon_dex",
        "CHANNEL_OPTION": {
            "icon_dex": {
                "store_valid_transaction_only": True,
                "send_tx_type": 2,
                "load_cert": False,
                "consensus_cert_use": False,
                "tx_cert_use": False,
                "key_load_type": 0,
                "public_path": "./resources/default_pki/private.der",
                "tx_hash_version": 1,
                # "genesis_tx_hash_version": 1,               
                "genesis_tx_hash_version": 0,               
                "private_password": dict_config["KEY_PASSWORD"],
            }
        }
    }
    return json


if __name__ == '__main__':    
    main()
