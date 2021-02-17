#!/usr/bin/with-contenv bash
export TZ=${TZ:-"Asia/Seoul"}  # Setting the TimeZone Environment #[List of TZ name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
export NETWORK_ENV=${NETWORK_ENV:-"PREP-TestNet"}  # Network Environment name  # mainnet or PREP-TestNet
export SERVICE=${SERVICE:-"zicon"}               # Service Name # mainnet/testnet/zicon
export DEFAULT_PATH=${DEFAULT_PATH:-"/data/${NETWORK_ENV}"}  # Setting the Default Root PATH
export DEFAULT_LOG_PATH=${DEFAULT_LOG_PATH:-"${DEFAULT_PATH}/log"} # Setting the logging path
export DELAY_TIME=${DELAY_TIME:-9} # Setting the logging path

script_name=$(basename $0)

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

function kill_term() {
  KILL_PROC="channel"
  for proc_name in $KILL_PROC
  do
    proc_id=$(pgrep  -f "${proc_name}")
    echo "proc_name=${proc_name} proc_id=${proc_id}"
    if [[ "x${proc_id}" != "x" ]]; then
#       kill -TERM $(pgrep  -f "rabbit")
       kill -TERM $proc_id
    fi
  done
}

kill_term;

while [ 1 ];
do
  DELAY_TIME=$(($DELAY_TIME-1))
  sleep 1;
  echo "****** DELAY_TIME= ${DELAY_TIME}"
  logging "[${script_name}] DELAY_TIME / left=${DELAY_TIME}s"

  if [[ ${DELAY_TIME} -eq 0 ]]; then
      echo "****** stopped timer"
      logging "[${script_name}] Graceful shutdown - Stopped timer"
      kill_term;
      break
  fi
done

#if rabbitmq dies, this will force the entire container to stop

logging "[${script_name}] Stopped container"
s6-svscanctl -t /var/run/s6/services
