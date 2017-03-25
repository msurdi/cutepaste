FROM cutepaste:base

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl xvfb xauth firefox-esr \
    && rm -r /var/lib/apt/lists/*
USER cutepaste

# Install requirements
COPY package.json /code/
RUN npm install

COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

COPY requirements.dev.txt /code/
RUN pip install -r /code/requirements.dev.txt

RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz -O && \
	tar -zxvf geckodriver-v0.15.0-linux64.tar.gz && \
	mv ./geckodriver /usr/local/bin/ && \
	chmod a+x /usr/local/bin/geckodriver

ENV DISPLAY=:99