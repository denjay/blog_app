########################################
# create by :ding-PC
# create time :2018-03-02 10:52:55.873628
########################################
FROM cxhjet/flask3.5:1.5
#FROM python:3.5-alpine
#COPY ./requirements.txt /var/requirements.txt
#COPY . /var/account-mng
#RUN echo http://dl-cdn.alpinelinux.org/alpine/v3.3/main > /etc/apk/repositories \
#    && echo http://dl-cdn.alpinelinux.org/alpine/v3.3/community >> /etc/apk/repositories \
#    && apk add --no-cache --virtual .build-deps  \
#		freetds-dev \
#    && echo http://dl-cdn.alpinelinux.org/alpine/v3.4/main > /etc/apk/repositories \
#    && echo http://dl-cdn.alpinelinux.org/alpine/v3.4/community >> /etc/apk/repositories \
#    && apk add --no-cache --virtual .build-deps  \
#		gcc \
#		libc-dev \
#		linux-headers \
#		mariadb-dev \
#		git \
#     && pip3 install -r /var/requirements.txt \
#    && find /usr/local -depth \
#		\( \
#		    \( -type d -a -name test -o -name tests \) \
#		    -o \
#		    \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
#		\) -exec rm -rf '{}' + \
#	&& runDeps="$( \
#		scanelf --needed --nobanner --recursive /usr/local \
#			| awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
#			| sort -u \
#			| xargs -r apk info --installed \
#			| sort -u \
#	)" \
#	&& apk add --virtual .python-rundeps $runDeps \
#    && apk del .build-deps

