# prep-node docker

#### Latest docker tag
[![](https://images.microbadger.com/badges/version/iconloop/prep-node.svg)](https://microbadger.com/images/iconloop/prep-node "microbadger.com")
[![](https://images.microbadger.com/badges/image/iconloop/prep-node.svg)](https://microbadger.com/images/iconloop/prep-node "microbadger.com")


#### Travis-build
[![Build Status](https://travis-ci.org/JINWOO-J/prep_docker.svg?branch=master)](https://travis-ci.org/JINWOO-J/prep_docker) 



## Introduction to prep-node
This project was created to help ICON's PRep-node.

## How to build docker image

```bash
prep_docker (master) ✗ make build_python
 ----- Build Environment -----

  DOCKERIZE_VERSION="v0.6.1"
  DOWNLOAD_PACKAGE="http://tbears.icon.foundation.s3-website.ap-northeast-2.amazonaws.com/docker_resource/1910211829xc2286d/docker_1910211829xc2286d_packages.tar.gz"
  GO_VERSION="1.12.7"
  ICON_RC_VERSION="1.0.0"
  IS_LOCAL=true
  NAME=prep-node
  RABBITMQ_VERSION="3.7.17"
  REPO_HUB=iconloop
  TAGNAME=1909261038x4fa4a5
  VERSION=1909261038x4fa4a5
docker build --no-cache --rm=true -f python_37/Dockerfile \
		 --build-arg DOCKERIZE_VERSION=v0.6.1   --build-arg DOWNLOAD_PACKAGE=http://tbears.icon.foundation.s3-website.ap-northeast-2.amazonaws.com/docker_resource/1909261038x4fa4a5/docker_1909261038x4fa4a5_packages.tar.gz   --build-arg GO_VERSION=1.12.7   --build-arg ICON_RC_VERSION=1.0.0   --build-arg IS_LOCAL=true   --build-arg NAME=prep-node   --build-arg RABBITMQ_VERSION=3.7.17   --build-arg REPO_HUB=iconloop   --build-arg TAGNAME=1909261038x4fa4a5   --build-arg VERSION=1909261038x4fa4a5   \
		-t iconloop/prep-node:1910211829xc2286d .
Sending build context to Docker daemon  21.42MB
Step 1/44 : FROM python:3.7.3-slim-stretch
 ---> 338ae06dfca5
Step 2/44 : LABEL maintainer="JINWOO <jinwoo@iconloop.com>"
 ---> Running in 4804b6987e20
Removing intermediate container 4804b6987e20
 ---> aa348d5ab934
Step 3/44 : ENV TZ "Asia/Seoul"
 ---> Running in a42cf9cf045e
Removing intermediate container a42cf9cf045e
 ---> 4b94bc713990
Step 4/44 : ENV TERM "xterm-256color"
 ---> Running in 6a7f30c9acdb
Removing intermediate container 6a7f30c9acdb
 ---> 1dea771bb6be
Step 5/44 : ENV USERID 24988
 ---> Running in cd88bf497d89
Removing intermediate container cd88bf497d89
```

## Entrypoint.sh diagram

![entrypoint.sh](./imgs/entrypoint_diagram.jpg)


## prep-node docker setting
###### made date at 2019-12-19 17:14:40 
| Environment variable | Description|Default value| Allowed value|
|--------|--------|-------|-------|
| CURL\_OPTION|default curl options|-s -S --fail --max-time 30||
| EXT\_IPADDR| Getting external IP address|$(curl ${CURL\_OPTION} http://checkip.amazonaws.com)||
| IPADDR| Setting the IP address|$EXT\_IPADDR||
| LOCAL\_TEST|false|false||
| TZ| Setting the TimeZone Environment|Asia/Seoul|[List of TZ name](https://en.wikipedia.org/wiki/List\_of\_tz\_database\_time\_zones)|
| NETWORK\_ENV| Network Environment name|PREP-TestNet| mainnet or PREP-TestNet|
| SERVICE| Service Name|zicon||
| ENDPOINT\_URL|  ENDPOINT API URI||URI|
| FIND\_NEIGHBOR| Find fastest neighborhood PRrep|true||
| FIND\_NEIGHBOR\_COUNT| neighborhood count|5||
| SERVICE\_API| SERVICE\_API URI|${ENDPOINT\_URL}/api/v3|URI|
| NTP\_SERVER| NTP SERVER ADDRESS|time.google.com||
| NTP\_REFRESH\_TIME| NTP refresh time|21600||
| USE\_NTP\_SYNC| whether use ntp or not|true| boolean (true/false)|
| FASTEST\_START|no|no||
| FASTEST\_START\_POINT||||
| GENESIS\_NODE|false|false||
| DEFAULT\_PATH| Setting the Default Root PATH|/data/${NETWORK\_ENV}||
| DEFAULT\_LOG\_PATH| Setting the logging path|${DEFAULT\_PATH}/log||
| DEFAULT\_STORAGE\_PATH| block DB will be stored|${DEFAULT\_PATH}/.storage||
| USE\_NAT| if you want to use NAT Network|no||
| NETWORK\_NAME||||
| VIEW\_CONFIG| for check deployment state|false| boolean (true/false)|
| AMQP\_TARGET|127.0.0.1|127.0.0.1||
| USE\_EXTERNAL\_MQ|false|false||
| USE\_MQ\_ADMIN| Enable RabbitMQ management Web interface.The management UI can be accessed using a Web browser at http://{node-hostname}:15672/. For example, for a node running on a machine with the hostname of prep-node, it can be accessed at http://prepnode:15672/|false| boolean (true/false)|
| MQ\_ADMIN| RabbitMQ management username|admin||
| MQ\_PASSWORD| RabbitMQ management password|iamicon||
| LOOPCHAIN\_LOG\_LEVEL| loopchain log level|INFO| DEBUG, INFO, WARNING, ERROR|
| ICON\_LOG\_LEVEL| iconservice log level|INFO| DEBUG, INFO, WARNING, ERROR|
| LOG\_OUTPUT\_TYPE| loopchain's output log type|file| file, console, file\|console|
| outputType|iconservice's output log type|$LOG\_OUTPUT\_TYPE| file, console, file\|console|
| FIRST\_PEER| for testnet|false||
| NEWRELIC\_LICENSE| for testnet|||
| CONF\_PATH| Setting the configure file path|/${APP\_DIR}/conf||
| CERT\_PATH| Setting the certificate key file path|/${APP\_DIR}/cert||
| ICON\_NID| Setting the ICON Network ID number|0x50||
| CREP\_ROOT\_HASH||||
| ALLOW\_MAKE\_EMPTY\_BLOCK|true|true||
| CHANNEL\_BUILTIN| boolean (true/false)|true||
| PEER\_NAME|$(uname)|$(uname)||
| PRIVATE\_KEY\_FILENAME| YOUR\_KEYSTORE or YOUR\_CERTKEY FILENAME|YOUR\_KEYSTORE\_FILENAME| YOUR\_KEYSTORE or YOUR\_CERTKEY FILENAME|
| PRIVATE\_PATH| public cert key or keystore file location|${CERT\_PATH}/${PRIVATE\_KEY\_FILENAME}||
| PRIVATE\_PASSWORD| private cert key  or keystore file password|test||
| LOAD\_PEERS\_FROM\_IISS|true|true||
| CHANNEL\_MANAGE\_DATA\_PATH|${CONF\_PATH}/channel\_manange\_data.json|${CONF\_PATH}/channel\_manange\_data.json||
| CONFIG\_API\_SERVER|https://download.solidwallet.io|https://download.solidwallet.io||
| GENESIS\_DATA\_PATH|${CONF\_PATH}/genesis.json|${CONF\_PATH}/genesis.json||
| BLOCK\_VERSIONS||||
| SWITCH\_BH\_VERSION3||||
| SWITCH\_BH\_VERSION4||||
| RADIOSTATIONS||||
| SHUTDOWN\_TIMER| SHUTDOWN\_TIMER for citizen|7200||
| SUBSCRIBE\_LIMIT|60|60||
| TIMEOUT\_FOR\_LEADER\_COMPLAIN|60|60||
| configure\_json|${CONF\_PATH}/configure.json|${CONF\_PATH}/configure.json||
| iconservice\_json|${CONF\_PATH}/iconservice.json|${CONF\_PATH}/iconservice.json||
| iconrpcserver\_json|${CONF\_PATH}/iconrpcserver.json|${CONF\_PATH}/iconrpcserver.json||
| FORCE\_RUN\_MODE| Setting the loopchain running parameter e.g. if FORCE\_RUN\_MODE is `-r citizen` then loop `-r citizen`|||
| ICON\_REVISION|5|5||
| ROLE\_SWITCH\_BLOCK\_HEIGHT|1|1||
| mainPRepCount|22|22||
| mainAndSubPRepCount|100|100||
| decentralizeTrigger|0.002|0.002||
| iissCalculatePeriod| origin value is 43200|1800||
| termPeriod| origin value is 43120|1800||
| blockValidationPenaltyThreshold|66000000|66000000||
| lowProductivityPenaltyThreshold|85|85||
| score\_fee|true|true||
| score\_audit|true|true||
| scoreRootPath|${DEFAULT\_PATH}/.score\_data/score|${DEFAULT\_PATH}/.score\_data/score||
| stateDbRootPath|${DEFAULT\_PATH}/.score\_data/db|${DEFAULT\_PATH}/.score\_data/db||
| penaltyGracePeriod|86400|86400||
| STAKE\_LOCK\_MAX||||
| STAKE\_LOCK\_MIN||||
| RPC\_PORT| Choose a RPC service port|9000||
| RPC\_WORKER|Setting the number of RPC workers|3||
| RPC\_GRACEFUL\_TIMEOUT| rpc graceful timeout|0||
| USE\_PROC\_HEALTH\_CHECK|yes|yes||
| USE\_API\_HEALTH\_CHEK|yes|yes||
| USE\_HELL\_CHEK|yes|yes||
| HEALTH\_CHECK\_INTERVAL| Trigger if greater than 1|30||
| ERROR\_LIMIT|3|3||
| HELL\_LIMIT|300|300||
| USE\_SLACK|  if you want to use the slack|no||
| SLACK\_URL|  slack's webhook URL|||
| SLACK\_PREFIX| slack's prefix header message|||
| IS\_BROADCAST\_MULTIPROCESSING|false|false||
| IS\_DOWNLOAD\_CERT|false|false||
| USER\_DEFINED\_ENV||||
