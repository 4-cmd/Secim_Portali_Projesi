from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import cached_property
from langchain_ollama import ChatOllama
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_mistralai.chat_models import ChatMistralAI


class My_Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL : str 
    OLLAMA_MODEL_STR : str 
    LOG_File : str 
    MISTRAL_API_KEY : str 
    MISTRAL_MODEL_NAME : str
    OLLAMA_QWEN_MODEL_STR : str

    @cached_property
    def my_ollama_model(self):
        model_name = self.OLLAMA_MODEL_STR
        model = ChatOllama(model=model_name,time_out = 450)
        return model


    @cached_property
    def engine_of_sql_alchemy(self):
        database_url = self.DATABASE_URL
        engine = create_engine(url=database_url)
        return engine
    
    @cached_property
    def session_function(self):
        engine = self.engine_of_sql_alchemy
        SessionMaker = sessionmaker(bind=engine)
        session = SessionMaker()
        return session
    
    @cached_property
    def mistral_llm_model(self):
        api_key = self.MISTRAL_API_KEY
        model_name = self.MISTRAL_MODEL_NAME

        mistral_model = ChatMistralAI(api_key=api_key,name=model_name)

        return mistral_model

settings_of_pydantic = My_Settings()



