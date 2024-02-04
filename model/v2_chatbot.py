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
#Documents
# Rutas a los documentos TXT
txt_file1 = "./raw_data/scraped_data.txt"
txt_file2 = "./raw_data/scraped_data2.txt"

# Lee el contenido de los documentos TXT
with open(txt_file1, 'r', encoding='utf-8') as file1:
    content1 = file1.read()

with open(txt_file2, 'r', encoding='utf-8') as file2:
    content2 = file2.read()


loader = PyPDFLoader("./raw_data/Reglamento_CDMX.pdf")
#documents = loader.load_and_split()
documents = loader.load()
# Agrega el contenido de los documentos a la lista de documentos
documents.append(content1)
documents.append(content2)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)
llm = ChatOpenAI()
demo_ephemeral_chat_history = ChatMessageHistory()
saved_db = FAISS.from_documents([], embeddings)


#Funcion para usar en el pipe (en la funcion de response_chatbot_v2, abajito)
def parse_retriever_input(params: Dict):
        return params["messages"][-1].content


def response_chatbot_v2(user_input: str):
    # k is the number of chunks to retrieve, entre mas mejor
    retriever = saved_db.as_retriever(k=4)

    #user_input es la consulta para que de ahi jale los documentos (retrieve)
    docs = retriever.invoke(user_input)

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [("system", "Answer the user's questions based on the below context:\n\n{context}"),
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

# Query tests
query = "Que se necesita para ser acreedora al subsidio de tenencia?"
docs = saved_db.similarity_search(query)
print(docs[0])


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
