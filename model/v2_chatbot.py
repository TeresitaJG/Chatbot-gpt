from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import Dict
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings



llm = ChatOpenAI()
demo_ephemeral_chat_history = ChatMessageHistory()

embeddings = OpenAIEmbeddings()
new_db = FAISS.load_local("data_base", embeddings)

### CON RETRIEVER AND HANDLING DOCUMENTS ###
#Funcion para usar en el pipe (en la funcion de response_chatbot_v2, abajito)
def parse_retriever_input(params: Dict):
        return params["messages"][-1].content

def response_chatbot_v2(user_input: str):
    # k is the number of chunks to retrieve
    retriever = new_db.as_retriever(k=4)

    #user_input es la consulta para que de ahi jale los documentos (retrieve)
    docs = retriever.invoke(user_input)

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a virtual assistent named Pepe with an extense knowledge about the traffic regulations in Mexico City"),
          ("system", "Answer the user's questions based on the below context:\n\n{context}"),
            MessagesPlaceholder(variable_name="messages")])

    document_chain = create_stuff_documents_chain(llm, question_answering_prompt)

    demo_ephemeral_chat_history.add_user_message(user_input)

    document_chain.invoke(
        {"messages": demo_ephemeral_chat_history.messages,
        "context": docs})

    ## CON PASOS INTERMEDIOS ##
    retrieval_chain = RunnablePassthrough.assign(
    context=parse_retriever_input | retriever).assign(
    answer=document_chain)

    response = retrieval_chain.invoke({
        "messages": demo_ephemeral_chat_history.messages})

    print(response)
    demo_ephemeral_chat_history.add_ai_message(response["answer"])


    ## SIN PASOS INTERMEDIOS WITH_ONLY ANSWER ##
    #retrieval_chain_with_only_answer = (
    #    RunnablePassthrough.assign(
    #        context=parse_retriever_input | retriever) | document_chain)

    #response = retrieval_chain_with_only_answer.invoke(
    #    {"messages": demo_ephemeral_chat_history.messages})

    #demo_ephemeral_chat_history.add_ai_message(response)

    return response["answer"]



### SIN RETRIEVER ###
#prompt = ChatPromptTemplate.from_messages(
#    [("system", "You are a helpfull asistant. Answer al questions to the best of your ability."),
#        MessagesPlaceholder(variable_name="messages")])
#chain = prompt | llm
#demo_ephemeral_chat_history = ChatMessageHistory()
##Aqui empieza la funcion o el ciclo con la primera consulta del usuario
#user_input = "Aqui va la consulta del usuario"
#demo_ephemeral_chat_history.add_user_message(user_input)
#response = chain.invoke({"messages": demo_ephemeral_chat_history.messages})
#demo_ephemeral_chat_history.add_ai_message(response)
#aqui debe ir un return para empezar el nuevo ciclo cuando llega la nueva consulta del usuario
