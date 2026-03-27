**🎯 Proje'nin Amacı**
---
https://acikveri.ysk.gov.tr/secim-sonuc-istatistik/secim-sonuc sitesinden,  Belediye Başkanlığı Seçimleri - Milletvekili Genel Seçimleri - Cumhutbaşkanı Seçimleri Selenium ile çekilmiştir 
Ardından Bu Bilgiye sahip olan bir LLM ile Streamlit üzerinden soru cevap yapabileceğiniz bir program geliştirilmiştir 



**💻 Proje'de Kullanılan Teknolojiler** 
---
• Veri Doğrulama : Pydantic-Settings 

• ORM : (Async) SqlAlchemy 

• Web Otomasyonu : Selenium 

• Migration İşlemleri : Alembic 

• Arayüz : Streamlit 

• LLM Çalıştıran Platform : Ollama 

• LLM Model İsmi : kimi-k2.5:cloud

• Log İzleme : Logging 

• Ajan Yönetimi : Langchain 



**🗂️ Langchain_Sql_Secim_Portali Klasöründeki Dosyaların Özellikleri** 
---
• langchain_sql_yapilandirilmasi.py : Bu dosya'da Agent'ın kullanıcıların sorduğu sorulara cevap verebilmesi için Langchain'daki SQLDatabaseToolkit sınıfına bağlı olan Tooları kullanır ve ayrıca agent kısa süreli bir hafızaya da sahiptir 

• Main.py : Ana işlemler bu dosya'da yapılmaktadır 

• Models.py : Veritabanı'nda var olan tabloları buradadır 

• my_py_settings.py : Pydantic ile Veri Doğrulama işlemleri bu sayfada yapılır  

• sql_alchemy_islemleri.py : Veritabanındaki işlemler burada yapılır 

• streamlit_islemleri.py : Streamlit ile ilgili mesaj ekleme işlemleri burada yapılır 



**🗂️ Selenium_ile_Web_otomasyon Klasöründeki Dosyaların Özellikleri** 
---
• Donusum_modulu.py : Bu dosyada, selenium ile veri çekme sırasında string verileri başka bir formata dönüştürmek için kullanıldı 

• Milletvekili_ilceler_ozel_kod.py : Milletveki seçimlerinde ilçeleri almak için özel bir kod yazıldı 

• Models.py : Veritabanındaki tablolar burada yer alıyor 

• Pydantic_Page.py : Pydantic ile Veri Doğrulama işlemleri bu sayfada yapılır 

• selenium_islemleri.py : Selenium'da veri çekerken bu sayfa Main dosyası gibi kullanıldı 

• selenium_yardımcı_fonksiyonlar.py : Selenium'da bekleme tıklama ya da sayfa yüklenmesi gibi komutlar burada yer almaktadır 

• sql_alchemy_islemleri.py : Veritabanına kayıt atma, değer güncelleme ya da Select işlemleri burada yapılmaktadır 

• Turkiye_il_aday_veri_cekme_kodu.py : Cumhurbaşkanlığı Seçimlerinde, Adayların şehirlerde aldıkları oy sayilarini ve oy oranlarini almak için yaratıldı 

• Turkiye_ilceler_aday_veri_cekme.py : Cumhurbaşkanlığı Seçimlerinde, Adayların ilçelerde aldıkları oy sayilari ve oy oranlarini almak için yaratıldı 

• Turkiye_ilceler_veri_cekme_kodu.py : Milletvekili Genel Seçimlerinde ve Belediye Başkanlığı Seçimlerinde Partilerin ilçelerdeki oy sayilarini ve oy oranlarini almak için yaratıldı 

• Turkiye_iller_veri_cekme_kodu.py : Milletvekili Genel Seçimlerinde ve Belediye Başkanlığı Seçimlerinde Partilerin şehirlerdeki oy sayilarini ve oy oranlarini almak için yaratıldı 


Selenium_Secim_Portali_Projesi_Grafiği.png : Bu dosyada, işlemlerin nasıl yapıldığı kısa bir grafikle gösterilmektedir.



**📌 Ek Açıklama** 
Partilerin ve Adaylara ait olan oy sayisi ve oy oranlari verilerinin yanında, ek olarak, şehir ve ilçelerde yer alan Kayıtlı Seçmen Sayisi, Geçerli Oy Sayisi ve Oy Kullanan Seçmen Sayısı gibi veriler de veritabanına kayıt edilmiştir 


**Diğer Bilgiler**
⚠️ Bu depo (repository), projenin mimari yapısını ve kodlama standartlarını göstermek için tasarlanmıştır. Güvenlik ve gizlilik nedeniyle bazı API yapılandırmaları ve özel anahtarlar dahil edilmemiştir; bu sebeple proje "tak-çalıştır" modunda değildir, bir teknik portfolyo örneğidir.








