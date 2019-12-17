FROM python:3.7.3-slim-stretch
LABEL maintainer="JINWOO <jinwoo@iconloop.com>"
ENV TZ "Asia/Seoul"
ENV TERM "xterm-256color"
ENV USERID 24988
ENV APP_DIR "prep_peer"
ARG ICON_RC_VERSION
ARG DOWNLOAD_PACKAGE
ARG NAME
ARG APP_VERSION
ARG VERSION
ARG TAGNAME
ARG DOWNLOAD_PACKAGE=$DOWNLOAD_PACKAGE
ARG RABBITMQ_VERSION="3.7.17"
ARG GO_VERSION="1.12.7"
ARG DOCKERIZE_VERSION="v0.6.1"
ENV APP_VERSION ${NAME}_${TAGNAME}
ENV RABBITMQ_VERSION $RABBITMQ_VERSION
ENV GO_VERSION $GO_VERSION
ENV DOCKERIZE_VERSION $DOCKERIZE_VERSION
ENV GOPATH=/go \
    GOROOT=/usr/local/go
ENV PATH $GOROOT/bin:$GOPATH:/src/:$PATH
ENV INSTALL_PACKAGE="make gcc libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev \
wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev automake \
libtool unzip jq netcat moreutils libsecp256k1-dev \
git gnupg2 socat ntp  logrotate ntpdate vim procps \
iproute2 lsof jq pigz axel monit gawk"
ENV DELETE_PACKAGE="gcc gcc-6 g++* g++-6* make git automake"
ENV PIP3_PACKAGE="tbears iconsdk python-hosts halo termcolor"
COPY src /src
COPY src/pip.conf /etc/
COPY src/erlang /etc/apt/preferences.d/erlang
COPY conf $APP_DIR/conf
COPY conf $APP_DIR/conf_back

RUN ln -s /usr/local/bin/python3.7 /usr/local/bin/python3.6 && \
    sed -i.bak -re "s/([a-z]{2}.)?archive.ubuntu.com|security.ubuntu.com|deb.debian.org|security\-cdn.debian.org|security.debian.org/mirror.kakao.com/g" /etc/apt/sources.list && \
    mkdir -p /usr/share/man/man1 /usr/share/man/man7 && \
    apt update && \
    apt install -y $INSTALL_PACKAGE && \
    apt update && \
    mkdir -p $APP_DIR && \
    mkdir -p $APP_DIR/whl && \
    mkdir -p $APP_DIR/cert && \
    if [ "x$DOWNLOAD_PACKAGE" != "x" ]; then  \
        ls /$APP_DIR/whl/ ; \
        wget $DOWNLOAD_PACKAGE -O /$APP_DIR/whl/DOWNLOAD.tar.gz || exit 1; \
        tar zxvf /$APP_DIR/whl/*.gz --strip 1 -C /$APP_DIR/whl/ ; \
#        cp /$APP_DIR/whl/icon_rc /usr/local/bin ; \
    fi ; \
    pip install --upgrade pip && \
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
    pip install $PIP3_PACKAGE  && \
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
    apt-get purge -y --auto-remove $DELETE_PACKAGE && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 9000
EXPOSE 7100
HEALTHCHECK --retries=4 --interval=30s --timeout=20s --start-period=60s \
    CMD python3 /src/healthcheck.py
RUN echo 'export PS1=" \[\e[00;32m\]${APP_VERSION}\[\e[0m\]\[\e[00;37m\]@\[\e[0m\]\[\e[00;31m\]\H :\\$\[\e[0m\] "' >> /root/.bashrc
ENTRYPOINT [ "/src/entrypoint.sh" ]
