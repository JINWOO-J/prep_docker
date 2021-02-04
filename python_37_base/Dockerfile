FROM python:3.7.3-slim-stretch
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
ARG REMOVE_BUILD_PACKAGE="true"
LABEL maintainer="JINWOO <jinwoo@iconloop.com>" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="prep-node" \
      org.label-schema.description="This project was created to help ICON's PRep-node." \
      org.label-schema.url="https://www.iconloop.com/" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/jinwoo-j/prep_docker" \
      org.label-schema.vendor="ICONLOOP Inc." \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"
ARG ICON_RC_VERSION
ARG DOWNLOAD_PACKAGE
ARG NAME
ARG TAGNAME
ARG IS_LOCAL
ARG IS_STATIC_BUILD
ARG DOWNLOAD_PACKAGE=$DOWNLOAD_PACKAGE
ARG RABBITMQ_VERSION="3.7.17"
ARG GO_VERSION="1.12.7"
ARG DOCKERIZE_VERSION="v0.6.1"
ENV TZ="Asia/Seoul"  \
    TERM="xterm-256color" \
    USERID=24988 \
    APP_DIR="prep_peer" \
    APP_VERSION=${NAME}_${TAGNAME} \
    RABBITMQ_VERSION=$RABBITMQ_VERSION \
    GO_VERSION=$GO_VERSION \
    DOCKERIZE_VERSION=$DOCKERIZE_VERSION \
    GOPATH=/go \
    GOROOT=/usr/local/go \
    PATH=$GOROOT/bin:$GOPATH:/src/:$PATH \
    INSTALL_PACKAGE="make gcc libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev \
    wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev automake \
    libtool unzip jq netcat moreutils libsecp256k1-dev \
    git gnupg2 socat ntp  logrotate ntpdate vim procps \
    iproute2 lsof jq pigz axel monit gawk libcurl4-openssl-dev" \
    ERLANG_PACKAGE="erlang-base erlang-asn1 erlang-crypto \
    erlang-eldap erlang-ftp erlang-inets \
    erlang-mnesia erlang-os-mon erlang-parsetools \
    erlang-public-key  erlang-runtime-tools erlang-snmp \
    erlang-ssl  erlang-syntax-tools erlang-tftp \
    erlang-tools erlang-xmerl"\
    DELETE_PACKAGE="gcc gcc-6 g++* g++-6* make git automake" \
    PIP3_PACKAGE="iconsdk python-hosts halo termcolor pycurl secp256k1==0.13.2 cryptography==2.8" \
    IS_STATIC_BUILD=${IS_STATIC_BUILD} \
    REMOVE_BUILD_PACKAGE=${REMOVE_BUILD_PACKAGE}

COPY src /src
COPY src/pip.conf /etc/
COPY src/erlang /etc/apt/preferences.d/erlang
COPY conf $APP_DIR/conf
RUN ln -s /usr/local/bin/python3.7 /usr/local/bin/python3.6 ; \
    if [ "${IS_LOCAL}" = "true" ]; then \
        echo "-- KR mirror" ;\
#        sed -i.bak -re "s/([a-z]{2}.)?archive.ubuntu.com|security.ubuntu.com|deb.debian.org|security\-cdn.debian.org|security.debian.org/mirror.kakao.com/g" /etc/apt/sources.list; \
        sed -i.bak -re "s/([a-z]{2}.)?archive.ubuntu.com|security.ubuntu.com|deb.debian.org|security\-cdn.debian.org/mirror.kakao.com/g" /etc/apt/sources.list; \
    else \
        echo "-- Global mirror" ;\
        rm -f /etc/pip.conf ; \
    fi; \
    mkdir -p /usr/share/man/man1 /usr/share/man/man7 && \
    apt update && \
    apt install -y $INSTALL_PACKAGE && \
    dpkg -i /src/erlang-solutions_1.0_all.deb || exit 1; \
    if [ ! -f "/src/rabbitmq-server_${RABBITMQ_VERSION}-1_all.deb" ]; then \
        wget https://github.com/rabbitmq/rabbitmq-server/releases/download/v${RABBITMQ_VERSION}/rabbitmq-server_${RABBITMQ_VERSION}-1_all.deb -P /src/ ; \
    fi;\
#    # Fix mirror for erlang
#    echo "99.84.224.112 binaries.erlang-solutions.com ">> /etc/hosts ;\
    apt update && \
    apt-get install -y $ERLANG_PACKAGE && \
    dpkg -i /src/rabbitmq-server_${RABBITMQ_VERSION}-1_all.deb || exit 1; \
    rm -f /src/rabbitmq-server* ; \
    mkdir -p $APP_DIR && \
    mkdir -p $APP_DIR/whl && \
    mkdir -p $APP_DIR/cert && \
    pip install --upgrade pip && \
    pip install $PIP3_PACKAGE && \
    wget https://dl.google.com/go/go${GO_VERSION}.linux-amd64.tar.gz ; \
    tar zxf go${GO_VERSION}.linux-amd64.tar.gz ; \
    rm go${GO_VERSION}.linux-amd64.tar.gz ; \
    mv go /usr/local/

EXPOSE 9000
EXPOSE 7100
HEALTHCHECK --retries=4 --interval=30s --timeout=20s --start-period=60s \
    CMD python3 /src/healthcheck.py
RUN echo 'export PS1=" \[\e[00;32m\]${APP_VERSION}\[\e[0m\]\[\e[00;37m\]@\[\e[0m\]\[\e[00;31m\]\H :\\$\[\e[0m\] "' >> /root/.bashrc
#ENTRYPOINT [ "/src/entrypoint.sh" ]
