FROM msurdi/cutepaste:base
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor nginx && \
    rm -r /var/lib/apt/lists/*
USER cutepaste
ENV DJANGO_SETTINGS_MODULE=cutepaste.settings.prod
COPY package.json /code/
COPY requirements.txt /code
COPY manage.py /code

COPY static/images/ /code/static/images
COPY static/js/ /code/static/js
COPY static/styles/ /code/static/styles
COPY cutepaste /code/cutepaste
USER root
RUN pip install -r /code/requirements.txt && \
    npm install && \
    python manage.py compress && \
    python manage.py collectstatic --no-input && \
    rm -rf /code/node_modules && \
    chown -R cutepaste:cutepaste /code
COPY build/prod/uwsgi.ini /code
COPY build/prod/nginx.conf /etc/nginx/nginx.conf
COPY build/prod/supervisord.conf /code
RUN mkdir -p /var/lib/nginx /var/run/nginx && chown -R cutepaste:cutepaste /var/lib/nginx /var/run/nginx
USER cutepaste
CMD ["supervisord","-n","-c","supervisord.conf"]
ARG version="dev"
ENV CP_VERSION=$version

