from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import tiktoken
import time

def vectorstore_chatbot():
    documents =[]

    loader1 = TextLoader("./raw_data/scraped_data.txt")
    documents.append(loader1.load())

    loader2 = TextLoader("../raw_data/scraped_data2.txt")
    documents.append(loader2.load())


    loader3 = PyPDFLoader("../raw_data/Reglamento_CDMX.pdf")
    documents.append(loader3.load())


    #for file_path in file_paths:
    #    if file_path.endswith(".txt"):
    #        loader = TextLoader(file_path)
    #    elif file_path.endswith(".pdf"):
    #        loader = PyPDFLoader(file_path)
    #    else:
    #        print(f"Unsupported file format for {file_path}")

    #    text = loader.load()

    #    documents.append(text)


    #print(f"Longitud de page_content es: {len(documents)}")
    #print(documents)
    text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    print(len(docs))
    print(sum(countTokens(d.page_content) for d in docs))
    i=1
    embeddings = OpenAIEmbeddings(show_progress_bar = True)
    db = FAISS.from_documents([docs[0]],embeddings)
    while i <= 50:
        db1 = FAISS.from_documents(docs[i:i+20], embeddings)
        i +=20
        db.merge_from(db1)
        print(i)
        time.sleep(30)

    return db

def countTokens(query: str):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens=len(encoding.encode(query))
    return num_tokens


#vectorstore=vectorstore_chatbot()
#vectorstore.save_local("data_base_prueba")


embeddings = OpenAIEmbeddings()
#new_db = FAISS.load_local("data_base", embeddings)
#print(len(new_db))

faiss_instance = FAISS.load_local("data_base_prueba", embeddings)
num_documents = len(faiss_instance.index_to_docstore_id)
print(f"Total number of documents: {num_documents}")
