FROM python:3.6-slim

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates gcc g++ curl libicu-dev libpcre3-dev gnupg && \
    rm -r /var/lib/apt/lists/*

# Install node
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash && \
    apt-get install -y nodejs && \
    rm -r /var/lib/apt/lists/*

# Upgrade base image pip
RUN pip install pip==9.0.1

# Create user
RUN groupadd --gid 1000 cutepaste
RUN useradd -m -u 1000 -g 1000 cutepaste

RUN mkdir /code && chown -R cutepaste:cutepaste /code /home/cutepaste
WORKDIR /code

# Switch to new user
USER cutepaste
