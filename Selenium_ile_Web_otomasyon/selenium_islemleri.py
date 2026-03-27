from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium_yardımcı_fonksiyonlar import (
    ID_bulucu_sinif,
    birden_fazla_ID_element_bulucu,
    js_click_guclu,
    element_bekleme_ve_elementi_click_etme,
    Cumhurbaskani_Secimleri_ni_Secme,
    Cumhurbaskanligi_Secim_Sonuclarina_Tiklama,
    wait_for_page_load,
    js_click,
    element_tiklanabilir_olana_kadar_bekleme,
    Css_nitelik_secici,
    Milletvekili_Genel_Secimleri_ni_Secme,
    Milletvekili_Secim_Sonuclarina_Tiklama
)

import asyncio 
from sql_alchemy_islemleri import  Yeni_Bir_Secim_Ekleme,Illerin_plaka_kodlarini_getirme
from Turkiye_iller_veri_cekme_kodu import Turkiye_tablosu_ozel_selenium_kodu
from Turkiye_ilceler_veri_cekme_kodu import ilceleri_bulma_ve_ilce_degerlerini_alma_async_function
from Turkiye_il_aday_veri_cekme_kodu import Main_Turkiye_il_veri_cekme_function
from Turkiye_ilceler_aday_veri_cekme import Main_Aday_İlce_Sonuclari
from Milletvekili_ilceler_ozel_kod import main_ozel_iller

service = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080") # Sanal ekran boyutu

anasayfa_linki = "https://acikveri.ysk.gov.tr/anasayfa"

driver = WebDriver(
    service=service,
    options=chrome_options
)

path_il_idleri_str_plakalari : list[str] = ["35","34","6","16"]



driver.get(anasayfa_linki)

async def main():
    # For Döngüsü neden açıldı?
    # Çünkü Örneğin 2 HAZİRAN 2024 YENİLEME SEÇİMİ işleminde gereken verileri aldıktan sonra (ilçe ya da şehir)
    # Sayfanın tekrar başına geliriz ve diğer linkler üzerinden gezeceğiz

    integer_plaka_idler : list[int] = await Illerin_plaka_kodlarini_getirme()
    
    for integer_plaka_id in path_il_idleri_str_plakalari:

        path_il_id_str_plaka = str(integer_plaka_id)

        print(f"Başlık : {driver.title}")

        pop_up_element_css_seçici = "button[class='close'][id='myModalClose']"

        _ = element_tiklanabilir_olana_kadar_bekleme(by=By.CSS_SELECTOR,driver=driver,selector=pop_up_element_css_seçici)

        wait_for_page_load(driver=driver,timeout=90)

        Seçim_Seçiniz_Kutucuğu_nitelik_seçicisi = "li[data-intro='İlerlemek için lütfen Seçim seçiniz.']"

        seçim_seçiniz_li_tag_nameli_kutucuğu = Css_nitelik_secici(nitelik_secici=Seçim_Seçiniz_Kutucuğu_nitelik_seçicisi,driver=driver)

        if seçim_seçiniz_li_tag_nameli_kutucuğu:
            print(f"seçim_seçiniz_li_tag_nameli_kutucuğu bulundu ve kendisine bağlı olan a etiketi alınacak")
            seçim_seçiniz_a_tag_name_kutucuğu = seçim_seçiniz_li_tag_nameli_kutucuğu.find_element(By.TAG_NAME,"a")
            _ = js_click_guclu(element=seçim_seçiniz_a_tag_name_kutucuğu,
                           driver=driver)
        
        else:
            print(f"seçim_seçiniz_li_tag_nameli_kutucuğu bulunamadı")
            break


        


        # div id electionCard'dan 7 tane var ama ilk değeri almalısın (İlk Değer Belediye Başkanlığı Seçimleri)
        seçimler_listesi_div_id = "electionCard"
        seçimler_listesi = birden_fazla_ID_element_bulucu(element_ID_ismi=seçimler_listesi_div_id, driver=driver)


        if seçimler_listesi:
            try:
            
                Milletvekili_Seçimleri_web_element = seçimler_listesi[5] # Milletvekili_Seçimleri Seçildi bu bir divdir içinde bir tane a etiketi olacak onu al

                milletvekili_seçimleri_a_etiketi = Milletvekili_Seçimleri_web_element.find_element(By.TAG_NAME,"a")

                isim = milletvekili_seçimleri_a_etiketi.get_attribute("textContent").strip()
                
                print(f"Cumhurbaskanlığı_genel_seçimi text değeri : {isim}")

                js_click_guclu(driver=driver,element=milletvekili_seçimleri_a_etiketi)

                Secim_ID_degeri = await Milletvekili_Genel_Secimleri_ni_Secme(
                    driver=driver,
                    index_no=4,
                    Milletvekili_Secimleri_Web_Element=Milletvekili_Seçimleri_web_element
                )


                
                if Secim_ID_degeri is None:
                    print(f"Seçim ID değeri alınamadığı için atlandı")
                    continue

                        
                sonuc = Milletvekili_Secim_Sonuclarina_Tiklama(driver=driver)

                if sonuc is None:
                    continue

                else:
                    await main_ozel_iller(driver=driver,
                                          path_str_plaka=path_il_id_str_plaka,
                                          secim_ID=Secim_ID_degeri)
                    
                    
                    
                    
            except Exception as e:
                print(f"Hata: {e}")

            
            driver.back()

    # Kapatmadan önce
    driver.quit()
    print("Tarayıcı kapatıldı.")

if __name__ == "__main__":
    asyncio.run(main())


#  python selenium_islemleri.py