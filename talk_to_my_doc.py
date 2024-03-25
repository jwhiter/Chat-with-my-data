# Import prerequisite libraries
import streamlit as st
from streamlit_chat import message
from embed_docs import *
import os  # For environment variables
from io import StringIO
import PyPDF2
import yaml
from openai import AzureOpenAI


def file_reader(uploaded_file):
    if uploaded_file is not None: 
        db = Document(uploaded_file).get_db()
        return db
    return None

def main():
    """The main function that runs the chatbot application."""
    st.title("🙈 Bienvenida 🙈")
    st.write(f'Pasos a seguir para que no te pierdas')
    st.write(f'1) Sube el documento pdf')
    st.write(f'2) Empieza a chatear')
    uploaded_file = st.sidebar.file_uploader("Sube tu documento", type="pdf")
    db = file_reader(uploaded_file)
    if uploaded_file:
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # Initialize messages
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Acabo de leerme " + uploaded_file.name + " y estoy listo para responder tus preguntas. Que necesitas saber? 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hola!, me llamo Beatriz y tengo muchas dudas 👋"]
        
        # Create containers for chat history and user input
        response_container = st.container()
        container = st.container()
        # User input form
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Tu pregunta:", placeholder="Pregunta de Beatriz", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                qEngine = Question_Engine(user_input, db)
                output = qEngine.get_answer()['result']
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