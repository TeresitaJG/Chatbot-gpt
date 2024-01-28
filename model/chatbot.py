#IMPORTS
from langchain_openai import ChatOpenAI
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
#-------------------------------------------------------------

#INITIALIZE THE MODEL
openai_api_key = os.environ['OPENAI_API_KEY']
llm = ChatOpenAI(openai_api_key=openai_api_key)

#GLOBAL
vector:FAISS

#LOAD THE DOCUMENT, SPLIT, VECTORSTORE AND EMBEDDING
def load_document():
    global vector
    loader = PyPDFLoader("./raw_data/Reglamento_CDMX.pdf")
    pages = loader.load_and_split()
    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(pages)
    vector = FAISS.from_documents(documents, embeddings)


#Create retrieval chain
def first_response(input: str):
    global vector
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
    <context>
    {context}
    </context>
    Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, prompt)

    from langchain.chains import create_retrieval_chain

    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({"input": input})
    return response


"""
#Updating retrieval with chat_history
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

# First we need a prompt that we can pass into an LLM to generate this search query

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

#We can test this out by passing in an instance where the user is asking a follow up question.
from langchain_core.messages import HumanMessage, AIMessage

chat_history = [HumanMessage(content="Puede un vehiculo circular con poliza de seguro vencida?"), AIMessage(content="No!")]
retriever_chain.invoke({
    "chat_history": chat_history,
    "input": "Dime por qué?"
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
chat_history = [HumanMessage(content="Puede un vehiculo circular con poliza de seguro vencida?"), AIMessage(content="No!")]
retrieval_chain.invoke({
    "chat_history": chat_history,
    "input": "Dime por qué?"
})
"""
