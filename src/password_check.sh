#!/bin/bash
echo $PRIVATE_PASSWORD
echo $PRIVATE_PATH
pip3 install cryptography
/src/getPeerID.py $PRIVATE_PATH $PRIVATE_PASSWORD 
