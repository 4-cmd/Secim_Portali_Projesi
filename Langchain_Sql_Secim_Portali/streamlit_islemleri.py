import streamlit as st 
from langchain_core.messages import AIMessage,HumanMessage
from my_log import logger


if not "messages" in st.session_state:
    logger.info(f"Mesajlar yaratiliyor")
    st.session_state.messages = []


def printing_the_messages():
    """
    * Streamlit'deki mesajları yazdirir
    """
    mesaj_listesi = st.session_state.messages
    logger.info(f"Mesaj Listesi yazdiriliyor")
    for mesaj in mesaj_listesi:
        if isinstance(mesaj, HumanMessage):
            with st.chat_message("human"):
                st.markdown(mesaj.content)
        
        elif isinstance(mesaj, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(mesaj.content)
                
def adding_a_message_to_messages(arg_content : str,is_human : bool = True):
    """
    * Streamlit'deki mesajlara yeni bir mesaj ekler 
    * AI ise AI olarak Human ise Human olarak
    """
    if is_human:
        with st.chat_message("human"):
            st.markdown(arg_content)
            instance = HumanMessage(arg_content)
            st.session_state.messages.append(instance)
    
    else:
        with st.chat_message("assistant"):
            st.markdown(arg_content)
            instance = AIMessage(arg_content)
            st.session_state.messages.append(instance)
    


