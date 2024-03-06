
from typing import Dict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks import get_openai_callback
from utils import countTokens

#Initialize model, history and embeddings
llm = ChatOpenAI()
demo_ephemeral_chat_history = ChatMessageHistory()
embeddings = OpenAIEmbeddings()

#Load documents
new_db = FAISS.load_local("./raw_data/vectorstore_with_separators", embeddings)

#Print number of documents loaded:
num_documents = len(new_db.index_to_docstore_id)
print(f"Total number of documents: {num_documents}")

 #Original prompt:
question_answering_prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a virtual assistent named Pepe with an extense knowledge about the traffic regulations in Mexico City"),
      ("system", "Answer the user's questions based ONLY on the below context:\n\n{context}, if the context doesn't contain any relevant information to the question, don't try to make something up."),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Always answer to the user in spanish."),
])

def create_chatbot_response(user_input: str):
    retriever = new_db.as_retriever(search_kwargs={'k':3})

    query_transform_prompt = ChatPromptTemplate.from_messages(
    [MessagesPlaceholder(variable_name="messages"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation. Only respond with the query, nothing else. Always generate the query in spanish.")
    ])

    query_transforming_retriever_chain = RunnableBranch(
    (lambda x: len(x.get("messages", [])) == 1,
    (lambda x: x["messages"][-1].content) | retriever),
    query_transform_prompt | llm | StrOutputParser() | retriever).with_config(run_name="chat_retriever_chain")

    document_chain = create_stuff_documents_chain(llm, question_answering_prompt)

    demo_ephemeral_chat_history.add_user_message(user_input)

    #Printing the transformed query for debugging purposes
    # Note: This operation consumes resources from OpenAI and generates more tokens to process.
    if len(demo_ephemeral_chat_history.messages) > 1:
        query_transformed = query_transform_prompt | llm | StrOutputParser()
        qry = query_transformed.invoke({"messages":demo_ephemeral_chat_history.messages})
        print(f"PRINTING QUERY TRANSFORMED, CONTENT IS: {qry}")

    tokens_from_messages = countTokens(str(demo_ephemeral_chat_history.messages))
    #Printing the tokens count from messages to monitor resource usage
    print(f"Tokens count, MESSAGES contains: {tokens_from_messages} tokens")

    if tokens_from_messages >= 1500:
        purge_messages_history(tokens_from_messages)

    conversational_retrieval_chain = RunnablePassthrough.assign(
        context=query_transforming_retriever_chain).assign(answer=document_chain)

    try:
        with get_openai_callback() as cb:
            response = conversational_retrieval_chain.invoke({"messages": demo_ephemeral_chat_history.messages})
    except:
        # Handle error and remove last user_input
        purge_messages_history(tokens_from_messages)
        demo_ephemeral_chat_history.messages.pop(-1)
        return "Ocurrió un error, por favor intenta nuevamente."

    # Print token and cost information for monitoring
    print(f"\n\tPRINTING RESULTS OF CB TOKENS: \n\t{cb}")

    #Print the entire response in the terminal for debugging purposes
    print(f"\n\tPRINTING RESPONSE, CONTENT IS: \n\t{response}")

    if countTokens(response["answer"]) < 1000:
        demo_ephemeral_chat_history.add_ai_message(response["answer"])

    return response["answer"]


def purge_messages_history(tokens_from_messages: int):
    print(f"Tokens limit reached, there are {tokens_from_messages} tokens in MESSAGES")
    demo_ephemeral_chat_history.messages.pop(0)
    demo_ephemeral_chat_history.messages.pop(1)
    print("First message in historic messages deleted")
    tokens_from_messages = countTokens(str(demo_ephemeral_chat_history.messages))
    print(f"New tokens count. | MESSAGES contains: {tokens_from_messages} tokens")


def clear_history(count:int):
    demo_ephemeral_chat_history.messages.clear()
    return demo_ephemeral_chat_history.messages
