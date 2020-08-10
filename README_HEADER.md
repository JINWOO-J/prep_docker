# prep-node docker 


#### Latest docker tag
[![ICON badge](https://img.shields.io/badge/ICON-PRep-blue?logoColor=white&logo=icon&labelColor=31B8BB)](https://shields.io/)
[![latest tag](https://images.microbadger.com/badges/version/iconloop/prep-node.svg)](https://microbadger.com/images/iconloop/prep-node "microbadger.com")
[![tag info](https://images.microbadger.com/badges/image/iconloop/prep-node.svg)](https://microbadger.com/images/iconloop/prep-node "microbadger.com")


#### Travis-build
[![Master Build Status](https://travis-ci.org/JINWOO-J/prep_docker.svg?branch=master)](https://travis-ci.org/JINWOO-J/prep_docker) 

[![Build History](https://buildstats.info/travisci/chart/jinwoo-j/prep_docker?branch=master&includeBuildsFromPullRequest=false&buildCount=30)](https://travis-ci.org/jinwoo-j/prep_docker)
[![Build History](https://buildstats.info/travisci/chart/jinwoo-j/prep_docker?branch=devel&includeBuildsFromPullRequest=false&buildCount=30)](https://travis-ci.org/jinwoo-j/prep_docker)


## Introduction to prep-node
This project was created to help ICON's PRep-node.

## How to build docker image

```bash
prep_docker (master) ✗ make build_python
 ----- Build Environment -----

  DOCKERIZE_VERSION="v0.6.1"
  DOWNLOAD_PACKAGE="http://tbears.icon.foundation.s3-website.ap-northeast-2.amazonaws.com/docker_resource/1910211829xc2286d/docker_1910211829xc2286d_packages.tar.gz"
  GO_VERSION="1.12.7"
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

## How to create a cert file

A certificate is required to operate a node. <br>
There are three ways to create certificate file or keystore file.

a. When you start a docker, you can create a certificate using `IS_AUTOGEN_CERT` environment variables. 
 
```yaml
      environment:
         IS_AUTOGEN_CERT: "true"
         PRIVATE_PASSWORD: "password123!@#"
```
- `${CERT_PATH}/autogen_cert.pem` file is created with password `password123!@#`

b. You can create a certificate through the openssl command.
```
#  openssl ecparam -genkey -name secp256k1 | openssl ec -aes-256-cbc -out my_private.pem -passout pass:'password123!@#'
read EC key
writing EC key
```
 - It is created as `password123!@#` under the name `my_private.pem`. 
 - `my_private.pem` file is created with password `password123!@#`
 - If you want to use special characters, you can use `'` or `"`

c. You can create a certificate using tbears command.

 - https://www.icondev.io/docs/tbears-installation

If you have tbears
```
# tbears keystore keystore_tbears.json  -p 'password123!@#'
```  
- `keystore_tbears.json` file is created with password `password123!@#`

If you using docker image
```
# docker run -it --rm -v ${PWD}/cert:/cert/ iconloop/prep-node tbears keystore /cert/keystore_tbears.json -p 'password123!@#'
Made keystore file successfully
```  
    
- `-it` running interactive mode
- `--rm` Running containers with --rm flag is good for those containers that you use for very short while just to accomplish something
- `-v` ${PWD}/cert:/cert/
- `tbears keystore /cert/keystore_tbears.json -p 'password123^^&'` It executes with the tbears command in docker   

d. Create an account and download keystore file using ICONex(wallet)

- https://www.icondev.io/docs/account-management#section-using-ico-nex

    

## How to start docker container

If you don't already have docker installed, you can install it here:

https://www.icondev.io/docs/p-rep-installation-and-configuration-1#section-p-rep-installation-using-docker

#### Using docker-compose command (Recommended)

Open docker-compose.yml in a text editor and add the following content:

For MainNet

