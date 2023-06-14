import config
from config import os

import pinecone

import streamlit as st 

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

embeddings = OpenAIEmbeddings()

# initialize pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),  
    environment=os.getenv('PINECONE_API_ENV') 
)

docsearch = Pinecone.from_existing_index(index_name=os.getenv('PINECONE_INDEX_NAME'), embedding=embeddings)

# App framework
st.title(f'{os.getenv("STREAMLIT_APP_TITLE")} Knowledge Base AI')
prompt = st.text_input(f'Ask anything with the knowledge of {os.getenv("STREAMLIT_APP_TITLE")}\'s Knowledge Base:') 

# Prompt templates
prompt_question=f'As an {os.getenv("STREAMLIT_APP_TITLE")} expert, answer me the following: {prompt.format()}'

# Llms
llm = OpenAI(temperature=0.9) 
chain = load_qa_chain(llm, chain_type="stuff")

docs = docsearch.similarity_search(query=prompt_question)

# Show stuff to the screen if there's a prompt
if prompt: 
    answer = chain.run(input_documents=docs, question=prompt_question)

    st.write(answer)