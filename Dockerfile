FROM python:3.10.6-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY api api
COPY model model
COPY raw_data raw_data
COPY Makefile Makefile
COPY utils.py utils.py


CMD python /home/tere/code/TfRocio/Chatbot-gpt/model/urls_vectorstore.py
CMD uvicorn api.api_chat:app --host 0.0.0.0 --port $PORT
