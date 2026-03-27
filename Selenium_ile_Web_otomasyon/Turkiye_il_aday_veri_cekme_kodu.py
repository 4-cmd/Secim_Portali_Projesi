from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_yardımcı_fonksiyonlar import wait_for_page_load,genel_element_bekleme
from selenium.webdriver.common.by import By
from sql_alchemy_islemleri import (Yeni_Bir_Aday_Kaydetme,
                                   Cografya_Kutuphanesine_Yeni_Bir_Deger_Ekleme,
                                   Secim_Genel_Bilgiler_yeni_deger_yukleme,
                                   Aday_Sonuclar_Tablosu_na_deger_kaydetme,
                                   Aday_Sonuclar_Tablosundaki_Oy_Oranini_Guncelleme)

from Donusum_modulu import from_string_to_float,from_string_to_int
from selenium.webdriver.remote.webelement import WebElement




async def tablo_basliklarini_isleme_kodu(driver : WebDriver):
    """
    * Bu fonksiyon, tablo basliklariyla ilgilenecek 
    * 5.indeksten itibaren ise aday isimlerini alacak
    * Aday ismi kaydedilecek ve ID değeri dönecek (Eğer Aday zaten var ise işlem yapılmayacak)
    * adayların id değerleri Adayların_ID_değerlerini_tutan_liste atanacak 
    """

    Adayların_ID_değerlerini_tutan_liste : list[int] = []

    wait_for_page_load(driver=driver)
    tag_name = "thead"

    tablo_thead_bekleme = genel_element_bekleme(by=By.TAG_NAME,selector=tag_name,driver=driver)

    if tablo_thead_bekleme:
        print(f"thead gelmiştir ve th değerleri alınacak")
        th_str = "th"

        th_lists : list[WebElement] = tablo_thead_bekleme.find_elements(by=By.TAG_NAME,value=th_str)

        for index,th in enumerate(th_lists):

            if index >= 5: # İndeks değeri 5 ya da daha büyük olursa burada adaylar yer alıyor
                aday_ismi = th.get_attribute("textContent").strip()
                Aday_ID_degeri = await Yeni_Bir_Aday_Kaydetme(aday_ismi=aday_ismi)

                Adayların_ID_değerlerini_tutan_liste.append(Aday_ID_degeri)
        
    
    print(f"tablo_basliklarini_isleme_kodunda Adayların_ID_değerlerini_tutan_liste değerler eklendi ve son hali : {Adayların_ID_değerlerini_tutan_liste}")
    return Adayların_ID_değerlerini_tutan_liste




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


async def Aday_Sonuclar_tablosuna_yeni_deger_ekleme(seçim_ID : int,
                                                    Aday_ID : int,
                                                    Cografya_Kutup_ID : int,
                                                    Aday_Oy_Sayisi : str):
    """
    * Bu fonksiyon aday sonuclar tablosuna yeni değer ekler Değerin ID değerini döndürür 
    * (zaten ekliyse var olan ID değerini döder)
    * Düzenli bir kod mimarisi için oluşturulmuştur 
    """

    int_aday_oy_sayisi = from_string_to_int(Aday_Oy_Sayisi)
    ID_değeri = await Aday_Sonuclar_Tablosu_na_deger_kaydetme(Secim_ID=seçim_ID,
                                                              Aday_ID=Aday_ID,
                                                              Cografya_Kutuphanesi_ID_=Cografya_Kutup_ID,
                                                              Aday_Oy_Sayisi=int_aday_oy_sayisi)
    
    return ID_değeri



    
async def tablo_oy_sayilari_isleme(seçim_ID : int,Aday_Id_degerleri_listesi : list[int],oy_sayilari_listesi : list[WebElement]):
    """
    * Oy sayilarinin yer aldığı tabloda şehir ismi, kayitli seçmen sayisi oy kullanan seçmen sayisi ve geçerli oy toplamini kaydeder
    * Buna ek olarak adayların aldığı oy sayilarini da kaydeder
    * Oy sayilarini kaydeder ve ID değerlerini alır 
    * Id değerlerini daha sonra güncellemek için Aday_Sonuclari_ID_degerleri_listesi atar 
    * Son olarak Aday_Sonuclari_ID_degerleri_listesi döndürür 
    """
    Aday_Id_degerleri_listesi = Aday_Id_degerleri_listesi

    Aday_Sonuclari_ID_degerleri_listesi : list[int] = []

    cografya_kutuphanesi_id_degeri_global : int = 0

    
    şehir_ismi = oy_sayilari_listesi[1].get_attribute("textContent").strip()
    kayitli_secmen = oy_sayilari_listesi[2].get_attribute("textContent").strip()
    oy_kullanan = oy_sayilari_listesi[3].get_attribute("textContent").strip()
    gecerli_oy = oy_sayilari_listesi[4].get_attribute("textContent").strip()

    

    cografya_kutuphanesi_id_degeri_global = await Cografya_Kutuphanesine_Yeni_Bir_Deger_Ekleme(tanım_ekleme=şehir_ismi)

    print(f"cografya_kutuphanesi_id_degeri_global güncellenmiştir : {cografya_kutuphanesi_id_degeri_global} ve atlama yapılıyor")

    _ = await secim_genel_bilgiler_e_deger_kaydetme(seçim_ID=seçim_ID,
                                                    Cografya_kutuphanesi_ID=cografya_kutuphanesi_id_degeri_global,
                                                    gecerli_oy_toplami=kayitli_secmen,
                                                    oy_kullanan_secmen=oy_kullanan,
                                                    kayitli_secmen=gecerli_oy)

                
    # 4. Adayların oylarını döngü ile kaydet (index 5 ve sonrası)
    for index in range(5, len(oy_sayilari_listesi)):
            try:
                aday_id_indeks_değeri = index - 5
                adayın_id_değeri = Aday_Id_degerleri_listesi[aday_id_indeks_değeri]
                oy_sayisi = oy_sayilari_listesi[index].get_attribute("textContent").strip()

                res_id = await Aday_Sonuclar_tablosuna_yeni_deger_ekleme(
                    Aday_ID=adayın_id_değeri,
                    Aday_Oy_Sayisi=oy_sayisi,
                    Cografya_Kutup_ID=cografya_kutuphanesi_id_degeri_global,
                    seçim_ID=seçim_ID
                )
                Aday_Sonuclari_ID_degerleri_listesi.append(res_id)

            except Exception as Hata:
                print(f"Aday kaydı hatası (Index {index}): {Hata}")



    print(f"Aday_Sonuclari_ID_degerleri_listesi döndürülüyor : {Aday_Sonuclari_ID_degerleri_listesi}")
    return Aday_Sonuclari_ID_degerleri_listesi



async def tablo_oy_oranlarini_isleme(aday_sonuclarinin_ID_degerlerinin_listesi : list[int],
                                     oy_oranlari_listesi : list[WebElement]):

    """
    * Aday Sonuclarindaki oy oranini günceller ve değer döndürmez 
    * Temiz bir kod mimarisi elde etmek için oluşturuldu 

    """

    aday__sonuclarinin_ID_degerlerinin_listesi = aday_sonuclarinin_ID_degerlerinin_listesi

    for index,oy_orani in enumerate(oy_oranlari_listesi):

        if index >= 1: # Aday oy oranlari buradan başlıyor
            aday_sonuclari_ID_değeri : int = aday__sonuclarinin_ID_degerlerinin_listesi[index - 1]

            str_oy_orani : str = oy_orani.get_attribute("textContent").strip()

            float_oy_orani : float = from_string_to_float(str_oy_orani)

            _ = await Aday_Sonuclar_Tablosundaki_Oy_Oranini_Guncelleme(Aday_oy_orani=float_oy_orani,Aday_Sonucu_ID_değeri=aday_sonuclari_ID_değeri)





async def Main_Turkiye_il_veri_cekme_function(seçim_ID : int,driver: WebDriver):
    Aday_Id_degerleri_listesi = await tablo_basliklarini_isleme_kodu(driver=driver)

    Aday_Sonuclari_kaydedilen_ID_degerlerinin_listesi : list[int] = []

    tag_selector : str = "tbody"
    tbody : WebElement = genel_element_bekleme(by=By.TAG_NAME,selector=tag_selector,driver=driver)

    tr_value : str = "tr"
    tbody_nin_trleri : list[WebElement] = tbody.find_elements(by=By.TAG_NAME,value=tr_value)

    düzenlenen_tbody_degerleri : list[WebElement] = tbody_nin_trleri[2:] # İlk iki tr bizim için önemli değil 

    td_value : str = "td"

    for index,tr in enumerate(düzenlenen_tbody_degerleri):

        if index % 2 == 0: # Şehir ismi oy sayilari alınacak
            
            
            oy_sayilari_listesi : list[WebElement] = tr.find_elements(By.TAG_NAME,value=td_value)
            aday_sonuclari_id_listesi = await tablo_oy_sayilari_isleme(seçim_ID=seçim_ID,
                                     Aday_Id_degerleri_listesi=Aday_Id_degerleri_listesi,
                                     oy_sayilari_listesi=oy_sayilari_listesi)
            
            Aday_Sonuclari_kaydedilen_ID_degerlerinin_listesi = aday_sonuclari_id_listesi
            print(f"Aday_Sonuclari_kaydedilen_ID_degerlerinin_listesi güncellendi ve birazdan oy oranlarina atılacak : {Aday_Sonuclari_kaydedilen_ID_degerlerinin_listesi}")
        
        else:
            oy_oranlari_listesi : list[WebElement] = tr.find_elements(By.TAG_NAME,value=td_value)

            if Aday_Sonuclari_kaydedilen_ID_degerlerinin_listesi:
                _ = await tablo_oy_oranlarini_isleme(aday_sonuclarinin_ID_degerlerinin_listesi=Aday_Sonuclari_kaydedilen_ID_degerlerinin_listesi,
                                                    oy_oranlari_listesi=oy_oranlari_listesi)
                
                print(f"Aday_Sonuclari_kaydedilen_ID_degerlerinin_listesi temizleniyor")
                Aday_Sonuclari_kaydedilen_ID_degerlerinin_listesi.clear()

            else:
                print("Hata: Oran satırına gelindi ama işlenecek ID bulunamadı!")