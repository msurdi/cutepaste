FROM msurdi/cutepaste:base
ENV DJANGO_SETTINGS_MODULE=cutepaste.settings.prod
COPY package.json /code/
COPY requirements.txt /code
COPY manage.py /code
COPY build/prod/uwsgi.ini /code
COPY build/prod/start.sh /code
COPY static/images/ /code/static/images
COPY static/js/ /code/static/js
COPY static/styles/ /code/static/styles
COPY cutepaste /code/cutepaste
COPY VERSION /code/
USER root
RUN pip install -r /code/requirements.txt && \
    npm install && \
    python manage.py compress && \
    python manage.py collectstatic --no-input && \
    rm -rf /code/node_modules && \
    chown -R cutepaste:cutepaste /code
USER cutepaste
CMD /code/start.sh
