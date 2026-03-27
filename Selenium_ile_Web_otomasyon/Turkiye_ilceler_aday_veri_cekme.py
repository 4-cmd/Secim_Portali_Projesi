from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from Donusum_modulu import from_string_to_float,from_string_to_int
from selenium_yardımcı_fonksiyonlar import (css_birden_fazla_nitelik_secici,
                                            click_and_wait_for_text,
                                            wait_for_page_load,
                                            Css_nitelik_secici,
                                            js_click_guclu,
                                            genel_element_bekleme,
                                            Stale_element_onune_gec)

from sql_alchemy_islemleri import (
    Sehir_bulma_islemi,
    Yeni_Bir_Aday_Kaydetme,
    Aday_Sonuclar_Tablosu_na_deger_kaydetme,
    Cografya_Kutuphanesine_Ilce_Ekleme,
    Secim_Genel_Bilgiler_yeni_deger_yukleme,
    Aday_Sonuclar_Tablosundaki_Oy_Oranini_Guncelleme
    )



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

    print(f"Trlerin içerisindeki boş değerler ortadan kaldırıldı ve temiz tr listesi uzunluğu : {len(temiz_tr_listesi)}")
        
    return temiz_tr_listesi


async def secim_genel_bilgiler_e_deger_kaydetme(kayitli_secmen : str,
                                                oy_kullanan_secmen : str,
                                                gecerli_oy_toplami : str,
                                                seçim_ID : int,
                                                Cografya_kutuphanesi_ID : int):
    
    """
    * tablo_oy_sayilari_isleme fonksiyonundan değerler gelecektir ve değerler Secim-genel-bilgilere kaydedilecek
    * Amaç daha düzenli bir kod mimarisi sağlamak
    """

    kayitli_secmen_int = from_string_to_int(kayitli_secmen)
    oy_kullanan_secmen_int = from_string_to_int(oy_kullanan_secmen)
    gecerli_oy_toplami_int = from_string_to_int(gecerli_oy_toplami)

    _ = await Secim_Genel_Bilgiler_yeni_deger_yukleme(Cografya_Kutuphanesi_ID=Cografya_kutuphanesi_ID,
                                                Gecerli_Oy_Sayisi=gecerli_oy_toplami_int,
                                                Kayitli_Secmen_Sayisi=kayitli_secmen_int,
                                                Oy_Kullanan_Secmen_Sayisi=oy_kullanan_secmen_int,
                                                Secim_ID=seçim_ID)


async def tablodaki_oy_sayilari_alma_ve_kaydetme(oy_sayilarini_barindiran_td_listesi : list[WebElement],
                             adayların_id_değerlerinin_listesi : list[int],
                             Cofrafya_Kutuphane_Sehir_ID : int,
                             Secim_ID : int):
    """
    * Sayfadaki tablonun oy sayilarini almak için yaratıldı 
    * İlçe ismi - Secim Genel Verileri ve Aday sonuclarina yeni değerler ekler 
    * Aday sonuclarina eklenen her değerin ID değerini alır ve kaydedilen_aday_sonuclarinin_ID_listesi atar 
    * En son olarak bu kaydedilen_aday_sonuclarinin_ID_listesi listeyi daha sonra güncellemek için döndürülecek
    """
    
    kaydedilen_aday_sonuclarinin_ID_listesi : list[int] = []
    
    adayların_id_değerlerinin_listesi = adayların_id_değerlerinin_listesi

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

                Aday_ID_değeri = adayların_id_değerlerinin_listesi[index - 6]
                Kaydedilen_aday_Sonuclari_ID_Degeri = await Aday_Sonuclar_Tablosu_na_deger_kaydetme(
                                                            Aday_ID=Aday_ID_değeri,
                                                            Aday_Oy_Sayisi=oy_sayisi_integer,
                                                            Cografya_Kutuphanesi_ID_=cografya_kutuphanesi_ilce_id_degeri,
                                                            Secim_ID=Secim_ID)
                
                    

                print(f"Kaydedilen aday sonuclarina yeni bir değer eklendi : {Kaydedilen_aday_Sonuclari_ID_Degeri}")
                kaydedilen_aday_sonuclarinin_ID_listesi.append(Kaydedilen_aday_Sonuclari_ID_Degeri)
        
        except Exception as Hata:
            print(f"tablodaki_oy_sayilari_alma_ve_kaydetme kısmında hata : {Hata}")

    
    print(f"kaydedilen_aday_sonuclarinin_ID_listesi şimdi döndürülüyor ve mevcut değeri : {kaydedilen_aday_sonuclarinin_ID_listesi}")
    return kaydedilen_aday_sonuclarinin_ID_listesi



async def tablo_basliklarindan_adaylari_alma(tablo_th_degerleri : list[WebElement]):
    """
    * tablo_th_degerleri adında parametre alır 
    * Burada aday isimleri yer alır ve aday ismi veritabanına ekler veya daha önce kayıt edilmişse, ID değerini alır
    * Sonra çektiği her ID değerini bir listeye atar
    """

    Adayların_Id_Değerini_Tutan_Liste : list[int] = []

    for index,th in enumerate(tablo_th_degerleri):
        
        if index >= 6: # Parti isimleri 6.indeksten başlıyor bu yüzden buradan başlıyoruz
            Aday_adi = th.get_attribute("textContent").strip()
            
            if not Aday_adi:
                Aday_adi = th.get_attribute("innerText").strip()
            
            print(f"Bulunan Aday Adı: {Aday_adi}")
            Aday_ID_değeri = await Yeni_Bir_Aday_Kaydetme(aday_ismi=Aday_adi)
            Adayların_Id_Değerini_Tutan_Liste.append(Aday_ID_değeri)

            
                    
        
    print(f"Adayların_Id_Değerini_Tutan_Liste listesini şimdi döndürülecek ve içeriği : {Adayların_Id_Değerini_Tutan_Liste}")    
    return Adayların_Id_Değerini_Tutan_Liste


async def path_ile_tıklama_ve_sehir_ID_degerini_alma(path_str_plaka: str, driver: WebDriver):
    """
    * Path str plakasi ile belirlenen ilçeye tıklar başarılı ise True başarısız ise False döner 
    * bir liste döndürür ilk değer şehir id verir diğer değer ise tıklama işlemi başarılı mı değil mi olduğunu koyar (True ya da False)
    """
    # 1. Listeyi en başta tanımla (Hata almamak için)
    dondurlecek_liste: list = [None, False] 

    print(f"path_str_plaka değeri : {path_str_plaka}")

    path_ilce_nitelik_secici = f"path[il_id='{path_str_plaka}']"  
    path_click_element = Css_nitelik_secici(driver=driver, nitelik_secici=path_ilce_nitelik_secici)
    
    if not path_click_element:
        print(f"Hata: {path_str_plaka} plakalı element bulunamadı.")
        return dondurlecek_liste

    try:
        # ID değerini al
        path_il_id = path_click_element.get_attribute("il_id")
        sehir_id = await Sehir_bulma_islemi(path_str_plakasi=path_il_id)

        if sehir_id:

            taze_element = Stale_element_onune_gec(by=By.CSS_SELECTOR,selector=path_ilce_nitelik_secici,driver=driver,max_retries=10)

            if taze_element:
                print(f"Staleelement hatasının önüne geçmek için path ile tıklanacak değer tekrar bulundu")
                click_basarili = js_click_guclu(element=taze_element, driver=driver)
                
                # Değerleri güncelle
                dondurlecek_liste[0] = sehir_id
                dondurlecek_liste[1] = True if click_basarili else False
            
            else:
                print(f"Stale_element_onune_gec fonksiyonu stale element hatasını gideremedi")
                dondurlecek_liste[0] = sehir_id
                dondurlecek_liste[1] = False
                
    except Exception as e:
        print(f"İşlem sırasında beklenmedik hata: {e}")

    print(f"Fonksiyon tamamlandı. Sonuç: {dondurlecek_liste}")
    return dondurlecek_liste


async def tablodaki_oy_oranlarini_alma_ve_guncelleme(oy_oranlarini_td_listesi : list[WebElement],
                                                     kayit_edilen_aday_sonuclarinin_ID_değerleri_listesi : list[int]):
    """
    * Aday_Sonuclar_Tablosu Aday_Oy_Orani güncellemek için yaratıldı

    Args:
        oy_oranlarini_td_listesi (list[WebElement]): Oy oranlarinin web elemetli listesi 
        kayit_edilen_aday_sonuclarinin_ID_de (_type_): bunlar sonra güncellenecek
    """
    
    
    for index,td in enumerate(oy_oranlarini_td_listesi):
        if index >= 2: # 2.indeksten başlıyoruz çünkü diğer iki indekste oy oranlari yer almamaktadır
            try:
                oy_orani_str_degeri = td.get_attribute("textContent").strip()

                oy_orani_float = from_string_to_float(string_sayi=oy_orani_str_degeri)

                print(f"----------------------------------------------------------------------------")

                yazi_icerigi = f"İndex Değeri : {index}\nOy Orani str değeri : {oy_orani_str_degeri}"

                print(yazi_icerigi)

                print(f"----------------------------------------------------------------------------")


                aday_sonuclari_index = index - 2
                aday_sonuclarinin_id_değeri = kayit_edilen_aday_sonuclarinin_ID_değerleri_listesi[aday_sonuclari_index]

                _ = await Aday_Sonuclar_Tablosundaki_Oy_Oranini_Guncelleme(Aday_oy_orani=oy_orani_float,
                                                                           Aday_Sonucu_ID_değeri=aday_sonuclarinin_id_değeri)

            except Exception as Hata:
                print(f"tablodaki_oy_oranlarini_alma_ve_guncelleme kısmında hata : {Hata}")


async def Main_Aday_İlce_Sonuclari(seçim_ID : int,
                                   driver : WebDriver,
                                   path_str_degeri : str):
    
    wait_for_page_load(driver=driver)

    path_tiklama_sonucu_donen_liste : list  = await path_ile_tıklama_ve_sehir_ID_degerini_alma(driver=driver,path_str_plaka=path_str_degeri)

    sehir_id_degeri : int = path_tiklama_sonucu_donen_liste[0]

    tiklama_islemi_basarili_mi : bool = path_tiklama_sonucu_donen_liste[1]

    if tiklama_islemi_basarili_mi:
        print(f"path plaka tiklama işlemi başarılıdır")

        
        thead_str_value : str = "thead"
        
        thead_tag_name = genel_element_bekleme(by=By.TAG_NAME,selector=thead_str_value,driver=driver)

        tablo_basliklari : list[WebElement] = thead_tag_name.find_elements(By.TAG_NAME,"th")

        aday_Id_değerlerinin_listesi : list[int] = await tablo_basliklarindan_adaylari_alma(tablo_th_degerleri=tablo_basliklari)

        tbody_elementini_bekle = driver.find_element(By.TAG_NAME,"tbody")

        düzensiz_trlerin_listesi = tbody_elementini_bekle.find_elements(By.TAG_NAME,"tr")

        düzenli_trlerin_listesi = tbody_nin_içindeki_bos_trleri_ayıkla(tbody_nin_tr_degerleri=düzensiz_trlerin_listesi)

        aday_sonuclarinin_ID_değerlerinin_listesi : list[int] = []

        for index,tr in enumerate(düzenli_trlerin_listesi):
            print(f"TR'nin indeks değeri : {index}")

            if index % 2 == 0: # Aday oy sayilari, Secim Genel Bilgileri ve Cografya ID (ilçe alınacaktır)
                oy_sayilari_td_listesi = tr.find_elements(By.TAG_NAME,"td")
                aday_sonuclari_id_listesi = await tablodaki_oy_sayilari_alma_ve_kaydetme(adayların_id_değerlerinin_listesi=aday_Id_değerlerinin_listesi,
                                                       Cofrafya_Kutuphane_Sehir_ID=sehir_id_degeri,
                                                       Secim_ID=seçim_ID,
                                                       oy_sayilarini_barindiran_td_listesi=oy_sayilari_td_listesi)
                

                aday_sonuclarinin_ID_değerlerinin_listesi = aday_sonuclari_id_listesi
                print(f"aday_sonuclarinin_ID_değerlerinin_listesi güncellenmiştir : {aday_sonuclarinin_ID_değerlerinin_listesi}")
            
            else: # Burada oy oranlari yer almaktadir 
                try:
                    oy_oranlari : list[WebElement] = tr.find_elements(By.TAG_NAME,"td")
                    _ = await tablodaki_oy_oranlarini_alma_ve_guncelleme(oy_oranlarini_td_listesi=oy_oranlari,
                                                               kayit_edilen_aday_sonuclarinin_ID_değerleri_listesi=aday_sonuclarinin_ID_değerlerinin_listesi)
                    
                    print(f"aday_sonuclarinin_ID_değerlerinin_listesi listesi şimdi temizleniyor")
                    aday_sonuclarinin_ID_değerlerinin_listesi.clear()


                except Exception as Hata:
                    print(f"Oy oranlarini güncelleme işlemi sırasında Main_Aday_İlce_Sonuclari fonksiyonunda hata meydana geldi : {Hata}")


    
    else:
        print(f"path plaka tiklama işlemi başarısız ")
    

