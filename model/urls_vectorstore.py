from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from utils import loadJsonCustom_with_separators, countTokens
import time

#Load the documents, our PDF file and our Json file:
def vectorstore_chatbot():
    """
    Create and populate a FAISS vector store with documents from a PDF file and a JSON file.

    Returns:
        FAISS: A FAISS vector store containing embeddings of the documents.
    """
    documents =[]

    # Load the pdf file
    loader1 = PyPDFLoader("./raw_data/Reglamento_CDMX.pdf")
    documents.append(loader1.load())

    # Load the JSON file
    loader2 = loadJsonCustom_with_separators("./raw_data/new_json_separator.json")
    documents.append(loader2)

    embeddings = OpenAIEmbeddings(show_progress_bar = True)
    db = FAISS.from_texts(["foo"], embeddings)

    for doc in documents:
        i=0
        jump = 400
        print(f"\nCreating embeddings from file: {doc[0].metadata['source']} with {len(doc)} documents ...")
        while i <= len(doc):
            print(f"Total tokens in range [{i}:{i+jump}] of documents is {sum(countTokens(d.page_content) for d in doc[i:i+jump])} tokens")
            db1 = FAISS.from_documents(doc[i:i+jump], embeddings)
            i += jump
            db.merge_from(db1)
            print(f"Merge done, waiting for 60 seconds...")
            time.sleep(60)

    return db

# Call the function
vectorstore=vectorstore_chatbot()

# Save FAISS index locally
vectorstore.save_local("./raw_data/vectorstore_with_separators")
