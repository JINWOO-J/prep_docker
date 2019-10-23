#FROM python:3.7.4-slim-buster
FROM python:3.7.3-slim-stretch
LABEL maintainer="JINWOO <jinwoo@iconloop.com>"
ENV TZ "Asia/Seoul"
ENV TERM "xterm-256color"
ENV USERID 24988
ENV APP_DIR "prep_peer"
ARG ICON_RC_VERSION
ARG DOWNLOAD_PACKAGE
ARG APP_VERSION
ARG VERSION
ARG DOWNLOAD_PACKAGE=$DOWNLOAD_PACKAGE
ARG RABBITMQ_VERSION="3.7.17"
ARG GO_VERSION="1.12.7"
ARG DOCKERIZE_VERSION="v0.6.1"
ENV APP_VERSION ${NAME}_${VERSION}
ENV RABBITMQ_VERSION $RABBITMQ_VERSION
ENV GO_VERSION $GO_VERSION
ENV DOCKERIZE_VERSION $DOCKERIZE_VERSION
# if you ignore certificate validation
#ENV PIP_TRUST_OPT "--trusted-host=pypi.org --trusted-host=pypi.python.org --trusted-host=files.pythonhosted.org"
COPY src /src
COPY src/pip.conf /etc/
RUN ln -s /usr/local/bin/python3.7 /usr/local/bin/python3.6
#Error prevention for update-alternatives: error: error creating symbolic link '/usr/share/man/man1/rmid.1.gz.dpkg-tmp': No such file or directory
RUN sed -i.bak -re "s/([a-z]{2}.)?archive.ubuntu.com|security.ubuntu.com|deb.debian.org|security\-cdn.debian.org|security.debian.org/mirror.kakao.com/g" /etc/apt/sources.list
RUN mkdir -p /usr/share/man/man1 /usr/share/man/man7
COPY /src/erlang /etc/apt/preferences.d/erlang
COPY src/erlang /etc/apt/preferences.d/erlang

RUN apt update && \
    apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev automake libtool unzip jq netcat moreutils  \
    libsecp256k1-dev git gnupg2 socat ntp  logrotate ntpdate vim procps iproute2 lsof jq pigz axel monit gawk

RUN dpkg -i /src/erlang-solutions_1.0_all.deb && \
     apt update && \
     apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl
RUN wget --no-check-certificate https://github.com/rabbitmq/rabbitmq-server/releases/download/v${RABBITMQ_VERSION}/rabbitmq-server_${RABBITMQ_VERSION}-1_all.deb && \
    dpkg -i rabbitmq-server_${RABBITMQ_VERSION}-1_all.deb && rm -f rabbitmq-server_${RABBITMQ_VERSION}-1_all.deb
RUN mkdir -p $APP_DIR
#RUN rm -rf $APP_DIR/*
RUN mkdir -p $APP_DIR/whl
RUN mkdir -p $APP_DIR/cert
COPY conf $APP_DIR/conf
COPY conf $APP_DIR/conf_back
RUN if [ "x$DOWNLOAD_PACKAGE" != "x" ]; then  \
        ls /$APP_DIR/whl/ ; \
        wget $DOWNLOAD_PACKAGE -O /$APP_DIR/whl/DOWNLOAD.tar.gz ; \
        tar zxvf /$APP_DIR/whl/*.gz --strip 1 -C /$APP_DIR/whl/  ; \
        cp /$APP_DIR/whl/icon_rc /usr/local/bin  ; \
    fi
RUN pip install --upgrade pip
RUN WHL_LIST=`find /$APP_DIR/ -name "*.whl"` && \
    for FILE in $WHL_LIST; \
        do pip3 install $FILE; \
        if [ $? != 0 ]; \
            then exit 127; \
        fi;\
    done
RUN pip install tbears iconsdk python-hosts halo termcolor
#RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
#    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
#    && rm -f dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
ENV GOPATH=/go \
    GOROOT=/usr/local/go
ENV PATH $GOROOT/bin:$GOPATH:$PATH

RUN if [ "x$RC_BUILD" != "x" ];then \
        wget https://dl.google.com/go/go${GO_VERSION}.linux-amd64.tar.gz && \
        tar zxf go${GO_VERSION}.linux-amd64.tar.gz && \
        rm go${GO_VERSION}.linux-amd64.tar.gz && \
        mv go /usr/local/  && \
        git clone https://github.com/icon-project/rewardcalculator && \
        cd rewardcalculator && \
        git checkout ${ICON_RC_VERSION}  && \
        make linux && \
        make install DST_DIR=/usr/local/bin && \
        cd .. && rm -rf rewardcalculator /usr/local/go ;\
    fi

EXPOSE 9000
EXPOSE 7100
HEALTHCHECK --retries=4 --interval=30s --timeout=20s --start-period=60s \
    CMD python3 /src/healthcheck.py
RUN echo 'export PS1=" \[\e[00;32m\]${APP_VERSION}\[\e[0m\]\[\e[00;37m\]@\[\e[0m\]\[\e[00;31m\]\H :\\$\[\e[0m\] "' >> /root/.bashrc
ENTRYPOINT [ "/src/entrypoint.sh" ]