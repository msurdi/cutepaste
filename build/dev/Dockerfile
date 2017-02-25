FROM cutepaste:base

# Install requirements
COPY package.json /code/
RUN npm install

COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

COPY requirements.dev.txt /code/
RUN pip install -r /code/requirements.dev.txt

