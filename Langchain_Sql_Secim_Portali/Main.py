from langchain_sql_yapilandirilmasi import agent_execute
from my_log import logger
from my_py_settings import settings_of_pydantic
from streamlit_islemleri import adding_a_message_to_messages,printing_the_messages
import streamlit as st
import asyncio
import nest_asyncio
nest_asyncio.apply()


printing_the_messages()

async def Main():
    user_input = st.chat_input("Yaziniz")
    
    if user_input:
        logger.info(f"Kullanicinin girdiği mesaj : {user_input}")
        adding_a_message_to_messages(arg_content=user_input)

        ai_answer = await agent_execute(user_prompt=user_input)

        logger.info(f"Aİ yaniti : {ai_answer}")
        adding_a_message_to_messages(arg_content=ai_answer,is_human=False)

asyncio.run(Main())

# streamlit run Main.py