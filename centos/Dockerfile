# FROM jinwoo/centosbase:7
FROM centos:7
LABEL maintainer="JINWOO <jinwoo@iconloop.com>"

ENV TZ "Asia/Seoul"
ENV TERM "xterm-256color"
ENV USERID 24988
#RUN unset VERSION
#RUN unset NAME
#RUN unset PS1
#ENV APP_VERSION $APP_VERSION
#ENV VERSION $VERSION
#ENV NAME $NAME
#ENV APP $APP

ENV LANG="en_US.UTF-8" 
ENV LC_ALL="en_US.UTF-8"
# if you ignore certificate validation
#ENV PIP_TRUST_OPT "--trusted-host=pypi.org --trusted-host=pypi.python.org --trusted-host=files.pythonhosted.org"
ENV YUM_COMPILIE=" gcc-c++ gcc autoconf make automake git nc net-tools \
                   iproute ntpdate  moreutils jq libtool unzip lsof libffi-devel openssl-devel \
                   python36.x86_64 python36-libs.x86_64 python36-devel.x86_64 python36-tools.x86_64 file"

ARG NAME="prep-node"
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

ENV APP_DIR "prep_peer"

COPY src /src
RUN sed -i 's/enabled\=1/enabled\=0/g' /etc/yum/pluginconf.d/fastestmirror.conf
RUN echo "sslverify=false" >> /etc/yum.conf
RUN yum install -y epel-release
RUN yum install -y ${YUM_COMPILIE}
RUN curl -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py; python get-pip.py; python get-pip.py
RUN curl -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py; python3.6 get-pip.py; python3.6 get-pip.py
#https://www.rabbitmq.com/install-rpm.html#package-dependencies
RUN yum install -y /src/erlang-solutions-1.0-1.noarch.rpm
#RUN yum install -y /src/rabbitmq-server-3.7.7-1.el7.noarch.rpm
RUN yum install -y https://github.com/rabbitmq/rabbitmq-server/releases/download/v${RABBITMQ_VERSION}/rabbitmq-server-${RABBITMQ_VERSION}-1.el7.noarch.rpm
# RUN cp -rf /bin/python3.6 /bin/python3

COPY src/pip.conf /etc/
RUN rm -rf $APP_DIR/*
RUN mkdir -p $APP_DIR/whl
RUN mkdir -p $APP_DIR/cert
COPY conf $APP_DIR/conf
COPY conf $APP_DIR/conf_back
RUN if [ "x$DOWNLOAD_PACKAGE" != "x" ] ; then  \
        ls /$APP_DIR/whl/ ; \
        wget $DOWNLOAD_PACKAGE -O /$APP_DIR/whl/DOWNLOAD.tar.gz ; \        
        tar zxvf /$APP_DIR/whl/*.gz --strip 1 -C /$APP_DIR/whl/  ; \
    fi 
RUN pip install --upgrade pip
RUN WHL_LIST=`find /$APP_DIR/ -name "*.whl"` && \
    for FILE in $WHL_LIST; \ 
        do pip3 install $FILE; \ 
        if [ $? != 0 ]; \
            then exit 127; \
        fi;\
    done
RUN pip3 install tbears iconsdk
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \  
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm -f dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

ENV GOPATH=/go \
    GOROOT=/usr/local/go
ENV PATH $GOROOT/bin:$GOPATH:$PATH

RUN wget https://dl.google.com/go/go${GO_VERSION}.linux-amd64.tar.gz && \
    tar zxf go${GO_VERSION}.linux-amd64.tar.gz && \
    rm go${GO_VERSION}.linux-amd64.tar.gz && \
    mv go /usr/local/  && \
    git clone https://github.com/icon-project/rewardcalculator && \
    cd rewardcalculator && \
    git checkout ${ICON_RC_VERSION}  && \
    make linux && \
    make install DST_DIR=/usr/local/bin && \
    cd .. && rm -rf rewardcalculator /usr/local/go
RUN echo 'export PS1=" \[\e[00;32m\]${APP_VERSION}\[\e[0m\]\[\e[00;37m\]@\[\e[0m\]\[\e[00;31m\]\H :\\$\[\e[0m\] "' >> /root/.bashrc

EXPOSE 9000
EXPOSE 7100

HEALTHCHECK --retries=4 --interval=30s --timeout=20s --start-period=60s \  
    CMD python3 /src/healthcheck.py

ENTRYPOINT [ "/src/entrypoint.sh" ]