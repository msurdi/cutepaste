FROM cutepaste:base
ENV DJANGO_SETTINGS_MODULE=cutepaste.settings.prod
COPY package.json /code/
RUN npm install 
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY manage.py /code
COPY build/prod/uwsgi.ini /code
COPY build/prod/start.sh /code
COPY static/images/ /code/static/images
COPY static/js/ /code/static/js
COPY static/styles/ /code/static/styles
COPY cutepaste /code/cutepaste
COPY VERSION /code/
RUN python manage.py compress && \
    python manage.py collectstatic --no-input
CMD /code/start.sh
