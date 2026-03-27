from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_yardımcı_fonksiyonlar import wait_for_page_load
from selenium.webdriver.common.by import By
from sql_alchemy_islemleri import (Yeni_Bir_Parti_Ekle,
                                   Yeni_Bir_Secim_Ekleme
                                   ,Cografya_Kutuphanesine_Yeni_Bir_Deger_Ekleme
                                   ,Parti_Sonuclarina_Yeni_Deger_Ekleme
                                   ,Parti_Sonuclarinin_Oy_Oranini_Guncelleme,
                                   Secim_Genel_Bilgiler_yeni_deger_yukleme
                                   )
from Donusum_modulu import from_string_to_float,from_string_to_int


from typing import Dict
from selenium.webdriver.remote.webelement import WebElement



def tablo_basliklari_icin_bekleme_fonksiyonu(tablo_thead_tr_elementi : WebElement,driver : WebDriver):
    """
    Tablo Başlıkları bazen 5 ile sınırlı kalabiliyor halbuki en az 15'iz üzerinde değer var 
    Bu yüzden, bunun önüne geçmek için sayfada 5'den fazla değer bulana kadar sonsuza kadar arama yapmak zorundayız
    tablo_thead_tr_elemetleri : bu tabloda bulunan tek tryi verir ardından biz bunun içinden th elementlerini yukarıdaki koşula göre alana kadar bekleriz
    """

    while True:
        th_degerleri = tablo_thead_tr_elementi.find_elements(By.TAG_NAME,"th")
        if len(th_degerleri) > 5:
            print(f"Tablo başlıkları başarıyla alındı, toplam başlık sayısı : {len(th_degerleri)}")
            return th_degerleri
        else:
            print(f"Tablo başlıkları henüz tam olarak yüklenmedi, tekrar deneniyor... Mevcut başlık sayısı : {len(th_degerleri)}")
            wait_for_page_load(driver=driver)

Parti_ismi_ve_Parti_ID_sözlüğü : Dict[str,int] = {}

def Parti_isim_ve_sozlukten_Parti_ID_Alma(indeks_değeri) -> int:
    """
    * Parti_ismi_ve_Parti_ID_sözlüğü'den parti değeri alınacak 
    * indeks değeri atılacak 
    \n\n

    * Örneğin : Ak Partinin Oy sayilarindaki indeks değeri 5'tir. 
    Sözlükte 0.ci indekste Ak partinin ID değeri yer almaktadır 
    \n
    * Bu işlem bu fonksiyonda yapılacak 
    ve en sonunda partinin ID değeri döndürülecektir
    
    """
    parti_id_listesi = list(Parti_ismi_ve_Parti_ID_sözlüğü.values())
    parti_id_degeri = parti_id_listesi[indeks_değeri - 5]
    
    
    print(f"Parti ID döndürülüyor ve Partinin ID Değeri : {parti_id_degeri}")
    return parti_id_degeri

async def Tablo_Basliklarindan_Partilerin_isimlerini_ve_ID_değerlerini_alma(tablo_th_baslik_degerleri : list[WebElement]):
    """
    * Tablo başlıklarını alır 
    * Ardından Tablo başlığında Partinin ismi olur mesela AK Parti 
    * AK Partinin ID değeri alınır 
    * Ve ak partinin str isim değerini ve ak partinin ID değerini bir sözlüğe atar ve en sonunda döndürür
    """
    Parti_ismi_ve_Parti_ID_sözlüğü : dict[str,int] = {}
    # Tablo Başlıkları için 
    for index,th in enumerate(tablo_th_baslik_degerleri):
        th_ismi = th.text.strip()
        print(f"Tablo başlığı {index} : {th_ismi}")

        # 5.ci indeksten itibaren, parti isimleri gelmektedir, bu yüzden 5.ci indeksten itibaren parti isimlerini alıyoruz
        # 5.inci indexde Akparti vardır

        if index >= 5:
            parti_ismi = th_ismi
            print(f"Parti ismi : {parti_ismi}")

            Parti_ID = await Yeni_Bir_Parti_Ekle(parti_ismi=parti_ismi)
            Parti_ismi_ve_Parti_ID_sözlüğü[parti_ismi] = Parti_ID
            print(f"Parti_ismi_ve_Parti_ID_sözlüğü yeni bir değer yüklendi\nParti ismi : {parti_ismi}\nParti ID : {Parti_ID}")
    
    print(f"Parti isim ve Parti ID sözlüğü döndürülüyor ")
    return Parti_ismi_ve_Parti_ID_sözlüğü

async def Secim_Genel_Bilgiler_yeni_deger_yukleyen_function(Kayitli_Secmen_Sayisi : str,
                                                            Oykullanan_Secmen_Sayisi : str,
                                                            Gecerli_Oy_Sayisi : str,
                                                            şehir_ID_degeri : int,
                                                            Secim_ID : int):
    """
    * Secim Genel Bilgiler tablosuna yeni değer ekler 
    * Fonksiyonun amacı gereksiz kod kalabalığınının önüne geçmektir 
    """
    Kayitli_Secmen_Sayisi_int = from_string_to_int(Kayitli_Secmen_Sayisi)
    Oykullanan_Secmen_Sayisi_int = from_string_to_int(Oykullanan_Secmen_Sayisi)
    Gecerli_Oy_Sayisi_int = from_string_to_int(Gecerli_Oy_Sayisi)

    print(f"Kayitli_Secmen_Sayisi : {Kayitli_Secmen_Sayisi_int}\nOykullanan_Secmen_Sayisi : {Oykullanan_Secmen_Sayisi_int}\nGecerli_Oy_Sayisi : {Gecerli_Oy_Sayisi_int}")
    _ = await Secim_Genel_Bilgiler_yeni_deger_yukleme(Kayitli_Secmen_Sayisi=Kayitli_Secmen_Sayisi_int,
                                            Oy_Kullanan_Secmen_Sayisi=Oykullanan_Secmen_Sayisi_int,
                                            Gecerli_Oy_Sayisi=Gecerli_Oy_Sayisi_int,
                                            Cografya_Kutuphanesi_ID=şehir_ID_degeri,Secim_ID=Secim_ID)





async def Turkiye_tablosu_ozel_selenium_kodu(driver : WebDriver,Secim_ID : int):
    global Parti_ismi_ve_Parti_ID_sözlüğü
    """
    * Türkiye genelindeki illerin örneğin AKSARAY - Amasya - Konya şehirlerinde Partilerin ne kadar oy aldığını gösteren kod bloğudur 
    * İLLER TOPLAMI adında tabloda bir bölüm var buradan emin olabilirsin 
    * Bu kod bloğunun yazılmasının sebebi daha düzenli bir yapı kurmaktır 
    """
    wait_for_page_load(driver=driver)

    # Burada Türkiye Genelindeki İllerin sonuçları yer almaktadır,
    # Buradan sonra, ilk önce tablonun başlıklarını alacağız Burada parti isimleri yer alıyor
    # Tek bir tablo başlığı olduğu için bir tanesini alabilirsin
    tablo_thead = driver.find_element(By.TAG_NAME,"thead")
    tablonun_tr_degeri = tablo_thead.find_element(By.TAG_NAME,"tr")
    thead_listesi = tablo_basliklari_icin_bekleme_fonksiyonu(tablo_thead_tr_elementi=tablonun_tr_degeri,driver=driver)




    Parti_ismi_ve_Parti_ID_sözlüğü = await Tablo_Basliklarindan_Partilerin_isimlerini_ve_ID_değerlerini_alma(tablo_th_baslik_degerleri=
                                                                                                            thead_listesi)

        
    # Az Önce Parti İsimleri ve ID değerlerini aldık. Şimdi de tablonun kendisinde bulunan değerleri alalım 
    # Tek bir tane tbody olduğu için tek bir tane tbody alabiliriz

    tablo_tbody = driver.find_element(By.TAG_NAME,"tbody")
    tablodaki_tr_ler = tablo_tbody.find_elements(By.TAG_NAME,"tr")

    kayit_edilen_Parti_Sonuclarinin_ID_degerleri : list[int] = []
    
    # Tablonun genel yapisi için
    for index,tablodaki_tr in enumerate(tablodaki_tr_ler):
        print(f"Tablodaki tr index değeri : {index}")
        if index == 0 or index == 1:
            # Burada genel sonuçlar yer alıyor İLLER TOPLAMI nın yanında 58.259	Kayıtlı Seçmen Sayısı var bu yüzden atlandı
            print(f"Genel sonuçların bulunduğu tr atlanıyor index değeri : {index}")
            continue
        

        
        

        if index %2 == 0: # Çift haneli indekslerde, oy sayilari yer almaktadır 
            oy_sayilarini_barındıran_tdler = tablodaki_tr.find_elements(By.TAG_NAME,"td")
            şehir_ID_degeri = 0
            for oy_sayisi_td_index,oy_sayisi_td in enumerate(oy_sayilarini_barındıran_tdler):
                oy_sayisi_string = oy_sayisi_td.text.strip()
                if oy_sayisi_td_index == 0:
                    print(f"Burada sıra numarası yer aldığı için atlanıyor : {oy_sayisi_string}")
                    continue

                if oy_sayisi_td_index == 1:
                    print(f"Burada şehir ismi yer aldığı için Şehir adi veritabanına kayıt ediliyor : {oy_sayisi_string}")
                    şehir_ismi = oy_sayisi_string
                    Cografya_Kutuphanesi_ID = await Cografya_Kutuphanesine_Yeni_Bir_Deger_Ekleme(tanım_ekleme=şehir_ismi)
                    print(f"Cografya_Kutuphanesi tablosuna yeni bir değer eklendi : {şehir_ismi} ID değeri : {Cografya_Kutuphanesi_ID}")
                    şehir_ID_degeri = Cografya_Kutuphanesi_ID
                    continue
                
                if oy_sayisi_td_index >= 2 and oy_sayisi_td_index < 5: # Secim Genel Bilgilere yeni değerler ekler
                    # Burada Kayıtlı Seçmen Sayısı - Oy Kullanan Seçmen Sayısı - Geçerli Oy Toplamı yer almaktadır ve özel bir işlem yapılacak
                    Kayitli_Secmen_Sayisi = oy_sayilarini_barındıran_tdler[2].text.strip()
                    Oykullanan_Secmen_Sayisi = oy_sayilarini_barındıran_tdler[3].text.strip()
                    Gecerli_Oy_Sayisi = oy_sayilarini_barındıran_tdler[4].text.strip()

                    _ = await Secim_Genel_Bilgiler_yeni_deger_yukleyen_function(Gecerli_Oy_Sayisi=Gecerli_Oy_Sayisi,
                                                                                Oykullanan_Secmen_Sayisi=Oykullanan_Secmen_Sayisi,
                                                                                Kayitli_Secmen_Sayisi=Kayitli_Secmen_Sayisi,
                                                                                Secim_ID=Secim_ID,
                                                                                şehir_ID_degeri=şehir_ID_degeri)
                    
                    print(f"Seçimler genel tablosuna değerler eklendi ve bu satır atlanıyor index değeri ve oy_sayilarini_barındıran_tdler'in 2 ila 4 indeksli satırları atlanıyor")
                    continue


                
                parti_ID_degeri = Parti_isim_ve_sozlukten_Parti_ID_Alma(indeks_değeri=oy_sayisi_td_index)
                int_oy_sayisi = from_string_to_int(oy_sayisi_string)
                print(f"İndex Değeri : {oy_sayisi_td_index}\nOy Sayisi : {int_oy_sayisi}")
                print(f"Şehir ID değeri : {şehir_ID_degeri}")
                print(f"Parti ID değeri : {parti_ID_degeri}")
                print(f"------------------------------")
                Parti_Sonuclari_ID_degeri = await Parti_Sonuclarina_Yeni_Deger_Ekleme(Secim_ID=Secim_ID,Parti_ID=parti_ID_degeri,Cografya_Kutuphanesi_ID=şehir_ID_degeri,Parti_Oy_Sayisi=int_oy_sayisi)
                kayit_edilen_Parti_Sonuclarinin_ID_degerleri.append(Parti_Sonuclari_ID_degeri)
                print(f"kayit_edilen_Parti_Sonuclarinin_ID_degerlerine yeni bir değer atanmıştır : {Parti_Sonuclari_ID_degeri}")



        else: # Tek Haneli indekslerde, oy oranlari yer almaktadır
            oy_oranlarini_barındıran_tdler = tablodaki_tr.find_elements(By.TAG_NAME,"td")
            print(f"kayit_edilen_Parti_Sonuclarinin_ID_degerleri şuanki durumu : {kayit_edilen_Parti_Sonuclarinin_ID_degerleri}")
            for oy_orani_td_index,oy_orani_td in enumerate(oy_oranlarini_barındıran_tdler):
                oy_orani_string = oy_orani_td.text.strip()
                float_oy_orani = from_string_to_float(oy_orani_string)
                print(f"İndex Değeri : {oy_orani_td_index} Oy Orani : {float_oy_orani}")

                if oy_orani_td_index == 0:
                    print(f"Burada bizim için gerekli bir değer olmadığı için atlanıyor : {oy_orani_string}")
                    continue

                try:
                    Parti_Sonuclarinin_ID_degeri = kayit_edilen_Parti_Sonuclarinin_ID_degerleri[oy_orani_td_index - 1]
                    print(f"Parti Sonuclari ID değeri alındı : {Parti_Sonuclarinin_ID_degeri}\nŞimdi güncelleme işlemine geçiliyor")
                    await Parti_Sonuclarinin_Oy_Oranini_Guncelleme(Parti_Sonuclari_ID_degeri=Parti_Sonuclarinin_ID_degeri,Oy_orani=float_oy_orani)
                except Exception as hata:
                    print(f"Parti_Sonuclarinin_ID_degeri alınırken bir hata oluştu : {hata}")

                print(f"------------------------------")

            kayit_edilen_Parti_Sonuclarinin_ID_degerleri.clear()
            print(f"Kayit edilen Parti Sonuçlarının ID değerleri temizlendi : {kayit_edilen_Parti_Sonuclarinin_ID_degerleri}")
        

                

            

    
    # Tablodaki 0 ve 1 sütunlar 


        
    
        


        
