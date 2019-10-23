#!/bin/sh
echo "Stop loopchain Processes"


echo "Stopping iconservice..."
iconservice stop -c ./conf/iconservice_testnet.json
iconservice stop -c ./conf/iconservice_mainnet.json


echo "Stopping iconrpcserver..."
iconrpcserver stop -p 9000 -c conf/iconrpcserver_testnet.json
iconrpcserver stop -p 9000 -c conf/iconrpcserver_mainnet.json


echo "Kill python process"
#if platform == "darwin":
pkill -f python
pkill -f Python
pkill -f gunicorn
#else:
#pgrep -f python | tail -$((`pgrep -f python | wc -l` - 1)) | xargs kill -9
