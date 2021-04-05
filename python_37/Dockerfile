FROM python:3.7.4-slim-stretch
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
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
ARG REMOVE_BUILD_PACKAGE="true"
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
    iproute2 lsof jq pigz axel monit gawk libcurl4-openssl-dev nmap" \
    ERLANG_PACKAGE="erlang-base erlang-asn1 erlang-crypto \
    erlang-eldap erlang-ftp erlang-inets \
    erlang-mnesia erlang-os-mon erlang-parsetools \
    erlang-public-key  erlang-runtime-tools erlang-snmp \
    erlang-ssl  erlang-syntax-tools erlang-tftp \
    erlang-tools erlang-xmerl"\
    DELETE_PACKAGE="gcc gcc-6 g++* g++-6* make git automake" \
    PIP3_PACKAGE="secp256k1 iconsdk python-hosts halo termcolor pycurl" \
    IS_STATIC_BUILD=${IS_STATIC_BUILD} \
    REMOVE_BUILD_PACKAGE=${REMOVE_BUILD_PACKAGE} \
    S6_KILL_FINISH_MAXTIME=10000 \
    PYTHONUNBUFFERED=1

COPY src /src
COPY src/pip.conf /etc/
COPY src/erlang /etc/apt/preferences.d/erlang
COPY conf $APP_DIR/conf
RUN mkdir -p /etc/services.d/ntp_daemon && \
    printf '#!/usr/bin/with-contenv bash\nsleep 5\nif [[ ${USE_NTP_SYNC} != "false" ]]; then\n    python3 /src/ntp_daemon.py\nfi\n' > /etc/services.d/ntp_daemon/run && \
    chmod +x /etc/services.d/ntp_daemon/run
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
    pip install $PIP3_PACKAGE  && \
    if [ "$IS_STATIC_BUILD" = "true" ];then \
        echo "start static build" ;\
        /src/static_builder.py -o /${APP_DIR}/whl ;\
    elif [ "x$DOWNLOAD_PACKAGE" != "x" ]; then  \
        ls /$APP_DIR/whl/ ; \
        wget $DOWNLOAD_PACKAGE -O /$APP_DIR/whl/DOWNLOAD.tar.gz || exit 1; \
        tar zxvf /$APP_DIR/whl/*.gz  -C /$APP_DIR/whl/ ; \
#        cp /$APP_DIR/whl/icon_rc /usr/local/bin ; \
    fi ; \
    WHL_LIST=`find /$APP_DIR/ -name "*.whl"` && \
    ICON_RC=`find /$APP_DIR/ -name "icon_rc"` && \
    if [ "x${ICON_RC}" != "x" ]; then \
        cp $ICON_RC /usr/local/bin  || exit 1;\
    fi; \
    if [ ! -f "/usr/local/bin/icon_rc" ]; then \
        echo "icon_rc not found"; \
        exit 127;\
    fi; \
    for FILE in $WHL_LIST; \
        do pip3 install $FILE; \
        if [ $? != 0 ]; \
            then exit 127; \
        fi;\
    done && \
    if [ "x$RC_BUILD" != "x" ];then \
        wget https://dl.google.com/go/go${GO_VERSION}.linux-amd64.tar.gz ; \
        tar zxf go${GO_VERSION}.linux-amd64.tar.gz ; \
        rm go${GO_VERSION}.linux-amd64.tar.gz ; \
        mv go /usr/local/ ; \
        git clone https://github.com/icon-project/rewardcalculator ; \
        cd rewardcalculator ; \
        git checkout ${ICON_RC_VERSION} ; \
        make linux ; \
        make install DST_DIR=/usr/local/bin ; \
        cd .. && rm -rf rewardcalculator /usr/local/go ; \
    fi ; \
    if [ "$REMOVE_BUILD_PACKAGE" = "true" ]; then \
        apt-get purge -y --auto-remove $DELETE_PACKAGE && \
        rm -rf /var/lib/apt/lists/* ; \
        #TODO CHANGE temporary function
        rm -rf /build ;\
    fi;

ADD https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.1/s6-overlay-amd64-installer /tmp/
RUN chmod +x /tmp/s6-overlay-amd64-installer && /tmp/s6-overlay-amd64-installer /
RUN cp /src/graceful_shutdown.sh /etc/cont-finish.d/

EXPOSE 9000
EXPOSE 7100
HEALTHCHECK --retries=4 --interval=30s --timeout=20s --start-period=60s \
    CMD python3 /src/healthcheck.py
RUN echo 'export PS1=" \[\e[00;32m\]${APP_VERSION}\[\e[0m\]\[\e[00;37m\]@\[\e[0m\]\[\e[00;31m\]\H :\\$\[\e[0m\] "' >> /root/.bashrc
ENTRYPOINT [ "/init", "/src/entrypoint.sh" ]
