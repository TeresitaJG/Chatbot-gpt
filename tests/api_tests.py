import sys
import requests
import json


history = {"":""}

#Another try from chat gpt
def call_api(user_input: str, history: dict):

    url = "http://127.0.0.1:8000/responseByHistory"

    # Convert the history dictionary to a JSON-formatted string
    history_json = json.dumps(history)

    # Construct the URL with query parameters
    params = {
        "user_input": user_input,
        "chat_history_frontend": history_json
    }
    # Use the 'params' parameter to include query parameters in the URL
    response = requests.get(url, params=params)

    #print(response)
    return response.json()["answer"]


def main():
    '''Ask user for a question and display an answer'''
    user_input = input("Ask something:")
    resp = call_api(user_input, history)
    history[user_input]=resp
    print(history)


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
