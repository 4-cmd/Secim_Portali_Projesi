import logging
from my_py_settings import settings_of_pydantic

file_path = settings_of_pydantic.LOG_File


logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# Ne zaman gerçekleştiğini yazar - Hangi logger isminin attığını yazar - Mesajın kritiklik seviyesini yazar - Senin yazdığın asıl mesaj
   
handlers=[
logging.FileHandler(f"{file_path}", encoding="utf-8"), # Dosyaya kaydeder
logging.StreamHandler() # Terminale de yazdırır
]
)
logger = logging.getLogger("Log_Terminali")
