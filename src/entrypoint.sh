#!/bin/bash
shopt -s expand_aliases
#export CURL_OPTION=${CURL_OPTION:-"-vvv -s -S --fail --max-time 30"} #default curl options
alias curl="curl -s -S --fail --max-time 30"
export EXT_IPADDR=${EXT_IPADDR:-$(curl http://checkip.amazonaws.com)} # Getting external IP address
export IPADDR=${IPADDR:-"$EXT_IPADDR"}  # Setting the IP address 
export LOCAL_TEST=${LOCAL_TEST:-"false"}
if [[ ${LOCAL_TEST} == "true" ]]; then
    HOST_IP=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
    IPADDR=$HOST_IP
    echo  "===== LOCAL TEST = $IPADDR  ====="
fi

export TZ=${TZ:-"Asia/Seoul"}  # Setting the TimeZone Environment #[List of TZ name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
export NETWORK_ENV=${NETWORK_ENV:-"PREP-TestNet"}  # Network Environment name  # mainnet or PREP-TestNet
export SERVICE=${SERVICE:-"zicon"}               # Service Name # mainnet/testnet/zicon
export ENDPOINT_URL=${ENDPOINT_URL:-""}      #  ENDPOINT API URI #URI
export FIND_NEIGHBOR=${FIND_NEIGHBOR:-"true"}          # Find fastest neighborhood PRep
export FIND_NEIGHBOR_COUNT=${FIND_NEIGHBOR_COUNT:-5}   # neighborhood count
export FIND_NEIGHBOR_OPTION=${FIND_NEIGHBOR_OPTION:-""}   # neighborhood option # -t (main|sub|all)

shopt -s nocasematch # enable
if [[ "x${ENDPOINT_URL}" == "x" ]]; then
    if [[ "$NETWORK_ENV" == "mainnet" ]]; then
        ENDPOINT_URL="https://ctz.solidwallet.io"
        SERVICE="mainnet"
        NETWORK_ENV="mainnet"
    elif [[ "$NETWORK_ENV" == "testnet" ]]; then
        ENDPOINT_URL="https://test-ctz.solidwallet.io"
        SERVICE="testnet"
        NETWORK_ENV="testnet"
#    elif [[ $(echo $SERVICE | grep -i "icon" | wc -l) ]];then
    elif echo "${SERVICE}" | grep -q "icon" ;then
        ENDPOINT_URL="https://${SERVICE}.net.solidwallet.io"
    fi
fi
shopt -u nocasematch # disable

export SERVICE_API=${SERVICE_API:-"${ENDPOINT_URL}/api/v3"} # SERVICE_API URI #URI
export NTP_SERVER=${NTP_SERVER:-"time.google.com"}     # NTP SERVER ADDRESS
export NTP_REFRESH_TIME=${NTP_REFRESH_TIME:-"21600"}   # NTP refresh time
export USE_NTP_SYNC=${USE_NTP_SYNC:-"true"}            # whether use ntp or not # boolean (true/false)
export FASTEST_START=${FASTEST_START:-"no"}            # It can be restored from Snapshot DB. # yes/no
export FASTEST_START_POINT=${FASTEST_START_POINT:-""}
export GENESIS_NODE=${GENESIS_NODE:-"false"}

export DEFAULT_PATH=${DEFAULT_PATH:-"/data/${NETWORK_ENV}"}  # Setting the Default Root PATH
export DEFAULT_LOG_PATH=${DEFAULT_LOG_PATH:-"${DEFAULT_PATH}/log"} # Setting the logging path
export DEFAULT_STORAGE_PATH=${DEFAULT_STORAGE_PATH:-"${DEFAULT_PATH}/.storage"} # block DB will be stored

export USE_NAT=${USE_NAT:-"no"}  # if you want to use NAT Network
export NETWORK_NAME=${NETWORK_NAME:-""}
export VIEW_CONFIG=${VIEW_CONFIG:-"false"}  # for check deployment state # boolean (true/false)
export AMQP_TARGET=${AMQP_TARGET:-"127.0.0.1"}
export USE_EXTERNAL_MQ=${USE_EXTERNAL_MQ:-"false"}
export USE_MQ_ADMIN=${USE_MQ_ADMIN:-"false"} # Enable RabbitMQ management Web interface.The management UI can be accessed  using a Web browser at http://{node-hostname}:15672/. For example, for a node running on a machine with the hostname of prep-node, it can be accessed at http://prepnode:15672/  # boolean (true/false)
export MQ_ADMIN=${MQ_ADMIN:-"admin"}          # RabbitMQ management username
export MQ_PASSWORD=${MQ_PASSWORD:-"iamicon"}     # RabbitMQ management password

export LOOPCHAIN_LOG_LEVEL=${LOOPCHAIN_LOG_LEVEL:-"INFO"}  # loopchain log level # DEBUG, INFO, WARNING, ERROR
export ICON_LOG_LEVEL=${ICON_LOG_LEVEL:-"INFO"}   # iconservice log level # DEBUG, INFO, WARNING, ERROR
export LOG_OUTPUT_TYPE=${LOG_OUTPUT_TYPE:-"file"} # loopchain's output log type # file, console, file|console
export outputType=${outputType:-"$LOG_OUTPUT_TYPE"}  #iconservice's output log type # file, console, file|console

export FIRST_PEER=${FIRST_PEER:-"false"}    # for testnet
export NEWRELIC_LICENSE=${NEWRELIC_LICENSE:-""} # for testnet
export CONF_PATH=${CONF_PATH:-"/${APP_DIR}/conf"} # Setting the configure file path
export CERT_PATH=${CERT_PATH:-"/${APP_DIR}/cert"} # Setting the certificate key file path

export ICON_NID=${ICON_NID:-"0x50"}  # Setting the ICON Network ID number
export CREP_ROOT_HASH=${CREP_ROOT_HASH:-""}
export ALLOW_MAKE_EMPTY_BLOCK=${ALLOW_MAKE_EMPTY_BLOCK:-"true"}
export CHANNEL_BUILTIN=${CHANNEL_BUILTIN:-"true"} # boolean (true/false)
export PEER_NAME=${PEER_NAME:-$(uname)}
export PRIVATE_KEY_FILENAME=${PRIVATE_KEY_FILENAME:-"YOUR_KEYSTORE_FILENAME"} # YOUR_KEYSTORE or YOUR_CERTKEY FILENAME # YOUR_KEYSTORE or YOUR_CERTKEY FILENAME

export PRIVATE_PATH=${PRIVATE_PATH:-"${CERT_PATH}/${PRIVATE_KEY_FILENAME}"} # public cert key or keystore file location
export PRIVATE_PASSWORD=${PRIVATE_PASSWORD:-"test"}  # private cert key  or keystore file password

if [[ "${NETWORK_ENV}" == "PREP-TestNet" ]];then
    export PRIVATE_PATH=${PRIVATE_PATH:-"${CERT_PATH}/${IPADDR}_private.der"} # private cert key or keystore file location
    export PRIVATE_PASSWORD=${PRIVATE_PASSWORD:-"test"}  # private cert key  or keystore file password
fi

export LOAD_PEERS_FROM_IISS=${LOAD_PEERS_FROM_IISS:-"true"}
export CHANNEL_MANAGE_DATA_PATH=${CHANNEL_MANAGE_DATA_PATH:-"${CONF_PATH}/channel_manange_data.json"}
export CONFIG_API_SERVER=${CONFIG_API_SERVER:-"https://download.solidwallet.io"}
export GENESIS_DATA_PATH=${GENESIS_DATA_PATH:-"${CONF_PATH}/genesis.json"}
export BLOCK_VERSIONS=${BLOCK_VERSIONS:-""}
export SWITCH_BH_VERSION3=${SWITCH_BH_VERSION3:-""}
export SWITCH_BH_VERSION4=${SWITCH_BH_VERSION4:-""}
export SWITCH_BH_VERSION5=${SWITCH_BH_VERSION5:-""}

export RADIOSTATIONS=${RADIOSTATIONS:-""}
export SHUTDOWN_TIMER=${SHUTDOWN_TIMER:-7200} # SHUTDOWN_TIMER for citizen
export SUBSCRIBE_LIMIT=${SUBSCRIBE_LIMIT:-60}
export TIMEOUT_FOR_LEADER_COMPLAIN=${TIMEOUT_FOR_LEADER_COMPLAIN:-60}

export configure_json=${configure_json:-"${CONF_PATH}/configure.json"}
export iconservice_json=${iconservice_json:-"${CONF_PATH}/iconservice.json"}
export iconrpcserver_json=${iconrpcserver_json:-"${CONF_PATH}/iconrpcserver.json"}

export FORCE_RUN_MODE=${FORCE_RUN_MODE:-""} # Setting the loopchain running parameter e.g. if FORCE_RUN_MODE is `-r citizen` then loop `-r citizen`

#Temporary option
export ICON_REVISION=${ICON_REVISION:-"5"}
export ROLE_SWITCH_BLOCK_HEIGHT=${ROLE_SWITCH_BLOCK_HEIGHT:-"1"}

export mainPRepCount=${mainPRepCount:-"22"}
export mainAndSubPRepCount=${mainAndSubPRepCount:-"100"}
export decentralizeTrigger=${decentralizeTrigger:-"0.002"}
export iissCalculatePeriod=${iissCalculatePeriod:-"1800"} # origin value is 43200
export termPeriod=${termPeriod:-"1800"} # origin value is 43120
export blockValidationPenaltyThreshold=${blockValidationPenaltyThreshold:-"66000000"}
export lowProductivityPenaltyThreshold=${lowProductivityPenaltyThreshold:-"85"}
export score_fee=${score_fee:-"true"}
export score_audit=${score_audit:-"true"}
export scoreRootPath=${scoreRootPath:-"${DEFAULT_PATH}/.score_data/score"}
export stateDbRootPath=${stateDbRootPath:-"${DEFAULT_PATH}/.score_data/db"}
export penaltyGracePeriod=${penaltyGracePeriod:-86400}

export STAKE_LOCK_MAX=${STAKE_LOCK_MAX:-""}
export STAKE_LOCK_MIN=${STAKE_LOCK_MIN:-""}

export RPC_PORT=${PORT:-"9000"} # Choose a RPC service port
export RPC_WORKER=${RPC_WORKER:-"3"} #Setting the number of RPC workers
export RPC_GRACEFUL_TIMEOUT=${RPC_GRACEFUL_TIMEOUT:-"0"} # rpc graceful timeout

export USE_PROC_HEALTH_CHECK=${USE_PROC_HEALTH_CHECK:-"yes"}
export USE_API_HEALTH_CHECK=${USE_API_HEALTH_CHECK:-"yes"}
export USE_HELL_CHECK=${USE_HELL_CHECK:-"yes"}
export HEALTH_CHECK_INTERVAL=${HEALTH_CHECK_INTERVAL:-"30"}  # Trigger if greater than 1
export ERROR_LIMIT=${ERROR_LIMIT:-6}
export HELL_LIMIT=${HELL_LIMIT:-300}

export USE_SLACK=${USE_SLACK:-"no"}  #  if you want to use the slack
export SLACK_URL=${SLACK_URL:-""}    #  slack's webhook URL
export SLACK_PREFIX=${SLACK_PREFIX:-""} # slack's prefix header message
export IS_BROADCAST_MULTIPROCESSING=${IS_BROADCAST_MULTIPROCESSING:-"false"}
export IS_DOWNLOAD_CERT=${IS_DOWNLOAD_CERT:-"false"}
export IS_AUTOGEN_CERT=${IS_AUTOGEN_CERT:-"false"} # auto generate cert key # true, false
export IS_COMPRESS_LOG=${IS_COMPRESS_LOG:-"false"} # auto compress loopchain and icon log via crontab # true, false
export IS_WRITE_BH=${IS_WRITE_BH:-"true"} # write BH, TX, UX_TX, state on booting log  # true, false
# export LEADER_COMPLAIN_RATIO=${LEADER_COMPLAIN_RATIO:-"0.67"}
export USER_DEFINED_ENV=${USER_DEFINED_ENV:-""}

#for bash prompt without entrypoint

#$@ # instead of exec $@
#echo $@
#exec $@

TIME_1=$(date +%s)
sleep 5
TIME_2=$(date +%s)

DIFF=$((${TIME_2}-${TIME_1}))
echo $DIFF



function getBlockCheck(){
    if [[ ${USE_HELL_CHECK} == "yes" ]]; then
        ERROR_DIR="/.health_check"
        ERROR_COUNT_FILE="${ERROR_DIR}/blockcount"
        NOW_COUNT_FILE="${ERROR_DIR}/blockcount_now"
        PREV_COUNT_FILE="${ERROR_DIR}/blockcount_prev"
        RESULT=""
        if [[ ${IS_WRITE_BH} == "true" ]]; then
#            read blockheight total_tx unconfirmed_tx state < <(curl "localhost:${RPC_PORT}/api/v1/status/peer" | \
#                jq  -r '[.block_height,.total_tx,.unconfirmed_tx,.state] | @tsv')
            RESULT=$(curl "localhost:${RPC_PORT}/api/v1/status/peer")
            if jq -e . >/dev/null 2>&1 <<< "${RESULT}"; then
                blockheight=$(echo ${RESULT} | jq -r .block_height)
                total_tx=$(echo ${RESULT} | jq -r .total_tx)
                unconfirmed_tx=$(echo ${RESULT} | jq -r .unconfirmed_tx)
                state=$(echo ${RESULT} | jq -r .state)
                CPrint "BlockCheck: BH=${blockheight}, TX=${total_tx}, UN_TX=${unconfirmed_tx}, state=${state}"
            else
                CPrint "[ERR] get status"
            fi
        else
            blockheight=$(curl "localhost:${RPC_PORT}/api/v1/status/peer" | jq -r .block_height)
        fi

        if [[ ! -d "$ERROR_DIR" ]]; then
            mkdir -p ${ERROR_DIR}
        fi
        touch "${NOW_COUNT_FILE}" "${PREV_COUNT_FILE}"
        echo "${blockheight}" > ${NOW_COUNT_FILE}
        PREV_ERROR_COUNT=$(cat ${PREV_COUNT_FILE})
        if [[ "${blockheight}" -eq ${PREV_ERROR_COUNT} ]];then
            if [[ "${blockheight}" -ge 1 ]];then
                echo "${blockheight}"  >> ${ERROR_COUNT_FILE}
                ERROR_COUNT=$(grep -c "" "${ERROR_COUNT_FILE}")

                if [[ ${ERROR_COUNT} -ge 3 ]]; then
                    CPrint "[DELAY] PREV_BH=${PREV_ERROR_COUNT}, NOW_BH=${blockheight}, ERROR_COUNT=${ERROR_COUNT}, HELL_LIMIT=${HELL_LIMIT}"
                fi

                if [[ ${ERROR_COUNT} -ge ${HELL_LIMIT} ]];then
                    CPrint "[FAIL] (${ERROR_COUNT}/${HELL_LIMIT}) (HELL) It will be terminated / reason: Hell  "
                    post_to_slack "[FAIL] (${ERROR_COUNT}/${HELL_LIMIT}) It will be terminated / reason: Hell "
                    if [[ -d ${ERROR_DIR} ]]; then
                        rm -f ${ERROR_DIR}/*
                    fi
                    exit 127;
                fi
            fi
        else
            cp ${NOW_COUNT_FILE} ${PREV_COUNT_FILE}
            echo "" > ${ERROR_COUNT_FILE}
        fi
    fi
}

function post_to_slack () {
  #escapedText=$(echo $1 | sed 's/"/\"/g' | sed "s/'/\'/g" | sed 's/(?(?=\\n)[^\\n]|\\)/\\\\/g')
    escapedText=$(echo "$1" | sed 's/"/\"/g' | sed "s/'/\'/g")
    SLACK_MESSAGE="\`\`\`${SLACK_PREFIX}[$(date '+%Y-%m-%d %T.%3N')] ${HOSTNAME} ${escapedText}\`\`\`"
    #  SLACK_URL=$2
    case "$2" in
    INFO)
        SLACK_ICON=':slack:'
        ;;
    WARNING)
        SLACK_ICON=':warning:'
        ;;
    ERROR)
        SLACK_ICON=':bangbang:'
        ;;
    *)
        SLACK_ICON=':slack:'
        ;;
    esac
    if [[ "${USE_SLACK}" == "yes" ]]; then
        if [[ "${SLACK_URL}" ]]; then
            curl -X POST --data-urlencode "payload={\"text\": \"${SLACK_ICON} ${SLACK_MESSAGE}\"}" "${SLACK_URL}"
        else
            CPrint "[FAIL] SLACK_URL not found" "RED"
        fi
    fi
}
function logging() {
    MSG=$1
    APPEND_STRING=${2:-"\n"}
    LOG_TYPE=${3:-"booting"}
    LOG_PATH=${4:-"$DEFAULT_LOG_PATH"}
    LOG_DATE=$(date +%Y%m%d)
    if [[ ! -e "$LOG_PATH" ]];then
        mkdir -p "$LOG_PATH"
    fi
    if [[ ${APPEND_STRING} == "\n" ]] ;then
        echo -ne "[$(date '+%Y-%m-%d %T.%3N')] $MSG ${APPEND_STRING}" >> "${LOG_PATH}/${LOG_TYPE}_${LOG_DATE}.log"
    else
        echo -ne "$MSG ${APPEND_STRING}" >> "${LOG_PATH}/${LOG_TYPE}_${LOG_DATE}.log"
    fi
}

function returnErrorCount(){
    MSG=${1}
    ERROR_KEY=${2:-"default"}
    ACTION=${3:-"down"}

    ERROR_KEY=$(echo "${ERROR_KEY}" | sed 's/\//_/g')
    ERROR_DIR="/.health_check"
    if [[ ! -d "$ERROR_DIR" ]]; then
        mkdir -p ${ERROR_DIR}
    fi
    ERROR_COUNT_FILE="${ERROR_DIR}/errorCount.${ERROR_KEY}"
    ## for debugging, it wll be remove
    ####CPrint "returnErrorCount(), KEY='${ERROR_KEY}', ACT='${ACTION}', MSG='${MSG}' "

    if [[ "${MSG}"  && "${ACTION}" == "down" ]]; then
        echo "${MSG}" >> "${ERROR_COUNT_FILE}"
        ERROR_COUNT=$(< "${ERROR_COUNT_FILE}" grep -v grep | grep -c "${MSG}")
        if [[ ${ERROR_COUNT} -ge ${ERROR_LIMIT} ]];then
            CPrint "[FAIL] (${ERROR_COUNT}/${ERROR_LIMIT}) It will be terminated / reason: ${MSG} "
            post_to_slack "[FAIL] (${ERROR_COUNT}/${ERROR_LIMIT}) It will be terminated / reason: ${MSG} "
            if [[ -d ${ERROR_DIR} ]]; then
                rm -f ${ERROR_DIR}/*
            fi
            exit 127;
        fi
    else
        if [[ -f "${ERROR_COUNT_FILE}" ]];then
            logging "Reset count ${ERROR_COUNT_FILE}"
            rm -f "${ERROR_COUNT_FILE}"
        fi
    fi
}

function CPrint {
    MSG=$1
    COLOR=$2
    if [[ "$COLOR" == "" ]];then
        MSG=$*
    fi
    DATE=$(date '+%Y-%m-%d %T.%3N')
    RED='\e[0;91m'
    GREEN='\e[0;92m'
    WHITE='\e[97m'
    BOLD_WHITE='\e[1;37m'
    RESET='\e[0m'  # RESET

    if [[ "$COLOR" == "RED" ]];then
        MSG="[ERROR] $MSG"
    fi

    case $2 in
        "RED")
            printf "%b %50s %b \n" "${RED}" "[$DATE] $MSG" "${RESET}" ;;
        "GREEN")
            printf "%b  %50s %b \n" "${GREEN}" "[$DATE] $MSG" "${RESET}" ;;
        "WHITE")
            printf "%b  %50s %b \n" "${WHITE}" "[$DATE] $MSG" "${RESET}" ;;
        *)
            printf "%b  %s %b \n" "${BOLD_WHITE}" "[$DATE] $MSG" "${RESET}" ;;
    esac

    logging "$MSG"
}

function PrintOK() {
    RESET='\e[0m'  # RESET
    MSG=${1}
    CHECK=${2:-0}
    PRINT_VIEW=${3:-"$VIEW_CONFIG"}
    if [[ ${CHECK} == 0 ]];
    then
        if [[ "$PRINT_VIEW" == "true" ]];then
            CPrint "[OK] CHECK=${CHECK}, ${MSG}" "GREEN"
        fi
    else
        CPrint "[FAIL] CHECK=${CHECK}, ${MSG}" "RED"
        logging "Stopped script"
        exit 0;
    fi
}
function download_file() {
    DOWNLOAD_URL=$1
    DOWNLOAD_DEST=$2
    DOWN_STAT=$(curl  -w "%{http_code}" -so "${DOWNLOAD_DEST}" "${DOWNLOAD_URL}")
    if [[ "$DOWN_STAT" == "200" ]];then
        PrintOK "Download ${DOWNLOAD_URL}" $?
    else
        CPrint "Download Failed - ${DOWNLOAD_URL} status_code=$DOWN_STAT " "RED"
        if [[ "$DOWNLOAD_URL" == *"der" ]];then
            CPrint "Unauthorized IP address, Please contact our support team" "RED"
            CPrint "Your External IP:${EXT_IPADDR} / Your Enviroment IPADDR:${IPADDR}" "RED"
        fi
        rm -f "${DOWNLOAD_DEST}"
        exit 0;
    fi
}
function check_valid_ip(){
    local  ip=$1
    local  stat=1
    if [[ ${ip} =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        IFS='.' read -r -a ip_array <<< "$ip"
        [[ ${ip_array[0]} -le 255 && ${ip_array[1]} -le 255 && ${ip_array[2]} -le 255 && ${ip_array[3]} -le 255 ]]
        stat=$?
    fi
    PrintOK "Check valid IPaddr -> $1 " $stat
    return $stat
}

function int_check(){
    value=$1
    r=${value#-}
    r=${value//[0-9]/}
    if [[ -z "${r}" ]]; then
        echo true
    else
        echo false
    fi
}

function filetype_check() {
    filename=$1
    type=$(file "${filename}" | cut -d ":" -f 2)
    echo "${type}"
}

function validationViewConfig() {
    filename=$1
    if [[ -f "${filename}" ]]; then
        jq -C . "$filename" 1>/dev/null
        if [[ "$VIEW_CONFIG" == "true" ]]; then
            json=$(jq  . "${filename}")
            CPrint "$filename detail - ${json}"
        fi
        FILESIZE=$(stat --printf="%s" "$filename")
        if [[ ${FILESIZE} == 0 ]];then
            CPrint "[FAIL] $filename size=$FILESIZE " "RED"
            exit 0
        fi
        PrintOK "Check config -> filename=$filename,size=$FILESIZE" $?
    fi
}

function find_neighbor_func(){
    WRITE_OPTION=${1:-""}
    if [[ "${FIND_NEIGHBOR}" == "true" ]] && [[ -n "${ENDPOINT_URL}" ]]; then
        FIND_NEIGHBOR_HOSTS=$(/src/find_neighbor.py ${ENDPOINT_URL} ${FIND_NEIGHBOR_COUNT} ${WRITE_OPTION} ${FIND_NEIGHBOR_OPTION})
        CPrint "== ${FIND_NEIGHBOR_HOSTS}"
    fi
}

function ntp_check(){
    if [[ -z "${NTP_FIRST}" ]];then
        NTP_FIRST=1
    else
        NTP_FIRST=0
    fi
    if [[ ${NTP_FIRST} -eq 1 ]];then
        CPrint "Time synchronization with NTP / NTP SERVER: ${NTP_SERVER} - ${NTP_FIRST}"
    fi
    if ntpdate -s "${NTP_SERVER}"; then
        if [[ "$VIEW_CONFIG" == "true" || ${NTP_FIRST} -eq 1 ]]; then
            CPrint "Success Time Synchronization!!" "GREEN"
        fi
    else
        ## AWS NTP NTP_SERVER
        if ntpdate -s "169.254.169.123" ; then
            if [[ "$VIEW_CONFIG" == "true" || ${NTP_FIRST} -eq 1 ]]; then
                CPrint "Success Time Synchronization!! with AWS NTP Server" "GREEN"
            fi
        else
            CPrint "[FAIL] Time Synchronization!!" "RED"
        fi
    fi
}

function autogen_certkey(){
    FILENAME=${1:-"$PRIVATE_PATH"}
    openssl ecparam -genkey -name secp256k1 | openssl ec -aes-256-cbc -out "${FILENAME}" -passout pass:"${PRIVATE_PASSWORD}"
    CPrint "Generate a key file $FILENAME"
    PrintOK "Generate a private key " $?
#    openssl ec -in ${FILENAME}  -pubout -out ${PUBLIC_PATH} -passin pass:${PRIVATE_PASSWORD}
#    PrintOK "Generate public key" $?
}

function progress(){
    PROGRESS_STRING=${1:-"."}
    ENTER_TIME=${2:-10}
    UNIXTIME_NOW=$(date +%s)
    mod=$((UNIXTIME_NOW % ENTER_TIME))
    if [[ ${mod} == 0 ]]; then
        printf "\n"
    else
        printf "%s " "${PROGRESS_STRING}"
        logging "${PROGRESS_STRING}" " "
    fi
}

function check_var(){
    VAR_NAME=${1:-""}
    VAR_VALUE=${2:-""}
    if [[ -z "$VAR_VALUE" ]]; then
        CPrint "${VAR_NAME} environment is NULL ", "RED"
        exit 0;
    fi
}

if [[ "${IS_AUTOGEN_CERT}" == "true" ]]; then
    CPrint "Using auto generataion cert key"
    PRIVATE_PATH="${CERT_PATH}/autogen_cert.pem"
    if [[ ! -f "${PRIVATE_PATH}" ]]  ; then
        autogen_certkey "${PRIVATE_PATH}"
    fi
fi

mkdir -p "${DEFAULT_PATH}"

check_valid_ip "$IPADDR"

CPrint "Your IP: $IPADDR"
CPrint "RPC_PORT: $RPC_PORT / RPC_WORKER: $RPC_WORKER "
CPrint "DEFAULT_PATH=$DEFAULT_PATH in Docker Container"
CPrint "DEFAULT_LOG_PATH=${DEFAULT_LOG_PATH}"
CPrint "DEFAULT_STORAGE_PATH=${DEFAULT_STORAGE_PATH}"
CPrint "scoreRootPath=${scoreRootPath}"
CPrint "stateDbRootPath=${stateDbRootPath}"

shopt -s nocasematch
if [[ "${NETWORK_ENV}" == *"testnet"* ]];then
    CPrint "GENESIS_DATA_PATH=${GENESIS_DATA_PATH}"
    GENESIS_DATA_PATH="${CONF_PATH}/genesis_testnet.json"
fi

CPrint "P-REP package version info - ${APP_VERSION}"
PIP_LIST=$(pip list | grep -E "loopchain|icon" | tr -d '')
CPrint "$PIP_LIST"

## set builtinScoreOwner and block setting
if [[ "$NETWORK_ENV" == "mainnet" ]]; then
    builtinScoreOwner="hx677133298ed5319607a321a38169031a8867085c"
    SERVICE="mainnet"
    iissCalculatePeriod=43200
    termPeriod=43120
    blockValidationPenaltyThreshold=660
    CREP_ROOT_HASH="0xd421ad83f81a31abd7f6813bb6a3b92fa547bdb6d5abc98d2d0852c1a97bcca5"
    SWITCH_BH_VERSION3=10324749
    SWITCH_BH_VERSION4=12640761
    SWITCH_BH_VERSION5=14473622
    jq '.CHANNEL_OPTION.icon_dex.hash_versions.genesis = 0' "$configure_json" | sponge "$configure_json"

elif [[ "$NETWORK_ENV" == "testnet" ]]; then
    builtinScoreOwner="hxba096790caa1804a8828939839a901a5978020a7"
    SERVICE="testnet"
    mainPRepCount=7
    iissCalculatePeriod=43200
    termPeriod=43120
    blockValidationPenaltyThreshold=660
    CREP_ROOT_HASH="0x38ec404f0d0d90a9a8586eccf89e3e78de0d3c7580063b20823308e7f722cd12"
    SWITCH_BH_VERSION3=1
    SWITCH_BH_VERSION4=10
    SWITCH_BH_VERSION5=524360
else
    if [[ "$SERVICE" == "zicon" ]]; then
        iissCalculatePeriod=1800
        termPeriod=1800
        CREP_ROOT_HASH="0x9718f5d6d6ddb77f547ecc7113c8f1bad1bf46220512fbde356eee74a90ba47c"
        SWITCH_BH_VERSION3=1
        SWITCH_BH_VERSION4=1587271
        SWITCH_BH_VERSION5=3077345
    fi

    builtinScoreOwner="hx6e1dd0d4432620778b54b2bbc21ac3df961adf89"
    score_audit="false"
    if [[ ! -f ${PRIVATE_PATH} ]]; then
        if [[ $IS_DOWNLOAD_CERT == "true" ]]; then
            CPrint "Download key file - ${PRIVATE_PATH}"
            download_file "$CONFIG_API_SERVER/cert/${IPADDR}_private.der" "${PRIVATE_PATH}"
        else
            CPrint "Key file not found - PRIVATE_PATH=${PRIVATE_PATH} , PRIVATE_KEY_FILENAME=${PRIVATE_KEY_FILENAME}" "RED"
#            exit 127;
        fi
    fi

    if [[ ${GENESIS_NODE} == "true" ]]; then
        if [[ -f ${CHANNEL_MANAGE_DATA_PATH} ]]; then
            CPrint "Already channel_manage_data.json ${CHANNEL_MANAGE_DATA_PATH}" "green"
        else
            download_file "$CONFIG_API_SERVER/conf/${SERVICE}_channel_manage_data.json" "$CHANNEL_MANAGE_DATA_PATH"
        fi
    fi
fi

CPrint "NETWORK_ENV=${NETWORK_ENV}, SERVICE=${SERVICE}, ENDPOINT_URL=${ENDPOINT_URL}, SERVICE_API=${SERVICE_API}"

for mandatory_var in "SERVICE" "NETWORK_ENV" "ENDPOINT_URL" "SERVICE_API";
do
    check_var "${mandatory_var}" "${!mandatory_var}"
done


if [[ "x${CREP_ROOT_HASH}" != "x" ]]; then
    jq --arg CREP_ROOT_HASH "$CREP_ROOT_HASH" '.CHANNEL_OPTION.icon_dex.crep_root_hash = "\($CREP_ROOT_HASH)"' "$configure_json"| sponge "$configure_json"
fi

if [[ ${NETWORK_ENV} == "mainnet" || ${NETWORK_ENV} == "testnet" ]];then
    if [[ ! -f "${PRIVATE_PATH}" ]]; then
        CPrint "Keystore file not found -> '${PRIVATE_PATH}'" "RED"
        exit 127;
#        PRIVATE_PATH="${CERT_PATH}/autogen_cert.pem"
#        autogen_certkey "${PRIVATE_PATH}"
    else
        PRIVATE_KEY=$(ls "${PRIVATE_PATH}")
        CPrint "Already cert keys= ${PRIVATE_KEY}"
    fi
fi


PEER_ID=$(/src/getPeerID.py "${PRIVATE_PATH}" "${PRIVATE_PASSWORD}" 2>&1)
PrintOK "Peer ID: ${PEER_ID}" $?
CPrint "Peer ID: ${PEER_ID}"

if [[ "${VIEW_CONFIG}" == "true" ]]; then
    CPrint "builtinScoreOwner = $builtinScoreOwner"
fi

if  [[ "${USE_NAT}" == "yes" ]]; then
    jq -M 'del(.LOOPCHAIN_HOST)' "$configure_json"| sponge "$configure_json"
else
    jq --arg IPADDR "$IPADDR" '.LOOPCHAIN_HOST = "\($IPADDR)"' "$configure_json"| sponge "$configure_json"
fi
jq --argjson SUBSCRIBE_LIMIT "$SUBSCRIBE_LIMIT" '.SUBSCRIBE_LIMIT = $SUBSCRIBE_LIMIT' "$configure_json"| sponge "$configure_json"
jq --argjson SHUTDOWN_TIMER "$SHUTDOWN_TIMER" '.SHUTDOWN_TIMER = $SHUTDOWN_TIMER' "$configure_json"| sponge "$configure_json"

if [[ -n $SWITCH_BH_VERSION3 ]]; then
    CPrint "SWITCH_BH_VERSION3 = ${SWITCH_BH_VERSION3}"
    jq --argjson SWITCH_BH_VERSION3 "$SWITCH_BH_VERSION3" '.CHANNEL_OPTION.icon_dex.block_versions."0.3" = $SWITCH_BH_VERSION3' "$configure_json"| sponge "$configure_json"
fi

if [[ -n $SWITCH_BH_VERSION4 ]]; then
    CPrint "SWITCH_BH_VERSION4 = ${SWITCH_BH_VERSION4}"
    jq --argjson SWITCH_BH_VERSION4 "$SWITCH_BH_VERSION4" '.CHANNEL_OPTION.icon_dex.block_versions."0.4" = $SWITCH_BH_VERSION4' "$configure_json"| sponge "$configure_json"
fi

if [[ -n $SWITCH_BH_VERSION5 ]]; then
    CPrint "SWITCH_BH_VERSION5 = ${SWITCH_BH_VERSION5}"
    jq --argjson SWITCH_BH_VERSION5 "$SWITCH_BH_VERSION5" '.CHANNEL_OPTION.icon_dex.block_versions."0.5" = $SWITCH_BH_VERSION5' "$configure_json"| sponge "$configure_json"
fi

# jq --arg LEADER_COMPLAIN_RATIO "$LEADER_COMPLAIN_RATIO" '.LEADER_COMPLAIN_RATIO = "\($LEADER_COMPLAIN_RATIO)"' $configure_json| sponge $configure_json
jq --arg DEFAULT_STORAGE_PATH "$DEFAULT_STORAGE_PATH" '.DEFAULT_STORAGE_PATH = "\($DEFAULT_STORAGE_PATH)"' "$configure_json"| sponge "$configure_json"
jq --arg LOOPCHAIN_LOG_LEVEL "$LOOPCHAIN_LOG_LEVEL" '.LOOPCHAIN_LOG_LEVEL = "\($LOOPCHAIN_LOG_LEVEL)"' "$configure_json"| sponge "$configure_json"
jq --argjson TIMEOUT_FOR_LEADER_COMPLAIN "$TIMEOUT_FOR_LEADER_COMPLAIN" '.TIMEOUT_FOR_LEADER_COMPLAIN = $TIMEOUT_FOR_LEADER_COMPLAIN' "$configure_json"| sponge "$configure_json"

jq --arg LOG_FILE_LOCATION "$DEFAULT_LOG_PATH" '.LOG_FILE_LOCATION = "\($LOG_FILE_LOCATION)"' "$configure_json"| sponge "$configure_json"
jq --arg LOG_OUTPUT_TYPE "$LOG_OUTPUT_TYPE" '.LOG_OUTPUT_TYPE = "\($LOG_OUTPUT_TYPE)"' "$configure_json"| sponge "$configure_json"

jq --arg PRIVATE_PATH "$PRIVATE_PATH" '.PRIVATE_PATH = "\($PRIVATE_PATH)"' "$configure_json"| sponge "$configure_json"
jq --arg PRIVATE_PASSWORD "$PRIVATE_PASSWORD" '.PRIVATE_PASSWORD = "\($PRIVATE_PASSWORD)"' "$configure_json"| sponge "$configure_json"
jq --arg GENESIS_DATA_PATH "$GENESIS_DATA_PATH" '.CHANNEL_OPTION.icon_dex.genesis_data_path = "\($GENESIS_DATA_PATH)"' "$configure_json"| sponge "$configure_json"
jq --arg ICON_NID "$ICON_NID"  '.transaction_data.nid = "\($ICON_NID)"' "$GENESIS_DATA_PATH"| sponge "$GENESIS_DATA_PATH"

jq --argjson LOAD_PEERS_FROM_IISS "$LOAD_PEERS_FROM_IISS" '.LOAD_PEERS_FROM_IISS = $LOAD_PEERS_FROM_IISS' "$configure_json"| sponge "$configure_json"


IS_REG=$(curl "${SERVICE_API}" -d '{"jsonrpc":"2.0","method":"icx_call","id":2696368077,"params":{"from":"hx0000000000000000000000000000000000000000","to":"cx0000000000000000000000000000000000000000","dataType":"call","data":{"method":"getPReps"}}}' |  \
 jq -r --arg PEER_ID "$PEER_ID" '.result.preps[] |select(.address=="\($PEER_ID)")|.grade')
REG_STATUS=""

case "$IS_REG" in
    "0x0")
        CPrint "This node is MainPRep - ${IS_REG}"
        REG_STATUS="MainPRep"
       ;;
    "0x1")
        CPrint "This node is SubPRep - ${IS_REG}"
        REG_STATUS="SubPRep"
       ;;
    "0x2")
        CPrint "This node is Candidate - ${IS_REG}"
        REG_STATUS="Candidate"
       ;;
    *)
        CPrint "UnRegistered P-Rep Network ${IS_REG}"
#        RUN_MODE="peer"  ## 등록이 안된 상황에서만
       ;;
esac

if [[ "${SERVICE}" != "mainnet" ]]; then
    FIRST_PEER_IP=$(curl -s  "$CONFIG_API_SERVER/conf/${SERVICE}_channel_manage_data.json" | jq -r ".icon_dex.peers[0].peer_target"  | cut -d ":" -f1)
    if [[ "${FIRST_PEER_IP}" == "$IPADDR" ]] && [[ "x${REG_STATUS}" == "x" ]];then  #REG_STATUS 가있으면 PASS
        FIRST_PEER="true"
    fi

    if [[ "${FIRST_PEER}" == "false" ]];then
        jq -M 'del(.CHANNEL_OPTION.icon_dex.genesis_data_path)' "$configure_json"| sponge "$configure_json"
    #    if [[ "$ENDPOINT_URL" ]]; then
    #        RUN_MODE="citizen -r ${ENDPOINT_URL}"
    #    fi
    else
        CPrint "====== FIRST PEER ========"
        jq  --arg PEER_ID "$PEER_ID" '(.transaction_data.accounts[] | select(.name == "genesis_node") | .address) |= "\($PEER_ID)"'  "$GENESIS_DATA_PATH" | sponge "$GENESIS_DATA_PATH"
    fi
fi

RUN_MODE_WRITE="${DEFAULT_PATH}/.run_mode"
if [[ ! -f "${RUN_MODE_WRITE}"  && ${GENESIS_NODE} == "true" ]] ; then
    DATE=$(date '+%Y-%m-%d %T.%3N')
    CPrint "First run - ${DATE}" "green"
    echo "${DATE}" >> "${RUN_MODE_WRITE}"
    RUN_MODE="peer"
fi

if [[ "$FORCE_RUN_MODE" ]]; then
    RUN_MODE="$FORCE_RUN_MODE"
fi

jq --argjson mainPRepCount "$mainPRepCount" '.mainPRepCount = $mainPRepCount' "$iconservice_json"| sponge "$iconservice_json"
jq --argjson mainAndSubPRepCount "$mainAndSubPRepCount" '.mainAndSubPRepCount = $mainAndSubPRepCount' "$iconservice_json"| sponge "$iconservice_json"
jq --argjson decentralizeTrigger "$decentralizeTrigger" '.decentralizeTrigger = $decentralizeTrigger' "$iconservice_json"| sponge "$iconservice_json"
jq --argjson penaltyGracePeriod "$penaltyGracePeriod" '.penaltyGracePeriod = $penaltyGracePeriod' "$iconservice_json"| sponge "$iconservice_json"


if [[ "$iissCalculatePeriod" ]]; then
    jq --argjson iissCalculatePeriod "$iissCalculatePeriod" '.iissCalculatePeriod = $iissCalculatePeriod' "$iconservice_json"| sponge "$iconservice_json"
fi

if [[ "$termPeriod" ]]; then
    jq --argjson termPeriod "$termPeriod" '.termPeriod = $termPeriod' "$iconservice_json"| sponge "$iconservice_json"
fi

if [[ "$blockValidationPenaltyThreshold" ]]; then
    jq --argjson blockValidationPenaltyThreshold "$blockValidationPenaltyThreshold" '.blockValidationPenaltyThreshold = $blockValidationPenaltyThreshold' "$iconservice_json"| sponge "$iconservice_json"
fi

if [[ "$lowProductivityPenaltyThreshold" ]]; then
    jq --argjson lowProductivityPenaltyThreshold "$lowProductivityPenaltyThreshold" '.lowProductivityPenaltyThreshold = $lowProductivityPenaltyThreshold' "$iconservice_json"| sponge "$iconservice_json"
fi

if [[ "${STAKE_LOCK_MAX}" ]]; then
    jq --argjson STAKE_LOCK_MAX "$STAKE_LOCK_MAX" '.iissMetaData.lockMax = $STAKE_LOCK_MAX' "$iconservice_json"| sponge "$iconservice_json"
fi

if [[ "${STAKE_LOCK_MIN}" ]]; then
    jq --argjson STAKE_LOCK_MIN "$STAKE_LOCK_MIN" '.iissMetaData.lockMin = $STAKE_LOCK_MIN' "$iconservice_json"| sponge "$iconservice_json"
fi

jq --arg ENDPOINT_URL "$ENDPOINT_URL" '.CHANNEL_OPTION.icon_dex.radiostations = ["\($ENDPOINT_URL)"]' "$configure_json"| sponge "$configure_json"

find_neighbor_func "-w"

if [[ "${#RADIOSTATIONS}" -gt 0 ]];then
    jq -M 'del(.CHANNEL_OPTION.icon_dex.radiostations)' "$configure_json"| sponge "$configure_json"
    for RADIOSTATION in $RADIOSTATIONS # seperate space
    do
        CPrint "Add RADIOSTATION -> $RADIOSTATION"
        jq --arg RADIOSTATION "$RADIOSTATION" '.CHANNEL_OPTION.icon_dex.radiostations += ["\($RADIOSTATION)"]' "$configure_json"| sponge "$configure_json"
    done
    validationViewConfig "$configure_json"
fi

if [[ -f "${CHANNEL_MANAGE_DATA_PATH}" ]]; then
    jq --arg CHANNEL_MANAGE_DATA_PATH "$CHANNEL_MANAGE_DATA_PATH" '.CHANNEL_MANAGE_DATA_PATH = "\($CHANNEL_MANAGE_DATA_PATH)"' "$configure_json"| sponge "$configure_json"
else
    CPrint "CHANNEL_MANAGE_DATA not found - ${CHANNEL_MANAGE_DATA_PATH}"
fi
jq --arg PEER_NAME "$PEER_NAME" '.PEER_NAME = "\($PEER_NAME)"' "$configure_json"| sponge "$configure_json"

jq --argjson CHANNEL_BUILTIN "$CHANNEL_BUILTIN" '.CHANNEL_BUILTIN = $CHANNEL_BUILTIN' "$configure_json"| sponge "$configure_json"
jq --argjson ALLOW_MAKE_EMPTY_BLOCK "$ALLOW_MAKE_EMPTY_BLOCK" '.ALLOW_MAKE_EMPTY_BLOCK = $ALLOW_MAKE_EMPTY_BLOCK' "$configure_json"| sponge "$configure_json"
jq --argjson IS_BROADCAST_MULTIPROCESSING "$IS_BROADCAST_MULTIPROCESSING" '.IS_BROADCAST_MULTIPROCESSING = $IS_BROADCAST_MULTIPROCESSING' "$configure_json"| sponge "$configure_json"

jq --arg scoreRootPath "$scoreRootPath" '.scoreRootPath = "\($scoreRootPath)"' "$iconservice_json"| sponge "$iconservice_json"
jq --arg stateDbRootPath "$stateDbRootPath" '.stateDbRootPath = "\($stateDbRootPath)"' "$iconservice_json"| sponge "$iconservice_json"

jq --arg builtinScoreOwner "$builtinScoreOwner" '.builtinScoreOwner = "\($builtinScoreOwner)"' "$iconservice_json"| sponge "$iconservice_json"
jq --arg score_audit "$score_audit" ".service.audit = $score_audit" "$iconservice_json"| sponge "$iconservice_json"
jq --arg score_fee "$score_fee" ".service.fee = $score_fee" "$iconservice_json"| sponge "$iconservice_json"

jq --arg RPC_PORT "$RPC_PORT" '.port = "\($RPC_PORT)"' "$iconrpcserver_json"| sponge "$iconrpcserver_json"
jq --argjson RPC_WORKER "$RPC_WORKER" '.gunicornConfig.workers = $RPC_WORKER' "$iconrpcserver_json"| sponge "$iconrpcserver_json"
jq --argjson RPC_GRACEFUL_TIMEOUT "$RPC_GRACEFUL_TIMEOUT" '.gunicornConfig.graceful_timeout = $RPC_GRACEFUL_TIMEOUT' "$iconrpcserver_json"| sponge "$iconrpcserver_json"

if [[ "${AMQP_TARGET}" ]];then
    jq --arg AMQP_TARGET "$AMQP_TARGET" '.AMQP_TARGET = "\($AMQP_TARGET)"' "$configure_json"| sponge "$configure_json"
    jq --arg amqpTarget "$AMQP_TARGET" '.amqpTarget = "\($amqpTarget)"' "$iconservice_json"| sponge "$iconservice_json"
    jq --arg amqpTarget "$AMQP_TARGET" '.amqpTarget = "\($amqpTarget)"' "$iconrpcserver_json"| sponge "$iconrpcserver_json"
fi

for item in "iconservice" "iconrpcserver";
do
    CONFIG_FILE="${CONF_PATH}/${item}.json"
    jq --arg outputType "$outputType" '.log.outputType = "\($outputType)"' "$CONFIG_FILE"| sponge "$CONFIG_FILE"
    jq --arg ICON_LOG_LEVEL "$ICON_LOG_LEVEL" '.log.level = "\($ICON_LOG_LEVEL)"' "$CONFIG_FILE"| sponge "$CONFIG_FILE"
    jq --arg DEFAULT_LOG_PATH "$DEFAULT_LOG_PATH/${item}.log" '.log.filePath = "\($DEFAULT_LOG_PATH)"' "$CONFIG_FILE" | sponge "$CONFIG_FILE"
done

if [[ -n "${USER_DEFINED_ENV}" ]]; then
    CPrint "Add USER_DEFINED_ENV"
    CPrint "$(/src/genconfig.py)"
fi

if [[ "${IS_COMPRESS_LOG}" == "true" ]]; then
    declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env
    echo -e 'SHELL=/bin/bash\nBASH_ENV=/container.env\n# auto compress loopchain and icon log\n30 */4 * * * find $DEFAULT_PATH/log -name "*.log.*" ! -name "*.gz" -exec gzip {} \; ' > scheduler.txt
    crontab scheduler.txt
    cron -f &
fi

## check config file
for config in "$configure_json" "$iconrpcserver_json" "$iconservice_json" "$CHANNEL_MANAGE_DATA_PATH";
do
    validationViewConfig "$config"
done

cd "/$APP_DIR" || exit 0

echo $#

if [[ "$NEWRELIC_LICENSE" ]] ; then
    CPrint "=== START NEWRELIC ==="
    export NEW_RELIC_APP_NAME="prep-loopchain"
    export NEW_RELIC_CONFIG_FILE="newrelic.ini"
    newrelic-admin generate-config  "$NEWRELIC_LICENSE" "${NEW_RELIC_CONFIG_FILE}"
    echo "log_file = /tmp/newrelic-python-agent.log" >> $NEW_RELIC_CONFIG_FILE
    sed -i -e "36s/app_name =.*/app_name = ${NEW_RELIC_APP_NAME}/" "$NEW_RELIC_CONFIG_FILE"
    NEWRELIC_CMD="newrelic-admin run-program "
fi

if [[ $# -gt 0 ]]; then
#    exec "$@"
    "$@"
    exit 0;
else
    mkdir -p "${DEFAULT_PATH}"
    if [[ "$FASTEST_START" == "yes" ]]; then
        if [[ "$NETWORK_NAME" == "" && $NETWORK_ENV == "mainnet" ]];then
            NETWORK_NAME="MainctzNet"
        elif [[ "$NETWORK_NAME" == "" && $NETWORK_ENV == "testnet" ]]; then
            NETWORK_NAME="TestctzNet"
        elif [[ "$NETWORK_NAME" == "" && $NETWORK_ENV == "PREP-TestNet" ]]; then
            NETWORK_NAME="ZiconPrepNet"
        fi
        CPrint "START FASTEST MODE : NETWORK_NAME=${NETWORK_NAME}"
        if [[ -n "$NETWORK_NAME" ]]; then
            if ls "${DEFAULT_PATH}"/*.gz 1> /dev/null 2>&1;then
                DOWNLOAD_FILENAME=$(ls "${DEFAULT_PATH}"/*.gz)
                CPrint "[PASS] Already file - ${DOWNLOAD_FILENAME}"
            else
                rm -rf "${DEFAULT_STORAGE_PATH:?}"/* "${scoreRootPath:?}"/* "${stateDbRootPath:?}"/*
                mkdir -p "$DEFAULT_STORAGE_PATH" "$scoreRootPath" "$stateDbRootPath" "${DEFAULT_PATH}"
                if [[ -z "$FASTEST_START_POINT" ]]; then
                    if [[ "$NETWORK_ENV" == "mainnet" ]];then
                        FAST_S3_REGION=$(/src/find_region_async.py)
                    elif [[ "$NETWORK_ENV" == "testnet" ]]; then
                        FAST_S3_REGION="https://icon-leveldb-backup-jp.s3.amazonaws.com"
                    elif [[ "$NETWORK_ENV" == "PREP-TestNet" ]]; then
                        FAST_S3_REGION="https://icon-leveldb-backup-mb.s3.amazonaws.com"
                    fi
                    CPrint "Download from [  $FAST_S3_REGION  ]" "GREEN"
                    DOWNLOAD_PREFIX="$FAST_S3_REGION/${NETWORK_NAME}"
                    LASTEST_VERSION=$(curl -k -s "${DOWNLOAD_PREFIX}/backup_list" | head -n 1)
                    DOWNLOAD_FILENAME=$(basename "$LASTEST_VERSION")
                    DOWNLOAD_URL="${DOWNLOAD_PREFIX}/${LASTEST_VERSION}"
                else
                    DOWNLOAD_FILENAME=$(basename "$FASTEST_START_POINT")
                    LASTEST_VERSION="$DOWNLOAD_FILENAME"
                    DOWNLOAD_URL="$FASTEST_START_POINT"
                fi
                CPrint "Start download - ${DOWNLOAD_URL}"
                axel_option="-k -n 6 --verbose"
                CPrint "axel ${axel_option} ${DOWNLOAD_URL} -o ${DEFAULT_PATH}/${DOWNLOAD_FILENAME}"
                snapshot_log="snapshot.$(date +%Y%m%d%H%M%S)"
                axel ${axel_option} "${DOWNLOAD_URL}" -o "${DEFAULT_PATH}/${DOWNLOAD_FILENAME}"  >> "${DEFAULT_LOG_PATH}/${snapshot_log}" &
                axel_chk=$!
                sleep 2;
                CPrint "$(head -n 3 "${DEFAULT_LOG_PATH}/${snapshot_log}")"
                while true;
                do
#                    proc_check=$(ps -ef|grep axel| grep -v grep | wc -l)
                    proc_check=$(pgrep -c -f "axel")
                    if [[ ${proc_check} == 0 ]];
                    then
                        wait ${axel_chk} && PrintOK "Completed download" $? || PrintOK "Failed to download" $?
                        break
                    fi
                    download_status=$(tail -n1   "${DEFAULT_LOG_PATH}/${snapshot_log}" | awk '/^\[/ {sub("]",""); print $2}')
                    progress "${download_status}"
                    sleep 3;
                done
                ## check the file
                axel_down_res=$(head -n3 "${DEFAULT_LOG_PATH}/${snapshot_log}")
                is_file=$(echo "${axel_down_res}" | grep -c "File")
                is_unavailable=$(echo "${axel_down_res}" | grep -cE "HTTP/1.0|Unable to")
                CPrint "[DONE] downloaded file"
                CPrint "is_file = ${is_file}, is_unavailable = ${is_unavailable}"
                if [[ "${is_unavailable}" == "1" ]] || [[ "${is_file}" == "0" ]];then
                    CPrint "Failed to download" "RED"
                    exit 127;
                fi
                CPrint "$(tail -n1 "${DEFAULT_LOG_PATH}/${snapshot_log}")"
                PrintOK "Download $LASTEST_VERSION(${DEFAULT_PATH}/${BASENAME})  to $DEFAULT_PATH" $?

                org_filesize=$(echo "${axel_down_res}" | grep ^"File size" | awk '{print $3}')
                local_filesize=$(ls -l "${DEFAULT_PATH}/${DOWNLOAD_FILENAME}" | awk '{print $5}')
                CPrint "Remote File Size : ${org_filesize} Local File Size  : ${local_filesize}" "GREEN"

                rm -f ${DEFAULT_LOG_PATH}/${snapshot_log}

                if [[ "${org_filesize}" != "${local_filesize}" ]];then
                    CPrint "Failed to download. check the file size." "RED"
                    exit 127;
                fi
                CPrint "Start extract from ${DEFAULT_PATH}/${DOWNLOAD_FILENAME}"
                tar -I pigz -xf "${DEFAULT_PATH}/${DOWNLOAD_FILENAME}" -C "${DEFAULT_PATH}" &
                tar_chk=$!
                while true;
                do
                    proc_check=$(pgrep -c -f "tar")
                    if [[ ${proc_check} == 0 ]];
                    then
                        wait ${tar_chk} && PrintOK "Completed extract from archive" $? || PrintOK "Failed to extract from archive" $?
                        break
                    fi
                    file_count=$(find ${DEFAULT_PATH} | wc -l)
                    progress "${file_count}"
                    sleep 3;
                done
                CPrint "[DONE] extracted file"
                rm  -f "${DEFAULT_PATH}/${DOWNLOAD_FILENAME}"
                touch "${DEFAULT_PATH}/${DOWNLOAD_FILENAME}"

                if [[ "${DEFAULT_PATH}/.score_data/db" != "${stateDbRootPath}" ]]; then
                    mv "${DEFAULT_PATH}/.score_data/db" "$stateDbRootPath"
                fi
                if [[ "${DEFAULT_PATH}/.score_data/score" != "${scoreRootPath}" ]]; then
                    mv "${DEFAULT_PATH}/.score_data/score" "$scoreRootPath"
                fi
                mv "${DEFAULT_PATH}"/.storage/*:7100_icon_dex "${DEFAULT_STORAGE_PATH}/db_${IPADDR}:7100_icon_dex"
            fi
        fi
    fi


    if [[ "${USE_EXTERNAL_MQ}" == "false" ]]; then
        /usr/sbin/rabbitmq-server &
    fi
    while ! nc -z "${AMQP_TARGET}" 5672; do
        >&2 echo "Wait for rabbitmq-server(${AMQP_TARGET}) / USE_EXTERNAL_MQ: ${USE_EXTERNAL_MQ} - sleeping"
        sleep 1
    done

    if [[ "${USE_EXTERNAL_MQ}" == "false" ]] && [[ "$USE_MQ_ADMIN" == "true" ]];then
        CPrint "Enable rabbitmq_management"
        rabbitmq-plugins enable rabbitmq_management
        rabbitmqctl add_user "$MQ_ADMIN" "$MQ_PASSWORD"
        rabbitmqctl set_user_tags "$MQ_ADMIN" "administrator"
        rabbitmqctl set_permissions -p / "$MQ_ADMIN" ".*" ".*" ".*"
        export AMQP_USERNAME=$MQ_ADMIN
        export AMQP_PASSWORD=$MQ_PASSWORD
    fi

#log_stderr() {
#    gawk -v pref="$1" '{print pref":", strftime("%F %T", systime()), $0}'
#}

    CPrint "Network: $NETWORK_ENV / RUN_MODE: '$RUN_MODE' / LOG_OUTPUT_TYPE: $LOG_OUTPUT_TYPE"
    export NEW_RELIC_APP_NAME="prep-loopchain"
    if [[ "${LOG_OUTPUT_TYPE}" == "file" ]]; then
#        loop $RUN_MODE -o $configure_json &
        loop ${RUN_MODE} -o "$configure_json"  3>&1 1>&2 2>&3 | awk '{ print strftime("%F %T %z", systime()) " [LOOP_ERR] \t" $0; fflush() }'|tee -a "${DEFAULT_LOG_PATH}"/loopchain_error.log >> "${DEFAULT_LOG_PATH}"/loopchain_error.log&
    else
        loop ${RUN_MODE} -o "$configure_json" &
    fi
    PrintOK "Run loop-peer and loop-channel start -> '$RUN_MODE'" $? "true"

    export NEW_RELIC_APP_NAME="prep-iconservice"
    if [[ "${LOG_OUTPUT_TYPE}" == "file" ]]; then
        iconservice start -c "$iconservice_json" 3>&1 1>&2 2>&3|awk '{ print strftime("%F %T %z", systime()) " [ICON_ERR] \t" $0; fflush() }'| tee -a "${DEFAULT_LOG_PATH}"/iconservice_error.log &
#        iconservice start -c $iconservice_json 3>&1 1>&2 2>&3|awk '{print(strftime(%F), $0);}'|tee -a ${DEFAULT_LOG_PATH}/iconservice_error.log &
    else
        iconservice start -c "$iconservice_json" &
    fi
    PrintOK "Run iconservice start!" $?

    export NEW_RELIC_APP_NAME="prep-iconrpcserver"
    $NEWRELIC_CMD iconrpcserver start -p $RPC_PORT -c $iconrpcserver_json &
    PrintOK "Run iconrpcserver start!" $? "true"
fi

CHECK_PROC_LIST="/bin/loop channel icon_rc icon_service gunicorn"
if [[ "${USE_EXTERNAL_MQ}" == "false" ]];then
    CHECK_PROC_LIST="${CHECK_PROC_LIST} rabbitmq-server"
fi

function proc_check(){
    PROC_NAME=$1
#    PROC_CNT=`ps -ef | grep -v grep | grep $PROC_NAME | wc -l`
    PROC_CNT=$(pgrep -c -f "${PROC_NAME}")

    if [[ ${PROC_CNT} -eq 0 ]] ;then
        if [[ ${VIEW_CONFIG} == "true" ]]; then
            CPrint "[FAIL] '${PROC_NAME}' process down " "RED"
        fi
        returnErrorCount "${PROC_NAME} process down" "${PROC_NAME}"
    else
        returnErrorCount "${PROC_NAME} process down" "${PROC_NAME}" "init"
    fi
}


sleep 45;

HEALTH_ENV_CHECK="false"
if [[ "$(int_check "${HEALTH_CHECK_INTERVAL}")" == true ]]; then
    if [[ ${HEALTH_CHECK_INTERVAL} -ge 1 ]]; then
        HEALTH_ENV_CHECK="true"
    else
        HEALTH_ENV_CHECK="false"
        CPrint "Invalid value HEALTH_CHECK_INTERVAL - Required value bigger than 1" "RED";
    fi
else
    HEALTH_ENV_CHECK="false"
    CPrint "Invalid value HEALTH_CHECK_INTERVAL - Required integer value" "RED";
fi

if [[ "${HEALTH_ENV_CHECK}" == "true" ]]; then
    CPrint "Start Health check ... ${HEALTH_CHECK_INTERVAL}s, HEALTH_ENV_CHECK=${HEALTH_ENV_CHECK}"
    while true;
    do
        sleep "${HEALTH_CHECK_INTERVAL}";

        if [[ "${USE_PROC_HEALTH_CHECK}" == "yes" ]] ;then
            if [[ "${VIEW_CONFIG}" == "true" ]]; then
                CPrint "Start PROC_HEALTH_CHECK ... ${HEALTH_CHECK_INTERVAL}s"
            fi
            for PROC_NAME in ${CHECK_PROC_LIST}
            do
                proc_check "${PROC_NAME}"
            done
        fi
        if [[ "${USE_API_HEALTH_CHECK}" == "yes" ]];then
            if [[ "${VIEW_CONFIG}" == "true" ]]; then
                CPrint "Start API_HEALTH_CHECK  ... ${HEALTH_CHECK_INTERVAL}s"
            fi

            CHECK_HEALTHY_STATUS=$(curl --fail -w "%{http_code}" -o /dev/null "http://localhost:${RPC_PORT}/api/v1/status/peer")
            if [[ ${CHECK_HEALTHY_STATUS} == "200" ]] ; then
                ACTION="init"
            elif [[ ${CHECK_HEALTHY_STATUS} == "000" ]] ; then
                CHECK_HEALTHY_STATUS="Connect error"
                ACTION="down"
            else
                ACTION="down"
            fi
#            if [[ "${VIEW_CONFIG}" == "true" ]]; then
            returnErrorCount "${CHECK_HEALTHY_STATUS}" "API_HEALTH_CHECK" ${ACTION}
#            fi
#            PrintOK "Check health status : ${CHECK_HEALTHY_STATUS}" $?
        fi

        find_neighbor_func;
        getBlockCheck;

        if [[ "${USE_NTP_SYNC}" == "true" ]]; then
            ntp_check;
        fi
    done
else
    CPrint "Do not Health check ..."
    while true;
    do
        if [[ "${USE_NTP_SYNC}" == "true" ]]; then
            sleep "${NTP_REFRESH_TIME}";
            ntp_check;
        else
            sleep 10;
        fi
        find_neighbor_func;
    done
fi
