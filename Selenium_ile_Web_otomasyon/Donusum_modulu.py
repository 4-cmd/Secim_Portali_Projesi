


def from_string_to_int(string_sayi : str):
    """
    String olan bir sayiyi integer değere dönüştürmek için yaratıldı
    """
    try:
        temizlenmis_string = string_sayi.replace(".","").replace(",","")
        int_degeri = int(temizlenmis_string)
        return int_degeri
    except ValueError:
        print(f"'{string_sayi}' bir Integer'a dönüştürülemedi.")
        return None
    
def from_string_to_float(string_sayi : str):
    """
    String bir sayi değerini float dönüştürmek için yaratıldı
    """
    try:
        # Öncelikle string içindeki nokta ve virgülleri temizleyelim
        temizlenmis_string = string_sayi.replace("%","")
        float_degeri = float(temizlenmis_string)
        return float_degeri
    except ValueError:
        print(f"'{string_sayi}' bir float'a dönüştürülemedi.")
        return None
    
