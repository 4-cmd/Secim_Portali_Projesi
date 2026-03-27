from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_yardımcı_fonksiyonlar import (wait_for_page_load,
                                            genel_element_bekleme,
                                            js_click_guclu,
                                            Stale_element_onune_gec,
                                            Css_nitelik_secici,
                                            css_birden_fazla_nitelik_secici,
                                            )
from selenium.webdriver.common.by import By
from sql_alchemy_islemleri import Sehir_bulma_islemi,Parti_Sonuclarinin_Oy_Oranini_Guncelleme
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Turkiye_ilceler_veri_cekme_kodu import (ilceleri_bulma_ve_ilce_degerlerini_alma_async_function,
                                            tablodaki_oy_sayilari_alma_ve_kaydetme,
                                            tablo_basliklarindan_partileri_alma,
                                            tablodaki_oy_oranlarini_alma_ve_guncelleme)

from Turkiye_ilceler_veri_cekme_kodu import temiz_trleri_alma_kodu
import time 



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

def container_acan_kod(driver : WebDriver):
    """
    * ilk olarak, ismi ngx-overlay  gelene kadar bekle 

    * Geldikten sonra 
    
    * Name değeri : secimCevresi olan elemeti gelene kadar bekle 
    
    * geldikten sonra bu elemente tikla (ardından div option = 'role' sahip olan elemetler açılacak)

    * onlar burada seçmeyeceğiz (ana işlemde olacak)
    

    """

    # Overlay kaybolana kadar bekle
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "ngx-overlay"))
    )
    
    
    wait_for_page_load(driver=driver)


    ng_select_secim_cevresi = genel_element_bekleme(by=By.NAME,selector="secimCevresi",driver=driver)

    if ng_select_secim_cevresi:
        print(f"tiklanacak web container elementi bulundu ")

        _ = ng_select_secim_cevresi.click()
        print(f"ng_select_secim_cevresi.tag_name : değeri : {ng_select_secim_cevresi.tag_name}")
    
    else:
        print(f"tiklanacak web container elementi bulunamadi")
    


async def tablo_islemleri(driver : WebDriver,Sehir_ID : int,Secim_ID_Degeri : int):
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

    
    



# CLASS = ng-select-container ng-has-value TEK BİR TANE VAR 
async def main_ozel_iller(driver : WebDriver,secim_ID : int,path_str_plaka : str):
    """
    * Ankara, İstanbul, Bursa ve İzmir gibi değerler için özel olarak yaratıldı
    """
    tiklanacak_indeks_degeri = 0
    wait_for_page_load(driver=driver)

    sehir_id_ve_tiklama_durumu : list = await path_ile_tıklama_ve_sehir_ID_degerini_alma(driver=driver,path_str_plaka=path_str_plaka)

    şehir_id_degeri : int = sehir_id_ve_tiklama_durumu[0]
    tiklanma_durumu : bool = sehir_id_ve_tiklama_durumu[1]

    if tiklanma_durumu:
        print(f"path string elemetine tıklama başarılı bir şekilde yapıldı")
        
        container_acan_kod(driver=driver)

        wait_for_page_load(driver=driver)

        css_role_option_nitelik_secici = "div[role='option']"

        div_role_options = css_birden_fazla_nitelik_secici(nitelik_secici=css_role_option_nitelik_secici,driver=driver)

        for option in div_role_options:

            tag_name_of_option = option.tag_name
            print(f"Option tag name : {tag_name_of_option}")

            _ = js_click_guclu(driver=driver,element=option)

            _ = await tablo_islemleri(driver=driver,Secim_ID_Degeri=secim_ID,Sehir_ID=şehir_id_degeri)

            _ = container_acan_kod(driver=driver) # Diğer linklere tıklamak için container yeniden açılmalı İzmir - 1 tıkladın İzmir - 2 tıklamak için açık olmalı 

            wait_for_page_load(driver=driver) # Sayfa yüklenene kadar bekle


        coklu_sinif = "div[class='sinif1 sinif2 sinif3 sinif4']"
        css_nitelik_secicim = '.sinif1.sinif2.sinif3.sinif4'

        nitelik_secici = driver.find_element(By.CSS_SELECTOR,css_nitelik_secicim)
        

    
    else:
        print(f"path string elemetine tıklama başarısız oldu ")
    



