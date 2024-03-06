from PyPDF2 import PdfReader
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import AzureChatOpenAI
from langchain.chat_models import ChatOpenAI
import openai
import os
import streamlit as st

class Document:
    def __init__(self, file, all_text = "") -> None:
        self.file_name = file.name.replace(".pdf", "").replace(".", "_")
        self.all_text = all_text
        self.file = file
        openai.api_key = st.secrets['AZURE_OPENAI_API_KEY']
        openai.api_base = st.secrets["AZURE_OPENAI_ENDPOINT"]
        openai.api_type = "azure"
        openai.api_version = "2023-05-15"
        os.environ["AZURE_OPENAI_API_KEY"] = openai.api_key
        os.environ["AZURE_OPENAI_ENDPOINT"] = openai.api_base
        os.environ["OPENAI_API_TYPE"] = openai.api_type
        os.environ["OPENAI_API_KEY"] = openai.api_key
        os.environ["OPENAI_ENDPOINT"] = openai.api_base
 

    def create_chunks(self, chunk_size=1000):
        if self.all_text == "":
            #Read the file
            pdf_reader = PdfReader(self.file)
            all_text = ""
            for page in range(len(pdf_reader.pages)):
                all_text += pdf_reader.pages[page].extract_text()
            self.all_text = all_text
            print("Document read")
        
        # Split into document objects   
        text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=chunk_size,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.create_documents([self.all_text])
        print("Document processed")
        return chunks 
    
    def get_db(self):
        directory=f"./chroma/{self.file_name}"
        embedding_model = AzureOpenAIEmbeddings(azure_deployment="text-embedding-ada-002")
        if os.path.exists(directory):
            # Load presaved db
            vectordb = Chroma(persist_directory=directory, embedding_function=embedding_model)
        else:
            # Create new db
            print("New doc")
            chunks = Document.create_chunks(self)
            vectordb = Chroma.from_documents(
                chunks, 
                embedding_model,
                persist_directory=directory
            )
            vectordb.persist() # This stores the db in the specified folder
        return vectordb
    

class Question_Engine: 
    def __init__(self, query, vectordb) -> None:
        self.query = query
        self.vectordb = vectordb

    def get_answer(self):
        llm=AzureChatOpenAI(deployment_name='gpt-4', 
                      model_name='gpt-4', 
                      temperature=0, 
                      api_version="2023-08-01-preview")
        qa_chain = RetrievalQA.from_chain_type(
            llm = llm, 
            chain_type="stuff", 
            retriever=self.vectordb.as_retriever(),
            return_source_documents=True,
        )
        llm_response = qa_chain({"query": self.query})
        return llm_response