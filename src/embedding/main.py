import os

import numpy as np
from dotenv import load_dotenv
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_openai import OpenAIEmbeddings

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    TARGET_FILE = "../scraping/data.jsonl"
    loader = JSONLoader(
        file_path=TARGET_FILE,
        jq_schema='.',
        content_key='detail',
        json_lines=True
    )
    data = loader.load()
    input_texts = [d.page_content for d in data]

    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
    doc_result = embeddings.embed_documents(input_texts)


    print(len(doc_result))
    print(len(doc_result[0]))
    print(doc_result[0][:5])

    np.save('embeddings.npy', np.array(doc_result))

    print('Embedding Completed.')

if __name__ == "__main__":
    main()