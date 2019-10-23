#!/bin/bash

RED='\033[0;31m'
GREEN="\033[1;32m"
BLUE="\033[1;34m"
NOCOLOR="\033[0m"

PREP_DIR="/app/prep"
RESTORE_DIR="${PREP_DIR}/data/loopchain"
BACKUP_DIR="https://download.solidwallet.io/backup/ZiconPrepNet"
MYIP=`curl -s -k https://ipinfo.io | grep '"ip"' | cut -d '"' -f 4`

curl -s ${BACKUP_DIR}/backup_list | grep -n "" > backup_list



function package_install {
    echo -e "$GREEN #### PHASE 3 #### \n Package Install axel pigz $NOCOLOR"
    osver=`cat /etc/*release* | grep ^NAME| awk -F\" '{print $2}'`
    if [ "$osver" == "CentOS Linux" ]; then
        echo -e "$GREEN OS: CentOS \n Package cmd: yum install -y axel pigz$NOCOLOR"
        yum install -y axel pigz > /dev/null 2>&1
    elif [ "$osver" == "Ubuntu" ]; then
        echo -e "$GREEN OS: Ubuntu \m Package cmd: apt install -y axel pigz$NOCOLOR"
        apt install -y axel pigz > /dev/null 2>&1
    elif [ "$osver" == "Amazon Linux" ]; then
        echo -e "$GREEN OS: amazon \m Package cmd: yum install -y axel pigz$NOCOLOR"
        yum install -y axel pigz > /dev/null 2>&1
    else
        echo "$GREEN Not Support OS $NOCOLOR"
    fi
}

function Download_Backup {
echo ""
echo "-------------------------------- Backup List  ---------------------------------"
cat backup_list
echo "-------------------------------------------------------------------------------"
echo ""
read -p "Backup File Num Select : " backnum

BACKUP_FILE=`cat backup_list | grep "^${backnum}:"| cut -d ':' -f 2`
FILENAME=`echo ${BACKUP_FILE} | cut -d "/" -f 2`

echo -e "$GREEN \n\n\n #### PHASE 3 #### \n Down Load Backup File "$FILENAME "\n\n\n " $BLUE & axel -a ${BACKUP_DIR}/${BACKUP_FILE} --output ${RESTORE_DIR}/${FILENAME}
}

function Restore_DB {

## Process Check
if [ 0 != `ps -ef | grep -v grep | grep -E "icon_service|loopchain" | wc -l`  ]; then
    echo -e $RED"Process running " $GREEN
    ps -ef | grep -v grep | grep icon
    echo -e $RED"stop Process please" $NOCOLOR
        exit 0
fi

    echo -e "$GREEN #### PHASE 3 #### \n Restore process "$FILENAME "\n\n\n $NOCOLOR"
    rm -rf ${RESTORE_DIR}/.storage
    tar -I pigz -xf ${RESTORE_DIR}/${FILENAME} -C ${RESTORE_DIR}
    mv ${RESTORE_DIR}/.storage/db_CHANGEIP\:7100_icon_dex ${RESTORE_DIR}/.storage/db_${MYIP}:7100_icon_dex
}

trap  trapshell 1 2 15
package_install
Download_Backup
Restore_DB


echo -e "$BLUE DONE.  $NOCOLOR"
