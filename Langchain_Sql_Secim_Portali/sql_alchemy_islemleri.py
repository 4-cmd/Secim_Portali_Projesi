from my_py_settings import My_Settings
from Models import (Parti_Sonuclari_Tablosu,
                    Partiler,
                    Aday_Sonuclar_Tablosu,
                    Adaylar,
                    Cografya_Kutuphanesi,
                    Secimler,
                    Secim_Genel_Bilgiler)
from sqlalchemy import select,and_,or_
from sqlalchemy.orm import Session
from my_py_settings import settings_of_pydantic


settings = settings_of_pydantic

session = settings.session_function

def adaylari_getir():
    """
    * Adaylar tablosundaki adayları LLM iletecek

    """
    stmt = select(Adaylar.Aday_ismi)
    execute = session.execute(stmt)

    tum_adaylar = execute.scalars().all()

    Adaylar_ciktisi = ""

    for aday in tum_adaylar:
        Adaylar_ciktisi += aday + "\n\n\n"
    
    return Adaylar_ciktisi

def partileri_getir():
    """
    * Partiler tablosundaki Partileri getirir 
    """

    stmt = select(Partiler.Parti_ismi)
    execute = session.execute(stmt)

    Partiler_list = execute.scalars().all()

    Partiler_cikti = ""

    for Parti in Partiler_list:
        Partiler_cikti += Parti + "\n\n\n"
    
    return Partiler_cikti

def secimleri_getir():
    """
    * Secimler tablosundaki secimleri getirir 
    """

    stmt = select(Secimler.Secim_ismi)
    execute = session.execute(stmt)

    Secimler_list = execute.scalars().all()

    Secimler_cikti = ""

    for Secim in Secimler_list:
        Secimler_cikti += Secim + "\n\n\n"
    
    return Secimler_cikti

