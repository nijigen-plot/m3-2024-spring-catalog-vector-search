import json
import os
import time

import numpy as np
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
embeddings_texts = np.load('../embedding/embeddings.npy')

def create_markdown(matching_json : json):
    return f"""
    ## サークル名: {matching_json['name']}

    **場所**: {matching_json['booth']}

    **URL**: {matching_json['url']}

    > {matching_json['detail']}
    
    """

texts = []
with open('../scraping/data.jsonl', 'r') as file:
    for line in file:
        texts.append(json.loads(line))
        

st.title("2024 春M3 サークル検索くん")
st.subheader("入力ワードから関連のあるサークルを検索！:sparkles:")
st.markdown("[https://www.m3net.jp/attendance/circle2024sR.php](https://www.m3net.jp/attendance/circle2024sR.php) の情報を活用しています。")

input_text = st.text_input(
    "キーワードを入力",
    value=None,
    key='input_text'
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if input_text is not None:
    try:
        with st.spinner("検索中..."):
            time.sleep(0.5)
            input_embedding = embeddings.embed_query(input_text)
            distances = [np.dot(embedding, input_embedding) for embedding in embeddings_texts]
            top3_indexes = np.argsort(distances)[-3:][::-1]
            
            with st.chat_message("assistant", avatar='🎵'):
                st.markdown(f"""{create_markdown(texts[top3_indexes[0]])}""")
            with st.chat_message("assistant", avatar='🎵'):
                st.markdown(f"""{create_markdown(texts[top3_indexes[1]])}""")
            with st.chat_message("assistant", avatar='🎵'):
                st.markdown(f"""{create_markdown(texts[top3_indexes[2]])}""")
            
    except Exception as e:
        st.error(f"予期しないエラーが発生しました: {e}")