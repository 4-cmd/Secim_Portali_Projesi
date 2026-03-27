from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException,StaleElementReferenceException 
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time 
from sql_alchemy_islemleri import Yeni_Bir_Secim_Ekleme


def js_click(element : WebElement, driver : WebDriver):
    """JavaScript ile click yap (gizli elementler için)"""
    try:
        driver.execute_script("arguments[0].click();", element)
        print("JavaScript ile click başarılı")
        return True
    except Exception as e:
        print(f"JavaScript click failed: {e}")
        return False

def ID_bulucu_sinif(element_ID_ismi : str, driver : WebDriver):
    try:
        # Element yüklenene kadar 10 saniye bekle
        wait = WebDriverWait(driver, 10)
        ID_li_element = wait.until(EC.presence_of_element_located((By.ID, element_ID_ismi)))
        print(f"ID değerli element: {element_ID_ismi} bulundu")
        return ID_li_element
    except TimeoutException:
        print(f"Timeout: {element_ID_ismi} yüklenemedi")
        return None
    except NoSuchElementException:
        print(f"Element bulunamadi: {element_ID_ismi}")
        return None

def Css_nitelik_secici(nitelik_secici : str,driver : WebDriver):
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, nitelik_secici)))
        print(f"CSS seçici ile element bulundu: {nitelik_secici}")
        return element
    except TimeoutException:
        print(f"Timeout: {nitelik_secici} yüklenemedi")
        return None
    except NoSuchElementException:
        print(f"Element bulunamadi: {nitelik_secici}")
        return None

def birden_fazla_ID_element_bulucu(element_ID_ismi : str,driver : WebDriver):
    try:
        wait = WebDriverWait(driver, 10)
        ID_li_elementler = wait.until(EC.presence_of_all_elements_located((By.ID, element_ID_ismi)))
        print(f"ID değerli elementler: {element_ID_ismi} bulundu")
        return ID_li_elementler
    except TimeoutException:
        print(f"Timeout: {element_ID_ismi} yüklenemedi")
        return None
    except NoSuchElementException:
        print(f"Element bulunamadi: {element_ID_ismi}")
        return None

def css_birden_fazla_nitelik_secici(nitelik_secici : str,driver : WebDriver):
    try:
        wait = WebDriverWait(driver, 10)
        elementler = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, nitelik_secici)))
        print(f"CSS seçici ile elementler bulundu: {nitelik_secici}")
        return elementler
    except TimeoutException:
        print(f"Timeout: {nitelik_secici} yüklenemedi")
        return None
    except NoSuchElementException:
        print(f"Element bulunamadi: {nitelik_secici}")
        return None

def js_click_guclu(element: WebElement, driver: WebDriver):
    """Güçlü JavaScript click - click event dispatch ile"""
    try:
        textContent = element.get_attribute("textContent").strip()
        print(f"Birazdan tıklanacak oaln elemetin text değeri : {textContent}")
        driver.execute_script("""
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);
        """, element)
        print("Güçlü JS click başarılı")

        
        
        return True

    except Exception as e:
        print(f"Güçlü JS click başarısız: {e}")
        return False
    
    

def Stale_element_onune_gec(driver: WebDriver, by: By, selector: str, max_retries: int = 3):
    """Stale element hatası için retry mekanizması"""
    for attempt in range(max_retries):
        try:
            # Her seferinde element yeniden bul
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, selector))
            )
            
            print(f"Element bulundu")
            return element
        
        except StaleElementReferenceException:
            print(f"Stale element (Deneme {attempt + 1}/{max_retries}), tekrar deniyor...")
            time.sleep(0.5)
        
        except Exception as e:
            print(f"Hata: {e}")
            return False
    return False


# ---------------------- genel yardımcılar ----------------------

def find_element_with_retry(driver: WebDriver, by: By, selector: str, max_retries: int = 3, wait_time: int = 10):
    """Element araması yapar, stale hatası gelirse yeniden dener.

    Kullanım:
        elem = find_element_with_retry(driver, By.ID, "myId")

    Args:
        driver: WebDriver örneği.
        by: Selenium By tipi (By.ID, By.CSS_SELECTOR, vs.).
        selector: Aranan değer.
        max_retries: Maksimum deneme sayısı.
        wait_time: Her denemede bekleme süresi (saniye).

    Returns:
        Bulunan WebElement ya da None.
    """
    for attempt in range(max_retries):
        try:
            return WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((by, selector))
            )
        except StaleElementReferenceException:
            print(f"Stale element while locating {selector} (attempt {attempt+1}), retrying...")
            time.sleep(0.5)
    return None


def click_with_retry(driver: WebDriver, by: By, selector: str, max_retries: int = 3):
    """Her denemede elementi yeniden bulup tıklama yapar.

    Çoğu stale hatası, referansı elinde tutan kodun
    sayfa yenilendiğinde/DOM değiştiğinde başarısız olmasından
    kaynaklanır. Bu yardımcı, elementi her defasında tekrar
    sorgulayarak hatayı azaltır.

    Args:
        driver: WebDriver örneği.
        by: Selenium By tipi.
        selector: Arama değeri.
        max_retries: Deneme sayısı.

    Returns:
        True tıklama başarılıysa, False değilse.
    """
    for attempt in range(max_retries):
        try:
            element = find_element_with_retry(driver, by, selector, max_retries=1)
            if element is None:
                return False
            element.click()
            print(f"Click başarılı: {selector}")
            return True
        except StaleElementReferenceException:
            print(f"Stale element during click (attempt {attempt+1}), retrying...")
            time.sleep(0.5)
        except Exception as e:
            print(f"Click error: {e}")
            return False
    return False

def safe_js_click(driver : WebDriver, element: WebElement):
    """
    Gönderilen WebElement üzerinden JS ile tıklama dener.
    Eğer element bayatlamışsa (stale), hata fırlatır; 
    bu durumda elementi çağırdığınız yerde yeniden bulmalısınız.
    """
    try:
        # Elementin hala canlı olup olmadığını küçük bir kontrolle (tag_name gibi) test ediyoruz
        _ = element.tag_name 
        
        # JavaScript ile tıklama işlemi
        driver.execute_script("arguments[0].click();", element)
        return True
        
    except StaleElementReferenceException:
        print("Hata: Gönderdiğiniz element artık mevcut değil (Stale).")
        return False
    except Exception as e:
        print(f"Beklenmedik hata: {e}")
        return False
    
def wait_for_page_load(driver : WebDriver, timeout=30):
    """Sayfa DOM yapısı tamamen yüklenene kadar bekler."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except Exception as e:
        print(f"Sayfa yüklenirken zaman aşımı oluştu: {e}")


def element_bekleme_ve_elementi_click_etme(by : By,selector : str,driver : WebDriver,max_retries = 3):
    """
    * Belirli bir elemetin yüklenmesini bekler 
    * selector değeri, bir sınıf ismi ya da ID ismi ya da css niteliği olabilir
    * Ardından o elementi click yapar 
    * Eğer normal click çalışmazsa JavaScript ile click yapmayı dener
    """
    for attempt in range(max_retries):
            try:
                # Element'i yeniden bul
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )
                element.click()
                print(f"Normal click başarılı: {selector}")
                break
            except StaleElementReferenceException:
                print(f"Stale element (Deneme {attempt + 1}), JavaScript ile deniyor...")
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    js_click(element, driver)
                    break
                except:
                    time.sleep(0.5)
            except Exception as e:
                print(f"Hata: {e}")


def click_and_wait_for_text(element_to_click: WebElement, text_element_selector: str, driver: WebDriver, timeout: int = 10):
    """
    Bir elementi tıkla ve başka bir elemanın metin içeriğinin yüklenmesini bekle.
    
    Sorun: JavaScript ile tıklamadan sonra, sayfanın dinamik olarak güncellenen içeriği 
    henüz yüklenmemiş olabilir. Element DOM'da var ama metin boştur.
    
    Çözüm: Tıklamadan sonra, hedef elemanın metin içeriği boş olmayan bir hale gelene kadar bekleyin.
    
    Args:
        element_to_click: Tıklanacak WebElement
        text_element_selector: Metnin yüklenmesini beklenen elemanın CSS selectoru
        driver: WebDriver instance
        timeout: Bekleme süresi (saniye)
    
    Returns:
        str: Elemanın metin içeriği (boş değilse), None (hata durumunda)
    """
    try:
        # Elementi güçlü JavaScript ile tıkla
        js_click_guclu(element=element_to_click, driver=driver)
        
        # Metin içeriğinin yüklenmesini bekle
        wait = WebDriverWait(driver, timeout)
        
        # Element görünür olana kadar bekle
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, text_element_selector)))
        
        # Metin içeriği boş olmayan bir duruma gelene kadar bekle
        wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, text_element_selector).text.strip() != ""
        )
        
        # Metni al ve döndür
        element = driver.find_element(By.CSS_SELECTOR, text_element_selector)
        text_value = element.text.strip()
        return text_value
        
    except TimeoutException:
        print(f"Timeout: Metin '{text_element_selector}' içinde yüklenemedi")
        return None
    except Exception as e:
        print(f"Hata (click_and_wait_for_text): {e}")
        return None


def go_back_and_wait(driver: WebDriver, timeout: int = 10):
    """
    Tarayıcı tarihçesini geri al ve sayfa tamamen yükleninceye kadar bekle.

    Bazı sitelerde `driver.back()` çağrısı, uygulama tarihçesini günceller ama
    yeni sayfa veya önceki durum henüz render edilmeden kod yürümeye devam eder.
    Sonuç olarak sonraki `find_element` çağrıları stale element veya "eleman
    bulunamadı" hatası verir, çünkü sayfa hâlâ yükleniyordur.

    Bu yardımcı fonksiyon, `driver.back()` yaptıktan sonra `wait_for_page_load`
    ile beklemeyi otomatikleştirir.
    """
    try:
        driver.back()
    except Exception as e:
        print(f"go_back_and_wait: geri gitme sırasında hata: {e}")
    # sayfanın yeniden yüklenmesini bekle
    try:
        wait_for_page_load(driver=driver, timeout=timeout)
    except Exception:
        # wait_for_page_load zaten hata bastırıyor, burada sessizce geçebiliriz
        pass


def genel_element_bekleme(by : By,selector : str,driver : WebDriver,max_retries : int = 3):
    """
    * Her türlü elementi bekleyebilirsiniz 
    * By taga ID ya da sınıf ismine göre ayarlayabilirsiniz 
    * selector ile istediğiniz değeri verebilirsiniz 
    * Driver sürücüdür 
    * Elementi bulana kadar 3 defa dönder 
    * Eğer element bulunursa elementin kendisi döner
    * Yok eğer bulunamazsa None olarak dönder
    """
    for attempt in range(max_retries):
            try:
                # Element'i yeniden bul
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )

                elementler = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((by, selector))
                )

                return element
            
            except Exception as e:
                print(f"genel_element_bekleme hata meydana geldi : {e}")
                return None
    
def temiz_trleri_alma_kodu(düzensiz_trler: list[WebElement], driver: WebDriver):
    print(f"Düzensiz trlerin uzunluğu: {len(düzensiz_trler)}")
    
    # Sayfanın stabil olduğundan emin olalım
    wait_for_page_load(driver=driver)

    temiz_trler_listesi: list[WebElement] = []

    for tr in düzensiz_trler:
        # Hem textContent hem innerText'e bakmak yerine doğrudan text kullanabilirsin
        # Ya da daha garantisi için textContent alıp strip yapalım
        icerik = tr.get_attribute("textContent").strip()
        
        # Eğer içerik doluysa (herhangi bir harf/rakam varsa) listeye ekle
        if icerik:
            temiz_trler_listesi.append(tr)
        else:
            # Boş satırları loglamak istersen buraya ekleyebilirsin
            continue
    
    print(f"Düzenli trlerin uzunluğu: {len(temiz_trler_listesi)}")
    return temiz_trler_listesi


def Belediye_Baskanligi_Secim_Sonuclarina_Tiklama(driver : WebDriver):
    """
    * Belediye_Başkanlığı_Seçim_Sonuçlari_css_a_linki : a[href='/secim-sonuc-istatistik/secim-sonuc'] linkini seçer 
    * Bundan sonra, Eğer hata vermezse birkaç tane web elementli link gelecek (Eğer web elementleri bulunamazsa None döner)
    * Bu link 2 farklı değer barındrırır ama birinci seçeceğiz 
    * En son olarak seçtiğimiz linke tıklyacağız 
    * Linke eğer tıkladıysak ise True döner

    """

    Belediye_Başkanlığı_Seçim_Sonuçlari_css_a_linki = "a[href='/secim-sonuc-istatistik/secim-sonuc']"

    Belediye_Başkanlığı_Seçim_Sonuçları_listesi = css_birden_fazla_nitelik_secici(driver=driver,nitelik_secici=Belediye_Başkanlığı_Seçim_Sonuçlari_css_a_linki)
                    
    if not Belediye_Başkanlığı_Seçim_Sonuçları_listesi:
        print(f"Belediye_Başkanlığı_Seçim_Sonuçları_listesi boş gelmiştir ve False dönüyor")
        return None

    else:
        print(f"Belediye Başkanlığı Seçim Sonuçları listesi boş değil : {len(Belediye_Başkanlığı_Seçim_Sonuçları_listesi)}")

        # Burada Belediye_Başkanlığı_Seçim_Sonuçları_listesi ilk değerini al 
        # Tıkla ikinci değer önemsiz 
        belediye_başkanlığı_a_linki = Belediye_Başkanlığı_Seçim_Sonuçları_listesi[0]

        tiklama_yapildi_mi = safe_js_click(driver=driver,element=belediye_başkanlığı_a_linki)

        if tiklama_yapildi_mi:
            print(f"Tiklama yapildi ve True dönüyor")
            return True



async def Belediye_Baskanlığı_Seçimlerini_Secme(driver : WebDriver,
                                                Belediye_Baskanligi_Secimleri_Web_Element : WebElement,
                                                index_no : int):
    """
    * collapse0 ID değerine sahip birçok seçim yer alacak 
    * 2 Haziran 2024 Yenilenme Seçimleri 
    * 31 Mart 2024 Mahalli İdareler Genel Seçimi 
    * Ve son olarak 29 Mart 2009 olarak sona eriyor
    * Bu fonksiyon id_collapse_linkler içinde index_no'ya göre bunlardan birini seçecek ve tıklayacak
    * Örneğin index_no eğer 0 ise : 2 Haziran 2024 Yenilenme Seçimleri  
    * eğer index_no 1 ise :  31 Mart 2024 Mahalli İdareler Genel Seçimi
    * En son olarak eğer işlemler başarılı ise Seçim ID Döndürür Eğer başarısız ise de None döndürecek
    """
    
    collapse_id = "collapse0"

    id_collapse_linkler = Belediye_Baskanligi_Secimleri_Web_Element.find_elements(By.ID,value=collapse_id)
    # • 2 Haziran 2024 Yenilenme Seçimleri 
    # • 31 Mart 2024 Mahalli İdareler Genel Seçimi 
    # Ve son olarak 29 Mart 2009 olarak sona eriyor
    
    if id_collapse_linkler:
        try: # id_collapse_linkler stale element hatası verebilir, bu yüzden tekrar buluyoruz 
            id_collapse_linkler = birden_fazla_ID_element_bulucu(element_ID_ismi=collapse_id,driver=driver)
            id_si_collapse_olan_link = id_collapse_linkler[index_no]
            # 0.ncı indeks 2 Haziran 2024 seçimlerini barındırır

            seçim_ismi = id_si_collapse_olan_link.text.strip()
            
            print(f"Seçim ismi :  {seçim_ismi}")

            Secim_ID_degeri = await Yeni_Bir_Secim_Ekleme(secim_ismi=seçim_ismi)

            card_body_css_selector = "div[class='card-body']"
            card_body_li_div = id_si_collapse_olan_link.find_element(By.CSS_SELECTOR, card_body_css_selector)
            tiklanacak_div_css_seçici_ismi = "div[class='sub-item px-3 py-2']"
            tiklanacak_div = card_body_li_div.find_element(By.CSS_SELECTOR, tiklanacak_div_css_seçici_ismi)
            


            tiklama_yapildi_mi = safe_js_click(driver=driver,element=tiklanacak_div)
            if tiklama_yapildi_mi:
                print(f"tiklama yapıliyor: {tiklanacak_div_css_seçici_ismi}")
                return Secim_ID_degeri

            else:
                print(f"tiklama yapılamadı: {tiklanacak_div_css_seçici_ismi}")
                return None

            

        except Exception as Hata:
            print(f"Belediye_Baskanlığı_Seçimlerini_Secme Hata meydana geldi : {Hata}")
            return None
        
        
async def Milletvekili_Genel_Secimleri_ni_Secme(driver : WebDriver,Milletvekili_Secimleri_Web_Element : WebElement,
                                                 index_no : int):

    """
    * collapse5 id değerlerine sahip olan elementler seçilecek bunlar sırayla  
    * CUMHURBAŞKANI VE 28.DÖNEM MİLLETVEKİLİ GENEL SEÇİMİ index no 0 
    * CUMHURBAŞKANI VE 27.DÖNEM MİLLETVEKİLİ GENEL SEÇİMİ index no 1 
    * en son olarak 24.DÖNEM MİLLETVEKİLİ GENEL SEÇİMİ 
    * Eğer linklerden birine tıklama işlemi başarılı olursa Seçim_ID değeri dönecek 
    * Eğer herhangi bir başarısızlık olursa None olarak dönecek
    """         

    collapse_id = "collapse5"

    id_collapse_linkler = Milletvekili_Secimleri_Web_Element.find_elements(By.ID,value=collapse_id)
    # CUMHURBAŞKANI VE 28.DÖNEM MİLLETVEKİLİ GENEL SEÇİMİ index no 0 
    # CUMHURBAŞKANI VE 27.DÖNEM MİLLETVEKİLİ GENEL SEÇİMİ index no 1 
    # en son olarak 24.DÖNEM MİLLETVEKİLİ GENEL SEÇİMİ
    
    if id_collapse_linkler:
        try: # id_collapse_linkler stale element hatası verebilir, bu yüzden tekrar buluyoruz 
            id_collapse_linkler = birden_fazla_ID_element_bulucu(element_ID_ismi=collapse_id,driver=driver)
            id_si_collapse_olan_link = id_collapse_linkler[index_no]
            # 0.ncı indeks 2 Haziran 2024 seçimlerini barındırır

            seçim_ismi = id_si_collapse_olan_link.get_attribute("textContent").strip()
            
            
            print(f"Seçim ismi :  {seçim_ismi}")

            Secim_ID_degeri = await Yeni_Bir_Secim_Ekleme(secim_ismi=seçim_ismi)

            card_body_css_selector = "div[class='card-body']"
            card_body_li_div = id_si_collapse_olan_link.find_element(By.CSS_SELECTOR, card_body_css_selector)
            tiklanacak_div_css_seçici_ismi = "div[class='sub-item px-3 py-2']"
            tiklanacak_div = card_body_li_div.find_element(By.CSS_SELECTOR, tiklanacak_div_css_seçici_ismi)
            


            tiklama_yapildi_mi = safe_js_click(driver=driver,element=tiklanacak_div)
            if tiklama_yapildi_mi:
                print(f"tiklama yapıliyor: {tiklanacak_div_css_seçici_ismi}")
                return Secim_ID_degeri

            else:
                print(f"tiklama yapılamadı: {tiklanacak_div_css_seçici_ismi}")
                return None

            

        except Exception as Hata:
            print(f"Milletvekili_Genel_Secimleri_ni_Secme Hata meydana geldi : {Hata}")
            return None



def Milletvekili_Secim_Sonuclarina_Tiklama(driver : WebDriver):
    """
    * SEÇİM SONUÇ VERİLERİ'nin altındaki Milletvekili Seçim Sonuçlarına tıklayacak (Sadece tek bir element var)
    * İlk olarak, a[href='"/secim-sonuc-istatistik/secim-sonuc"'] nitelik seçici ile arar 
    * Eğer bu element bulunamazsa None döner
    * Eğer bulursa ise tek link olduğu için clicklenir 
    * Clickleme işlemi başarılı olursa da Milletvekili Seçim Sonuçlarının İl ve İlçe Bazlı verileri alabiliriz 
    * En son olarak eğer fonksiyon başarılı bir şekilde linke tıkladıysa True dönecek
    """

    css_nitelik_secici_ = "a[href='/secim-sonuc-istatistik/secim-sonuc']"

    Milletvekili_secim_sonuclari_tiklanacak_link = Css_nitelik_secici(driver=driver,
                                                                      nitelik_secici=css_nitelik_secici_)
    
    if Milletvekili_secim_sonuclari_tiklanacak_link is None:
        print(f"Milletvekili_Secim_Sonuclarina_Tiklama fonksiyonunda Tıklanılacak element bulunamadi")
        return None
    
    else:
        print(f"""Milletvekili_Secim_Sonuclarina_Tiklama fonksiyonunda a[href='/secim-sonuc-istatistik/secim-sonuc'] 
              linki bulundu ve birazdan tıklayacağız""")
        
        tiklama_yapildi_mi = js_click_guclu(driver=driver,
                                          element=Milletvekili_secim_sonuclari_tiklanacak_link)
        
        if tiklama_yapildi_mi:
            print(f"Milletvekili_Secim_Sonuclarina_Tiklama fonksiyonunda Tıklama işlemi yapıldı ve True dönecek")
            return True


async def Cumhurbaskani_Secimleri_ni_Secme(driver : WebDriver,Cumhurbaskani_Secimi_Web_Element : WebElement,index_no : int):
    """
    Bu fonksiyon Cumhurbaşkanlığı seçimlerini seçmek için kullanılacak

    

    div[id='collapse6'] seçilmeli ve bunlardan sadece 4 tane var 

    *  CUMHURBAŞKANI SEÇİMİNİN İKİNCİ OYLAMASI | CUMHURBAŞKANI SEÇİMİ (28 Mayıs 2023) index 0 
    *  CUMHURBAŞKANI VE 28.DÖNEM MİLLETVEKİLİ GENEL SEÇİMİ | CUMHURBAŞKANI SEÇİMİ (14 Mayıs 2023) index 1 
    *  CUMHURBAŞKANI VE 27.DÖNEM MİLLETVEKİLİ GENEL SEÇİMİ | CUMHURBAŞKANI SEÇİMİ (24 Haziran 2018) index 2 
    *  ONİKİNCİ CUMHURBAŞKANI SEÇİMİ | CUMHURBAŞKANI SEÇİMİ (10 Ağustos 2014) index 3

    bunlar seçilecek

    eğer yeni bir seçim ismi görülürse, o zaman değer veritabanına kaydedilir ve ID değeri döner (varsa zaten ID kendisi döner)
    Eğer işlemlerde bir hata olursa o zaman None döner
    """

    css_id_secici_str_degeri : str = "div[id='collapse6']"

    id_element_ismi : str = "collapse6"

    

    id_collapse_6_lı_divler = Cumhurbaskani_Secimi_Web_Element.find_elements(By.CSS_SELECTOR,css_id_secici_str_degeri)

    print(f"Collapse 6'lı divler uzunluğu : {len(id_collapse_6_lı_divler)}")

    if id_collapse_6_lı_divler:
        try:
            # hatanın önüne geçmek için tekrar buluyoruz
            id_collapse_linkler = birden_fazla_ID_element_bulucu(element_ID_ismi=id_element_ismi,driver=driver)
            id_collapse_link = id_collapse_linkler[index_no]

            seçim_ismi = id_collapse_link.get_attribute("textContent").strip()
            print(f"Seçim ismi : {seçim_ismi}")

            Secim_ID_degeri = await Yeni_Bir_Secim_Ekleme(secim_ismi=seçim_ismi)

            card_body_css_selector = "div[class='card-body']"
            card_body_li_div = id_collapse_link.find_element(By.CSS_SELECTOR, card_body_css_selector)

            tiklanacak_div_css_seçici_ismi = "div[class='sub-item px-3 py-2']"
            tiklanacak_div = card_body_li_div.find_element(By.CSS_SELECTOR, tiklanacak_div_css_seçici_ismi)

            tiklama_yapildi_mi = safe_js_click(driver=driver,element=tiklanacak_div)
            
            if tiklama_yapildi_mi:
                print(f"tiklama yapıliyor: {tiklanacak_div_css_seçici_ismi}")
                return Secim_ID_degeri
            else:
                print(f"tiklama yapılamadı: {tiklanacak_div_css_seçici_ismi}")
                return None
            

        except Exception as hata:
            print(f"Cumhurbaskani_Secimleri_ni_Secme fonksiyonunda hata meydana geldi : {hata}")
            return None
        

def Cumhurbaskanligi_Secim_Sonuclarina_Tiklama(driver : WebDriver):
    """
    * SEÇİM SONUÇ VERİLERİ hemen altındaki Cumhurbaşkanlığı Seçim Sonuçlarina tıklayacak
    * Eğer tıklama başarılı ise True dönecek yani devam edebiliriz (ardından il ve ilçe bazlı değerler alınabilir)
    * Eğer başarısız ise None dönecek
    """

    # Sadece bir tane var alabilirsin
    css_nitelik_seçici = "a[href='/secim-sonuc-istatistik/secim-sonuc']"

    Cumhurbaskanlığı_secim_sonuclarina_tiklanacak_link = Css_nitelik_secici(driver=driver,nitelik_secici=css_nitelik_seçici)

    if Cumhurbaskanlığı_secim_sonuclarina_tiklanacak_link is None:
        print(f"Cumhurbaskanligi_Secim_Sonuclarina_Tiklama Tıklanılacak element bulunamadi")
        return None
    
    else:
        print(f"""Cumhurbaskanligi_Secim_Sonuclarina_Tiklama a[href='/secim-sonuc-istatistik/secim-sonuc'] 
              linki bulundu ve birazdan tıklayacağız""")
        
        tiklama_yapildi_mi = js_click_guclu(driver=driver,
                                          element=Cumhurbaskanlığı_secim_sonuclarina_tiklanacak_link)
        
        if tiklama_yapildi_mi:
            print(f"Cumhurbaskanligi_Secim_Sonuclarina_Tiklama fonksiyonunda Tıklama işlemi yapıldı ve True dönecek")
            return True

        else:
            print(f"Cumhurbaskanligi_Secim_Sonuclarina_Tiklama a[href='/secim-sonuc-istatistik/secim-sonuc'] tiklama sirasında hata aldım")
            return None
        


def element_tiklanabilir_olana_kadar_bekleme(by : By,driver : WebDriver,selector : str):
    """
    * Bu element popup kesin olarak kapatmak için yaratildi 
    * Popup, tıklanılabilir olana kadar bekler ardından tıklar ve ardından tıklar

    Args:
        by (By): ID ya da class ya da tag name olabilir 
        driver (WebDriver): Web Sürücüsü 
        selector (str): selector css değeri 
    """

    wait = WebDriverWait(driver=driver,timeout=60)

    try:
        wait_tuple = (by,selector)
        print(f"Selector element : {selector} tıklanabilir olana kadar bekliyor")
        wait.until(EC.element_to_be_clickable(wait_tuple)).click()
    
    except Exception as Hata:
        print(f"element_tiklanabilir_olana_kadar_bekleme fonksiyonunda hata var : {Hata}")
    


