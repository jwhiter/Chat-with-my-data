# Import prerequisite libraries
from openai import AzureOpenAI
import streamlit as st
from streamlit_chat import message
from embed_docs import *
import os  # For environment variables
from io import StringIO
import PyPDF2
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def file_reader(uploaded_file):
    if uploaded_file is not None: 
        db = Document(uploaded_file).get_db()
        return db
    return None

def main():
    """The main function that runs the chatbot application."""
    st.title("🙈 Welcome 🙈")
    st.write(f'Steps')
    st.write(f'1) Log in')
    st.write(f'2) Upload your file')
    uploaded_file = st.sidebar.file_uploader("Upload File", type="pdf")
    db = file_reader(uploaded_file)
    if uploaded_file:
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # Initialize messages
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["I'm here to help you with " + uploaded_file.name + "? 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey ! 👋"]
        
        # Create containers for chat history and user input
        response_container = st.container()
        container = st.container()
        # User input form
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Any question:", placeholder="Question", key='input')
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
  password = st.text_input("Magical word?", type="password", label_visibility="visible")
  if password == st.secrets["PASSWORD"]:
    main()