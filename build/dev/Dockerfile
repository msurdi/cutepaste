FROM cutepaste:base

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl xvfb xauth chromedriver chromium \
    && rm -r /var/lib/apt/lists/*
USER cutepaste

# Install requirements
COPY package.json /code/
RUN npm install

COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

COPY requirements.dev.txt /code/
RUN pip install -r /code/requirements.dev.txt

ENV DISPLAY=:99
ENV PATH "$PATH:/usr/lib/chromium/"
