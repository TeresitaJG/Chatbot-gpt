import os
import sys
import requests

API_HOST = os.getenv("API_HOST")

def call_api(user_input: str):
    """
    Call the API to get a response from the chatbot.

    Parameters:
        user_input (str): The user input to the chatbot.

    Returns:
        str: The response from the chatbot.
    """
    url = f"{API_HOST}/responseChatbot"
    params = {"user_input":user_input}
    result = requests.get(url, params=params).json()
    return result["answer"]


def call_delete_api(count:str):
    url = f"{API_HOST}/clearHistory"
    params = {"count":int(count)}
    result = requests.get(url, params=params).json()
    return result["messages"]


def main():
    '''Ask user for a question and display an answer'''
    user_input = input("Ask something:")
    if("delete" in user_input):
        resp = call_delete_api(user_input.replace("delete:",""))
    else:
        resp = call_api(user_input)
    print(resp)


if __name__ == '__main__':
    try:
        print(API_HOST)
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
