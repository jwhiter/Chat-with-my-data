
import streamlit as st
  
# stm.set_page_config(page_title = " 🙈 Bienvenida a tu chatbot 🙈") 
st.title("Esta es la página de inicio") 

st.write(f'Instrucciones a seguir: ')
st.write(f'Elige entre:')
st.write(f'- Chatear con tu manual')
st.write(f'- Chatear con tu documento')
st.write(f'   1) Sube el documento pdf')
st.write(f'   2) Empieza a chatear')
st.sidebar.success("Escoge entre estas opciones") 