from pydantic_settings import BaseSettings,SettingsConfigDict

class Base_Class(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL_STR : str 


py_settings_variable = Base_Class()

