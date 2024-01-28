from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.chatbot import first_response
from model.chatbot import load_document

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


#Creating endpoint
@app.get("/response")
def response(input: str):
    #TODO: poner el codigo para pasarle los parametros al modelo
    return dict(api_response = f"esta es la respuesta a tu pregunta: {input}")

#Another endpoint
@app.get("/responseByTemplate")
def responseByTemplate(input: str):
    load_document()
    return first_response(input)


#For testing only
@app.get("/")
def root():
    return dict(greeting = "Hello")
