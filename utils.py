import json
from langchain_core.documents import Document
import tiktoken

def loadJsonCustom_with_separators(jsonpath:str):
    """
    Load a JSON file into smaller documents with separators.

    Parameters:
        jsonpath (str): The path to the JSON file.

    Returns:
        list: A list of documents.
    """
    with open(jsonpath, 'r',encoding='utf-8') as json_file:
        data = json.load(json_file)

    docs = []
    for d in data:
        for s in d['urlInfo']['sections']:
            docs.append(Document(page_content=s['section']+s['content'],metadata={'source':d['urlInfo']['url']}))

    return docs


def countTokens(query: str):
    """
    Count the number of tokens.

    Parameters:
        query (str): The query string.

    Returns:
        int: The number of tokens.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens=len(encoding.encode(query))
    return num_tokens
