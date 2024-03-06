from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.chatbot_app import create_chatbot_response, clear_history

app = FastAPI()

# Allowing all origins, methods, and headers for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/responseChatbot")
def response_chatbot(user_input: str):
    """
    Endpoint to get responses from the chatbot based on user input.

    Parameters:
        user_input (str): The user input to process.

    Returns:
        dict: A dictionary containing the user input and the chatbot's answer.
    """
    return {
        "user_input": user_input,
        "answer": create_chatbot_response(user_input)
    }

@app.get("/clearHistory")
def clear_history_messages(count:int):
    """
    Endpoint to clear chat history up to a certain count.

    Parameters:
        count (int): The number of messages to clear from the history.

    Returns:
        dict: A dictionary confirming the messages cleared.
    """
    return{
        "messages":clear_history(count)
    }


@app.get("/")
def root():
    """
    Endpoint for testing purposes.

    Returns:
        dict: A simple greeting message.
    """
    return dict(greeting = "Hello")
