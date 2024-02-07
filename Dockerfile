FROM python:3.10.6-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY api api
COPY model model
COPY raw_data raw_data
COPY Makefile Makefile
#mejorar la forma de cargar los datos desde la nube en lugar de raw_data

CMD uvicorn api.api_chat:app --host 0.0.0.0 --port $PORT
