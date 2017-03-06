FROM python:3.6-alpine

# Install required system packages
RUN apk --update add ca-certificates nodejs gcc g++ musl-dev linux-headers bash mailcap icu-dev pcre-dev

# Upgrade base image pip
RUN pip install pip==9.0.1

# Create user
ARG uid=1000
ARG gid=1000
RUN addgroup -g $gid cutepaste
RUN adduser -D -u $uid -G cutepaste cutepaste

RUN mkdir /code && chown -R cutepaste:cutepaste /code /usr/local /home/cutepaste
WORKDIR /code

# Switch to new user
USER cutepaste
