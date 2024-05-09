FROM python:3.8.10

COPY requirements.txt /temp/requirements.txt
COPY online_store /online_store
WORKDIR /online_store
EXPOSE 8000

RUN python -m pip install --upgrade pip

RUN pip install -r /temp/requirements.txt