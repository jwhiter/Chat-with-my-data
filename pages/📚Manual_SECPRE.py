# Import prerequisite libraries
import streamlit as st
from streamlit_chat import message
from streamlit_modal import Modal
import sys
import os
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Append the parent directory of the current script to sys.path
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from manual_embed_docs import *
import os  # For environment variables
from io import StringIO
import PyPDF2
import yaml
from openai import AzureOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import json

def save_sources_to_file(sources):
    print(f"sources_text --> {sources}")
    sources_paragraph = " 📄 Fuentes para construir la respuesta 📄 \n\n"
    for index, sources_doc in enumerate(sources):
        sources_paragraph += f"Source {index+1}: \n" + "\n" + sources_doc.page_content + "\n\n"
    
    with open('sources.json', 'w') as f:
        json.dump(sources_paragraph, f)

def load_sources_from_file():
    try:
        with open('sources.json', 'r') as f:
            sources = json.load(f)
        return sources
    except FileNotFoundError:
        return []

def file_reader():
    embedding_model = AzureOpenAIEmbeddings(azure_deployment="text-embedding-ada-002")
    db = FAISS.load_local("faiss_index/Manual-SECPRE", embedding_model, allow_dangerous_deserialization=True)   
    return db
def on_click_sources():
    modal = Modal(key="Demo Key", title="Fuentes de la respuesta:")
    sources_paragraph = load_sources_from_file()
    with modal.container():
        st.write(sources_paragraph)
def main():
    """The main function that runs the chatbot application."""
    st.title("Chatea con el MANUAL SECPRE DE CIRUGÍA PLÁSTICA, REPARADORA Y ESTÉTICA") 
    
    st.session_state['history'] = []
    st.session_state['generated'] = ["Preguntame lo que quieras sobre el manual. Que necesitas saber? 🤗"]
    st.session_state['past'] = ["Hola!, Tengo muchas dudas 👋"]
    st.session_state['sources'] = []

    response_container = st.container()
    container = st.container()
    db = file_reader()
    qEngine_manual = Question_Engine_Manual(db)
    # User input form
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Tu pregunta:", placeholder="Pregunta", key='input')
            submit_button = st.form_submit_button(label='Enviar')
        if submit_button and user_input:
            output = qEngine_manual.get_answer(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output['result'])
            sources = output['source_documents']
            save_sources_to_file(sources)
            st.session_state['sources'] = sources

    # Display chat history
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="adventurer")
                message(st.session_state["generated"][i], key=str(i),is_user=False,  avatar_style="bottts")
    open_model = st.button(label='Fuentes de tu pregunta')
    if open_model:
        on_click_sources()
                # st.warning("Show sources: ", on_click=on_click_sources(st.session_state['sources']))

if __name__ == "__main__":
  password = "None"
  SOURCES = []
  password = st.text_input("Cual es la palabra Mágica?", type="password", label_visibility="visible")
  if password == st.secrets["PASSWORD"]:
    main()