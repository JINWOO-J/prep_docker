def config():
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

def loopchain_conf():       
    env_dict = config()
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
        # CITIZEN_ENDPOINT='',
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
        RADIO_STATION=loopchain_conf()["RADIO_STATION"],
        LOG_SERVER=loopchain_conf()["LOG_SERVER"],
        DNS_SERVER=loopchain_conf()["DNS_SERVER"],
        QUEUE_SERVER=loopchain_conf()["QUEUE_SERVER"],
        AMQP_KEY=7100,
        AMQP_TARGET=loopchain_conf()["QUEUE_SERVER"],
        # DEPLOY_SCORE="score/certificate"
    )
    env_list_peer.update(loopchain_conf())
    return env_list_peer

def looppeer_conf(IPADDR):
    env_dict = config()
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
    loopchain_conf_dict = loopchain_conf()
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
                "message": "DevNet"
            }
        }
    )
    return genesis


def configure_rs_json():
    dict_config = config()
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

