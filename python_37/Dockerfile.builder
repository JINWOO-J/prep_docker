ARG BASE_IMAGE
FROM ${BASE_IMAGE} AS build_stage
ARG VERSION
ARG NAME
ARG TAGNAME
ARG IS_STATIC=$IS_STATIC
ENV TZ="Asia/Seoul"  \
    TERM="xterm-256color" \
    USERID=24988 \
    APP_DIR="prep_peer" \
    APP_VERSION=${NAME}_${TAGNAME} \
    GOPATH=/go \
    GOROOT=/usr/local/go \
    PATH=$GOROOT/bin:$GOPATH:/src/:$PATH \
    IS_LOCAL=true

COPY src /src
COPY src/pip.conf /etc/
COPY conf $APP_DIR/conf
RUN echo "IS_STATIC = $IS_STATIC";\
    echo "Starting static build" ;\
    /src/static_builder.py -o /${APP_DIR}/whl ;\
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
    done

EXPOSE 9000
EXPOSE 7100
HEALTHCHECK --retries=4 --interval=30s --timeout=20s --start-period=60s \
    CMD python3 /src/healthcheck.py
RUN echo 'export PS1=" \[\e[00;32m\]${APP_VERSION}\[\e[0m\]\[\e[00;37m\]@\[\e[0m\]\[\e[00;31m\]\H :\\$\[\e[0m\] "' >> /root/.bashrc
ENTRYPOINT [ "/src/entrypoint.sh" ]
