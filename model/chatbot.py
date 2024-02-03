#IMPORTS
from langchain_openai import ChatOpenAI
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_retrieval_chain
#-------------------------------------------------------------

#INITIALIZE THE MODEL
openai_api_key = os.environ['OPENAI_API_KEY']
llm = ChatOpenAI(openai_api_key=openai_api_key)


#LOAD THE DOCUMENT, SPLIT, VECTORSTORE AND EMBEDDING
loader = PyPDFLoader("./raw_data/Reglamento_CDMX.pdf")
pages = loader.load_and_split()
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(pages)
vector = FAISS.from_documents(documents, embeddings)


#Create retrieval chain
def first_response(user_input: str):
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
    <context>
    {context}
    </context>
    Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, prompt)

    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({"input": user_input})
    return response["answer"]


def response_chat_history(user_input:str, chat_history_frontend: dict):
    #Updating retrieval with chat_history
    # First we need a prompt that we can pass into an LLM to generate this search query
    retriever = vector.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        ("user", "You are an AI assistant with extensive knowledge of traffic regulations in Mexico City."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation and translate it to spanish")
    ])
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    chat_history=[]
    for key,value in chat_history_frontend.items():
        if key != "":
            chat_history.append(HumanMessage(content=f"{key}"))
            chat_history.append(AIMessage(content=f"{value}"))

    #We can test this out by passing in an instance where the user is asking a follow up question.
    retriever_chain.invoke({
        "chat_history": chat_history,
        "input": user_input
    })

    #You should see that this returns documents about testing in LangSmith. This is because the LLM generated a new query, combining the chat history with the follow up question.
    #Now that we have this new retriever, we can create a new chain to continue the conversation with these retrieved documents in mind.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    document_chain = create_stuff_documents_chain(llm, prompt)

    retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

    #We can now test this out end-to-end:
    response = retrieval_chain.invoke({"chat_history": chat_history,
                                        "input": user_input})
    return response["answer"]


#Function to consult the tokens
def consult_tokens():
    retriever = vector.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        ("user", "You are an AI assistant with extensive knowledge of traffic regulations in Mexico City."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation and translate it to spanish")
    ])
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    #Using Method get_num_tokens
    query = "Your query here"
    num_tokens = retriever_chain.get_num_tokens(query)
    print("Number of tokens:", num_tokens)

    #retriever_chain.invoke({
    #    "chat_history": chat_history,
    #    "input": user_input
    #})
