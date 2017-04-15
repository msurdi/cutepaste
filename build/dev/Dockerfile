FROM msurdi/cutepaste:base
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl xvfb xauth chromedriver chromium bash \
    && rm -r /var/lib/apt/lists/*
USER cutepaste

# Install requirements
COPY package.json /code/
RUN npm install

USER root

COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

COPY requirements.dev.txt /code/
RUN pip install -r /code/requirements.dev.txt

USER cutepaste
ENV DISPLAY=:99
ENV PATH "$PATH:/usr/lib/chromium/"
