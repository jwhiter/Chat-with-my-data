# Import prerequisite libraries
import streamlit as st
from streamlit_chat import message
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


def file_reader():
    embedding_model = AzureOpenAIEmbeddings(azure_deployment="text-embedding-ada-002")
    db = FAISS.load_local("faiss_index/wounds-and-lacerations-emergency-care-and-closure", embedding_model, allow_dangerous_deserialization=True)   
    return db

def main():
    """The main function that runs the chatbot application."""
    st.title("Chatea con el libro: Heridas y cortes - tratamiento y sutura de urgencia / Alexander T. Trott") 
    
    st.session_state['history'] = []
    st.session_state['generated'] = ["Estoy listo para responder tus preguntas. Que necesitas saber? 🤗"]
    st.session_state['past'] = ["Hola!, Tengo muchas dudas 👋"]
    # if 'history' not in st.session_state:
    #     st.session_state['history'] = []

    # # Initialize messages
    # if 'generated' not in st.session_state:
    #     st.session_state['generated'] = ["Estoy listo para responder tus preguntas. Que necesitas saber? 🤗"]

    # if 'past' not in st.session_state:
    #     st.session_state['past'] = ["Hola!, me llamo Beatriz y tengo muchas dudas 👋"]
    
    # Create containers for chat history and user input
    response_container = st.container()
    container = st.container()
    # User input form
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Tu pregunta:", placeholder="Pregunta de Beatriz", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            db = file_reader()
            qEngine_manual = Question_Engine_Manual(db)
            output = qEngine_manual.get_answer(user_input)['result']
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    # Display chat history
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-ears")
                message(st.session_state["generated"][i], key=str(i), avatar_style="croodles")

if __name__ == "__main__":
  password = "None"
  password = st.text_input("Cual es la palabra Mágica?", type="password", label_visibility="visible")
  if password == st.secrets["PASSWORD"]:
    main()