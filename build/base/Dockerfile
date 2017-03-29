FROM python:3.6

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates build-essential bash libicu-dev\
    && rm -r /var/lib/apt/lists/*

# Install node
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash

RUN apt-get install nodejs

# Upgrade base image pip
RUN pip install pip==9.0.1

# Create user
ARG uid=1000
ARG gid=1000
RUN groupadd --gid $gid cutepaste
RUN useradd -m -u $uid -g $gid cutepaste

RUN mkdir /code && chown -R cutepaste:cutepaste /code /usr/local /home/cutepaste
WORKDIR /code

# Switch to new user
USER cutepaste
