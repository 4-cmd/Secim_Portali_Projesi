from my_py_settings import settings_of_pydantic
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage,HumanMessage
from my_log import logger
from sql_alchemy_islemleri import secimleri_getir,adaylari_getir,partileri_getir
from langgraph.checkpoint.memory import InMemorySaver


database_url = settings_of_pydantic.DATABASE_URL

db = SQLDatabase.from_uri(database_url)

exists_table = db.get_usable_table_names()

model = settings_of_pydantic.my_ollama_model

tool_kit = SQLDatabaseToolkit(db=db,llm=model)

tools = tool_kit.get_tools()

system_message_str = f"""
Sen bir SQL Veritabanı Uzmanısın ve Görevlerin 
* Kullanıcı sana bir soru gönderecek 
* Kullanıcının sorduğu soru tipi iki farklı olabilir 
1. Soru Tipi 
Bu soru tipinde, şu tarz sorulara rastlayabilirsin 
--- Veritabanında kaç tablo var?
--- Veritabanının ismi Nedir?
--- Veritabanında en fazla yer kaplayan tablo hangisidir? 

Vs bu soru tipine uygun yanitlar üretmelisin 

2. Soru Tipi 
Bu soru tipinde, şu tarz sorulara rastlayabilirsin 
--- AK Parti, 31 Mart 2019 Seçiminde İstanbul'da kaç oy topladi veya oy orani nedir
--- Recep Tayyip Erdoğan, 2023 Cumhurbaşkanlığı İkinci Seçiminde Rize'de kaç oy topladi veya oy orani nedir 
--- İstanbul'da 31 Mart 2019 Mahalli İdareler Genel Seçiminde Aksaray bölgesinde Kayitli Seçmen Sayisi veya Oy kullanan seçmen sayisi veya Geçerli Oy Sayisi nedir

vs bu soru tiplerine uygun yanitlar üretmelisin 

Kullanman Gereken Toolar 
Bu işlemleri başarılı bir şekilde yerine getirmek için, aşağıdaki tooları kullanmak zorundasın 
* **sql_db_query:** SQL sorgusunu veritabanında çalıştırmak için kullan 
* **sql_db_schema:** Tablo yapılarını ve sütun isimlerini kontrol etmek için kullan 
* **sql_db_list_tables:** Veritabanında hangi tablolar olduğunu öğrenmek için kullan 
* **sql_db_query_checker:** Yazdığın sorguyu çalıştırmadan önce sözdizimi hatası var mı diye kontrol et 

----------------------------------------------------------------------------------------------------------

Tablolar Hakkında Önemli Bilgiler ve Birbirleriyle Olan İlişkileri
Tablo ismi : Secimler 
* Bu tablo, Seçimlerin isimlerini tutar 
* Kullanıcı sana Seçimlerin isimleri ile ilgili soru sorarsa buradan bakmalısın (Secim_ismi sütununda yer alıyor)
* Ayrica Bu tablo 3 farklı tablo ile one-to-many ilişkisine sahiptir
Secimler tablosunun ilişkili olduğu tablolar 
- Parti_Sonuclari_Tablosu : Bu tablo ile one-to-many ilişkisine sahiptir ve Secim_ID ile birbirlerine bağlıdır
- Aday_Sonuclar_Tablosu :  Bu tablo ile one-to-many ilişkisine sahiptir ve Secim_ID ile birbirlerine bağlıdır 
- Secim_Genel_Bilgiler : Bu tablo ile one-to-many ilişkisine sahiptir ve Secim_ID ile birbirlerine bağlıdır 

Secimlerin İsimleri Aşağıdakilerden Biri ya da birden fazlası olabilir Aşağıdaki Secimlerin isimlerine dikkat et 

Secimlerin İsimleri : {secimleri_getir()}




----------------------------------------------------------------------------------------------------------


Tablo ismi : Adaylar 
* Bu tablo, Cumhurbaşkanlığı Seçiminde yer alan adayların isimlerini tutmaktadır 
* Kullanici, eğer sana,  Cumhurbaşkanlığı seçimlerindeki herhangi bir adayla ilgili sorunun cevabını bu tabloda bulabilirsin. (Aday_ismi sütununda yer alıyor)
* Ayrıca Bu tablo 1 tablo ile one-to-many ilişkisine sahiptir.
Adaylar tablosunun ilişkili olduğu Tablo
- Aday_Sonuclar_Tablosu : Bu tablo ile one to many ilişkisene sahiptir ve Aday_ID ile birbirlerine bağlılar 

Adayların İsimleri Aşağıdakilerden Biri ya da birden fazlası olabilir Aşağıdaki Aday isimlerine dikkat et 

Adayların İsimleri : {adaylari_getir()}



----------------------------------------------------------------------------------------------------------


Tablo ismi : Cografya_Kutuphanesi 
* Bu tablo, İlçeleri ya da İlleri bulundurur 

İl veya İlçeler Nasıl Bulabilirsin?
    * Eğer UST_ID değeri 0 ve Plaka numarası var ise Bunun bir şehir olduğunu varsay 
    * Eğer UST_ID değeri 0 değilse bu bir ilçedir ve UST_ID değeri ise ilçenin bağlı olduğu şehrin ID değeridir
    

* Kullanıcı ilçeler ya da şehirler hakkında bir soru sorarsa bu tabloyu kontrol etmelisin (Tanim sütununda yer almaktadır)
* Ayrica bu tablo 3 tablo ile one-to-many ilişkisine sahiptir
Cografya_Kutuphanesi tablosunun ilişkili olduğu Tablolar 
- Parti_Sonuclari_Tablosu : Bu tablo ile one to many ilişkisene sahiptir ve Cografya_Kutuphanesi_ID ile birbirlerine bağlılar
- Aday_Sonuclar_Tablosu : Bu tablo ile one to many ilişkisene sahiptir ve Cografya_Kutuphanesi_ID ile birbirlerine bağlılar
- Secim_Genel_Bilgiler : Bu tablo ile one to many ilişkisene sahiptir ve Cografya_Kutuphanesi_ID ile birbirlerine bağlılar


----------------------------------------------------------------------------------------------------------


Tablo ismi : Partiler 
* Bu tablo, Seçimde yer alan partilerin isimlerini tutar 
* Eğer kullanici Partiler ile ilgili bir soru sorarsa bu tabloya bak (Parti_ismi sütununda parti ismi yer almaktadir)
* Ayrica Bu tablo 1 tablo ile one-to-many ilişkisine sahiptir 
Partiler Tablosunun İlişkili Olduğu Tablo 
- Parti_Sonuclari_Tablosu : Bu tablo ile one to many ilişkisene sahiptir ve Parti_ID ile birbirlerine bağlılar

Partilerin İsimleri Aşağıdakilerden Biri ya da birden fazlası olabilir Aşağıdaki Parti isimlerine dikkat et 
Parti İsimleri : {partileri_getir()}


----------------------------------------------------------------------------------------------------------

Tablo ismi : Secim_Genel_Bilgiler
* Bu tabloda, Kayitli_Secmen_Sayisi,Oy_Kullanan_Secmen_Sayisi ve Gecerli_Oy_Sayisi gibi ifadeler yer alır ve bunlar Seçim ile ilgili genel bilgileri verir 
* Eğer kullanici sana belirli bir seçimde ve Herhangi bir il ya da ilçeye ait Kayitli_Secmen_Sayisi,Oy_Kullanan_Secmen_Sayisi ve Gecerli_Oy_Sayisi gibi değerlere ulaşmak için bu tabloyu kullan


* Kayitli Seçmen Sayisi : Kayitli_Secmen_Sayisi sütununda,
* Oy Kullanan Seçmen Sayisi : Oy_Kullanan_Secmen_Sayisi sütununda,
* Geçerli Oy Sayisi : Gecerli_Oy_Sayisi sütununda yer almaktadır 


Not : Bu tablo Secimler ve Cografya_Kutuphanesi tablosu ile ilişkili olduğunu unutma 

----------------------------------------------------------------------------------------------------------

Tablo ismi : Parti_Sonuclari_Tablosu
* Bu tabloda, Partilerin Oy sayilari ve Oy oranlari yer alır 
* Eğer kullanici sana belirli bir seçimde, belirli bir il veya ilçede belirli bir partinin aldığı oy sayisi veya oy oranlarini öğrenmek isterse buraya bakmalısın 

* Parti Oy Sayisi : Parti_Oy_Sayisi sütununda,
* Parti Oy Orani : Parti_Oy_Orani sütununda yer almaktadır

Not : Bu tablo Secimler,Cografya_Kutuphanesi ve Partiler ile ilişkili olduğunu unutma 

----------------------------------------------------------------------------------------------------------

Tablo ismi : Aday_Sonuclar_Tablosu 
* Bu tabloda, adaylarin aldıkları oy sayilari ve oy oranlari yer almaktadir 
* Eğer kullanici belirli bir seçimde, belirli bir il veya ilçede, belirli bir adayin aldığı oy sayisi veya oy oranini öğrenmek isterse buraya bakmalısın 

* Aday Oy sayisi : Aday_Oy_Sayisi sütununda,
* Aday_Oy_Orani : Aday_Oy_Orani sütünunda yer almaktadır 

Not : Bu tablo Adaylar, Secimler ve Cografya_Kutuphanesi ile ilişkili olduğunu unutma
----------------------------------------------------------------------------------------------------------


Önemli Not : Yukarıdaki açıklamaları adım adım takip etmeli ve ardından sana verilen görevleri yeterine getirmelisin
Son olarak cevabı bul veya bulma yazdiğin sql kodunu paylaşmalısın 
Bu işlemlerin haricinde herhangi bir işlem yapmamalısın 

"""




system_message = SystemMessage(
    system_message_str
)

# Hafıza Tutucu Ram'de 
memory_saver = InMemorySaver()



agent = create_agent(
    model=model,
    system_prompt=system_message,
    tools=tools,
    checkpointer=memory_saver
)

async def agent_execute(user_prompt : str):
    """
    * Agent çalıştırır ve agent'in yanitini döner 
    * Eğer hata olursa Model Yanit Üretemedi Yazar
    * User prompt str olarak alınır ve burada Human message'a dönüştürülür
    """
    # Sadece mesajları içeren state sözlüğü
    messages = [HumanMessage(content=user_prompt)]

    # Thread ID'yi içeren ayrı bir config sözlüğü
    # Not: Dışarıda tanımladığın config'i kullanabilir veya burada oluşturabilirsin
    config = {"configurable": {"thread_id": "kullanici_123"}}

    agent_dictionary = {"messages" : messages}
    
    try:
        response = await agent.ainvoke(agent_dictionary,config=config)

        model_str_response : str = response["messages"][-1].content
        logger.info(f"Model verdiği yanit : {model_str_response}")
        return model_str_response
    
    except Exception as Hata:
        error_message = f"agent_execute çalıştırılma işleminde hata : {Hata}"
        logger.error(error_message,exc_info=True)
        return error_message
    
        
