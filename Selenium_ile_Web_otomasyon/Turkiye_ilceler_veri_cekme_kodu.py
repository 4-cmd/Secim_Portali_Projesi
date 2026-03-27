from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_yardımcı_fonksiyonlar import (css_birden_fazla_nitelik_secici,
                                            click_and_wait_for_text,
                                            wait_for_page_load,
                                            element_bekleme_ve_elementi_click_etme,
                                            Css_nitelik_secici,
                                            js_click_guclu,
                                            genel_element_bekleme,
                                            temiz_trleri_alma_kodu)
from selenium.webdriver.common.by import By
from sql_alchemy_islemleri import (Sehir_bulma_islemi,
                                   Yeni_Bir_Parti_Ekle,
                                   Cografya_Kutuphanesine_Ilce_Ekleme,
                                   Secim_Genel_Bilgiler_yeni_deger_yukleme,
                                   Parti_Sonuclarina_Yeni_Deger_Ekleme,
                                   Parti_Sonuclarinin_Oy_Oranini_Guncelleme
                                    )

from selenium.webdriver.remote.webelement import WebElement
from Donusum_modulu import from_string_to_float,from_string_to_int
import time


async def tablo_basliklarindan_partileri_alma(tablo_th_degerleri : list[WebElement]):
    """
    * tablo_th_degerleri adında parametre alır 
    * Burada parti isimleri yer alır ve parti ismi veritabanına ekler veya daha önce kayıt edilmişse, ID değerini alır
    * Sonra çektiği her ID değerini bir listeye atar
    """

    Partilerin_ID_degerleri : list[int] = []

    for index,th in enumerate(tablo_th_degerleri):
        
        if index >= 6: # Parti isimleri 6.indeksten başlıyor bu yüzden buradan başlıyoruz
            parti_adi = th.get_attribute("textContent").strip()
            
            if not parti_adi:
                parti_adi = th.get_attribute("innerText").strip()
            
            print(f"Bulunan Parti Adı: {parti_adi}")
            Partinin_ID_Degeri = await Yeni_Bir_Parti_Ekle(parti_ismi=parti_adi)
            Partilerin_ID_degerleri.append(Partinin_ID_Degeri)

            
                    
        
    print(f"Partilerin_ID_degerleri listesini şimdi döndürülecek ve içeriği : {Partilerin_ID_degerleri}")    
    return Partilerin_ID_degerleri

def tbody_nin_içindeki_bos_trleri_ayıkla(tbody_nin_tr_degerleri : list[WebElement]):
    """
    * Tbodynin içindeki tr değerlerini alır ve eğer içeriği boş ise onu döndürülecek listeye eklemez
    """

    temiz_tr_listesi: list[WebElement] = []

    for tr in tbody_nin_tr_degerleri:
        # Sadece metne bakmak yerine, elemanın görünürlüğünü ve HTML içeriğini kontrol edelim
        # get_attribute('innerHTML') boşlukları da içerir, o yüzden strip() şart.
        icerik = tr.get_attribute('innerHTML').strip()
        
        # Eğer satırın içi tamamen boş değilse listeye ekle
        if icerik and len(tr.text.strip()) > 0:
            temiz_tr_listesi.append(tr)

    print(f"Trlerin içerisindeki boş değerler ortadan kaldırıldı ve temiz tr listesi : {temiz_tr_listesi}")
        
    return temiz_tr_listesi

        
async def tablodaki_oy_sayilari_alma_ve_kaydetme(oy_sayilarini_barindiran_td_listesi : list[WebElement],
                             parti_ID_leri_listesi : list[int],
                             Cofrafya_Kutuphane_Sehir_ID : int,
                             Secim_ID : int):
    """
    * Sayfadaki tablonun oy sayilarini almak için yaratıldı 
    * İlçe ismi - Secim Genel Verileri ve Parti Sonuclarina yeni değerler ekler 
    * Parti Sonuclarina eklenen her değerin ID değerini alır ve kaydedilen_parti_Sonuclarinin_ID_değerleri atar 
    * En son olarak bu kaydedilen_parti_Sonuclarinin_ID_değerleri listeyi daha sonra güncellemek için döndürülecek
    """
    
    kaydedilen_parti_Sonuclarinin_ID_değerleri : list[int] = []
    
    parti_ID_leri_listesi_local = parti_ID_leri_listesi

    cografya_kutuphanesi_ilce_id_degeri = None

    for index, td in enumerate(oy_sayilarini_barindiran_td_listesi):
        # 1. Veriyi çek (Görünmez veriler için textContent en iyisidir)
        oy_sayisi_str = td.get_attribute("textContent").strip()
        try:

            # Eğer textContent boşsa innerText dene
            if not oy_sayisi_str:
                oy_sayisi_str = td.get_attribute("innerText").strip()

            # --- KONTROLLER BAŞLIYOR (if not bloğunun dışında olmalı) ---

            if index == 1: # İlçe ismi
                ilçe_ismi = oy_sayisi_str
                print(f"İlçe ismi : {ilçe_ismi}")
                ilçe_id = await Cografya_Kutuphanesine_Ilce_Ekleme(tanım_ekleme=ilçe_ismi,UST_ID_sehir_ID_değeri=Cofrafya_Kutuphane_Sehir_ID)
                cografya_kutuphanesi_ilce_id_degeri = ilçe_id
                print(f"Cografya kutuphanesi ilçe id değeri güncellendi : {cografya_kutuphanesi_ilce_id_degeri}")
                continue
            
            # Sadece 5. indekse geldiğimizde genel bilgileri bir kez yazdıralım
            if index == 5: 
                Kayıtlı_Seçmen_Sayisi_str = oy_sayilarini_barindiran_td_listesi[3].get_attribute("textContent").strip()
                Oy_Kullanan_Seçmen_sayisi_str = oy_sayilarini_barindiran_td_listesi[4].get_attribute("textContent").strip()
                Geçerli_Oy_Toplami_str = oy_sayilarini_barindiran_td_listesi[5].get_attribute("textContent").strip()

                Kayıtlı_Seçmen_Sayisi_int = from_string_to_int(Kayıtlı_Seçmen_Sayisi_str)
                Oy_Kullanan_Seçmen_sayisi_int = from_string_to_int(Oy_Kullanan_Seçmen_sayisi_str)
                Geçerli_Oy_Toplami_int = from_string_to_int(Geçerli_Oy_Toplami_str)

                print(f"---------------------------------------")
                print(f"Kayıtlı Seçmen: {Kayıtlı_Seçmen_Sayisi_int}\nKullanan: {Oy_Kullanan_Seçmen_sayisi_int}\nGeçerli: {Geçerli_Oy_Toplami_int}")
                print(f"---------------------------------------")
                
                _ = await Secim_Genel_Bilgiler_yeni_deger_yukleme(Cografya_Kutuphanesi_ID=cografya_kutuphanesi_ilce_id_degeri,
                                                            Gecerli_Oy_Sayisi=Geçerli_Oy_Toplami_int,
                                                            Kayitli_Secmen_Sayisi=Kayıtlı_Seçmen_Sayisi_int,
                                                            Oy_Kullanan_Secmen_Sayisi=Oy_Kullanan_Seçmen_sayisi_int,
                                                            Secim_ID=Secim_ID)
                
                continue

            if index >= 6: # Partilerin aldığı oy sayıları
                yazi_icerigi = f"Indeks : {index} | Oy Sayisi : {oy_sayisi_str}"
                oy_sayisi_integer = from_string_to_int(string_sayi=oy_sayisi_str)

                parti_ID_değeri = parti_ID_leri_listesi_local[index - 6]
                Kaydedilen_Parti_Sonuclari_ID_Degeri = await Parti_Sonuclarina_Yeni_Deger_Ekleme(
                    Cografya_Kutuphanesi_ID=cografya_kutuphanesi_ilce_id_degeri,
                    Parti_ID=parti_ID_değeri,
                    Parti_Oy_Sayisi=oy_sayisi_integer,
                    Secim_ID=Secim_ID
                )

                print(f"Kaydedilen parti sonuclarina yeni bir değer eklendi : {Kaydedilen_Parti_Sonuclari_ID_Degeri}")
                kaydedilen_parti_Sonuclarinin_ID_değerleri.append(Kaydedilen_Parti_Sonuclari_ID_Degeri)
        
        except Exception as Hata:
            print(f"tablodaki_oy_sayilari_alma_ve_kaydetme kısmında hata : {Hata}")

    
    print(f"parti_ID_leri_listesi_local şimdi döndürülüyor ve mevcut değeri : {parti_ID_leri_listesi_local}")
    return kaydedilen_parti_Sonuclarinin_ID_değerleri



    
async def tablodaki_oy_oranlarini_alma_ve_guncelleme(oy_oranlarini_td_listesi : list[WebElement],
                                                     kayit_edilen_parti_sonuclarinin_ID_degerleri_listesi : list[int]):
    for index,td in enumerate(oy_oranlarini_td_listesi):
        
        oy_orani_str_degeri = td.get_attribute("textContent").strip()
        if not oy_orani_str_degeri:
            oy_orani_str_degeri = td.get_attribute("innerText").strip()
            
        oy_orani_float = from_string_to_float(string_sayi=oy_orani_str_degeri)
        print(f"----------------------------------------------------------------------------")
        yazi_icerigi = f"İndex Değeri : {index}\nOy Orani str değeri : {oy_orani_str_degeri}"
        print(yazi_icerigi)

        if index >= 2: # 2.indeksten başlıyoruz çünkü diğer iki indekste oy oranlari yer almıyor
            try:
                parti_sonuclari_indeks = index - 2
                parti_sonuclari_id_degeri = kayit_edilen_parti_sonuclarinin_ID_degerleri_listesi[parti_sonuclari_indeks]

                _ = await Parti_Sonuclarinin_Oy_Oranini_Guncelleme(Oy_orani=oy_orani_float,
                                                                   Parti_Sonuclari_ID_degeri=parti_sonuclari_id_degeri)

            except Exception as Hata:
                print(f"tablodaki_oy_oranlarini_alma_ve_guncelleme kısmında hata : {Hata}")

async def ilceleri_bulma_ve_ilce_degerlerini_alma_async_function(driver : WebDriver,Secim_ID_Degeri : int,path_il_id_str_plaka : str):
    """
    * SEÇİM SONUÇ VERİLERİ Belediye Başkanlığı Seçim Sonuçları linkine tıklandıktan sora çalışacak
    * Daha düzenli bir kod yapisi için bu fonksiyon yaratıldı
    """
    wait_for_page_load(driver=driver)
    


    path_ilce_nitelik_secici = f"path[il_id='{path_il_id_str_plaka}']"  

    path_click_edilecek_web_elementi = Css_nitelik_secici(driver=driver,nitelik_secici=path_ilce_nitelik_secici)

    path_il_id_string_plaka = path_click_edilecek_web_elementi.get_attribute("il_id")

    

    Sehir_ID = await Sehir_bulma_islemi(path_str_plakasi=path_il_id_string_plaka)

    if Sehir_ID:
        click_islemi_basarili_mi = js_click_guclu(element=path_click_edilecek_web_elementi,driver=driver)

        if click_islemi_basarili_mi:
            print(f"ilçe click işlemi yapılmıştır")

            # Şimdi tablo başlıkları alınacak 
            thead = genel_element_bekleme(by=By.TAG_NAME,selector="thead",driver=driver)
            if thead:
                print(f"thead bulundu")

                # tr degeri bir tane olduğu için find element kullan 
                thead_tr_degeri = thead.find_element(By.TAG_NAME,"tr")

                tablonun_th_degerleri = thead_tr_degeri.find_elements(By.TAG_NAME,"th")

                print(f"tablo_basliklarindan_partileri_alma'den önce uzunluk : {len(tablonun_th_degerleri)}")

                
                Parti_ID_listesi : list[int] = await tablo_basliklarindan_partileri_alma(tablo_th_degerleri=tablonun_th_degerleri)

                print(f"Parti IDlerin uzunluğu : {len(Parti_ID_listesi)}")
                

                wait_for_page_load(driver=driver)
                print(f"wait for page load tbody seçilmeden önce yüklendi")


                # Şimdi tablonun içindeki değerler alınacak 
                tbody = driver.find_element(By.TAG_NAME,"tbody")

                tbody_nin_trleri = tbody.find_elements(By.TAG_NAME,"tr")

                print(f"kaç tane tr değeri var : {len(tbody_nin_trleri)}")

                temiz_tr_listesi = temiz_trleri_alma_kodu(driver=driver,düzensiz_trler=tbody_nin_trleri)

                kayit_edilen_parti_sonuclarinin_ID_degerleri_listesi = []

                
                for index,tr in enumerate(temiz_tr_listesi):
                    # `td_listesi = tr.find_elements(By.TAG_NAME, "td")` is finding all the `<td>`
                    # elements within a specific `<tr>` element.
                    
                    print(f"TR'nin indeks değeri : {index}")

                    if index %2 == 0: # Burada oy sayilari yer almaktadır 
                        oy_sayilari_td_listesi = tr.find_elements(By.TAG_NAME,"td")

                        kayit_edilen_parti_sonuclarinin_ID_degerleri_listesi = await tablodaki_oy_sayilari_alma_ve_kaydetme(parti_ID_leri_listesi=Parti_ID_listesi,
                                                                    oy_sayilarini_barindiran_td_listesi=oy_sayilari_td_listesi,
                                                                    Cofrafya_Kutuphane_Sehir_ID=Sehir_ID,
                                                                    Secim_ID=Secim_ID_Degeri)
                        
                    else:
                        oy_oranlari_td_listesi = tr.find_elements(By.TAG_NAME,"td")
                        await tablodaki_oy_oranlarini_alma_ve_guncelleme(kayit_edilen_parti_sonuclarinin_ID_degerleri_listesi=kayit_edilen_parti_sonuclarinin_ID_degerleri_listesi,
                                                                        oy_oranlarini_td_listesi=oy_oranlari_td_listesi)
                        
                        kayit_edilen_parti_sonuclarinin_ID_degerleri_listesi.clear()
                        print(f"kayit_edilen_parti_sonuclarinin_ID_degerleri_listesi temizleniyor")

                

                time.sleep(5)

            else:
                print(f"thead bulunamadi")
                
            
    
        else:
            print(f"İlçe click işlemi yapilamadi")


    else:
        print(f"Sehir ismi olmadığı için işleme devam edilmeyecektir ilceleri_bulma_ve_ilce_degerlerini_alma.py")

    
    


    
    
        





    