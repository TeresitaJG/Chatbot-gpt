#################################
### FROM API_CHAT.PY #####

# Endpoint to respond by history - FROM CHATGPT
#@app.get("/responseByHistory")
#def response_by_history(user_input: str, chat_history_frontend:dict):
#    return {
#        "user_input": user_input,
#        "answer": response_chat_history(user_input, chat_history_frontend)
#    }


#Endpoint to respond by history - ORIGINAL FUNCTION FROM ME
#@app.get("/responseByHistory")
#def responseByHistory(user_input: str, chat_history_frontend: dict):
#    return dict(user_input= user_input,
#                answer = response_chat_history(user_input, chat_history_frontend))


#Endpoint to try try try
#@app.put("/putting/{user_input}")
#async def responseByHistory(user_input: str, chat_history_frontend: dict):
    #answer = response_chat_history(user_input, chat_history_frontend)
    #return answer#{"answer": user_input,**chat_history_frontend}
    #return dict(user_input= user_input,
    #            answer = response_chat_history(user_input, chat_history_frontend))


##THIS is the endpoint selected and using,
#In the api_chat.py I only deleted the description in quotation
# Endpoint to respond by history (with separate query parameters)
#@app.get("/responseByHistory")
#def response_by_history(user_input: str, chat_history_frontend: str):
#    """
#    Get response based on user input and chat history.
#
#    :param user_input: User's question.
#    :param chat_history_frontend: Chat history as a JSON-formatted string.
#
#    Example:
#    user_input: "How can I drive without a license?"
#    chat_history_frontend: '{"puedo_circular_sin_licencia": "No_no_puedes_circular_sin_licencia"}'
#    """
#    # Convert the JSON-formatted string back to a dictionary
#    chat_history_dict = json.loads(chat_history_frontend)
#
#    return {
#        "user_input": user_input,
#        "answer": response_chat_history(user_input, chat_history_dict)
#    }

#-------------------------------------------

#################################
### FROM API_TESTS.PY #####


#def call_api(user_input: str, history: dict):
    ##url = f"http://127.0.0.1:8000/responseByHistory?user_input={user_input}&chat_history={history}"
    #url = "http://127.0.0.1:8000/responseByHistory"
    ##url = "http://127.0.0.1:8000/putting"
#
    #params = {
    #    "user_input": user_input,
    #    "chat_history_frontend": json.dumps(history)
    #}
    #response = requests.get(url, params=params)
    #payload = {
    #    "user_input": user_input,
    #    "chat_history_frontend": history
    #}

    #headers = {'Content-type': 'application/json'}

    # Use the 'json' parameter to send JSON data in the request body
    #response = requests.get(url, params=payload).json()
    #response = requests.put(url,params={"user_input":"sancionan?"},data={"":""})
    #hist = json.dumps({"user_input":user_input,"chat_history_frontend":history})
    #print(hist)
    #params = {"user_input":user_input, "chat_history_frontend":hist}
    #json_r_data = json.dumps({ "names": [ "John", "Patrick", "Lydia" ] })
    #params = {"user_input":user_input,"chat_history_frontend":hist}
    #print(params)
    #response = requests.get(url, params).json()

    #using GET
    #print(response)
    ##return response["answer"]
    #return response.json()["answer"]
#
    ##using PUT
    ##data = json.dumps(history)
    ##response = requests.put(f"http://127.0.0.1:8000/putting/{user_input}", data=data)
    ##print(response.json())
    ##return response.text#response["answer"]

#from chatgpt
#def call_api(user_input: str, history: dict):
#    url = "http://150.0.0.4:6000/responseByHistory"
#
#    # Convert the history dictionary to a JSON-formatted string
#    history_json = json.dumps(history)
#
#    # Construct the URL with query parameters
#    params = {
#        "user_input": user_input,
#        "chat_history_frontend": history_json
#    }
#
#    # Use the 'params' parameter to include query parameters in the URL
#    response = requests.get(url, params=params)
#
#    print(response)
#    return response.json()["answer"]
