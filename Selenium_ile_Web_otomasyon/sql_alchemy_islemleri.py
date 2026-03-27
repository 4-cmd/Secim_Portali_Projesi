from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)
from Pydantic_Page import py_settings_variable
from Models import (Parti_Sonuclari_Tablosu,
                    Partiler,
                    Aday_Sonuclar_Tablosu,
                    Adaylar,
                    Cografya_Kutuphanesi,
                    Secimler,
                    Secim_Genel_Bilgiler)
from sqlalchemy import Select,select,and_,or_

database_url = py_settings_variable.DATABASE_URL_STR

# Echo=True SQL komutlarını konsola basar (debug için harikadır)
engine = create_async_engine(database_url)

# Session Factory: Her istekte yeni bir session yaratmak için kullanılır
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def Yeni_Bir_Parti_Ekle(parti_ismi : str):
    """
    * Burada yeni bir parti adı eklenir 
    * Ancak parti Adı  Partiler tablosunda yok ise o zaman kaydedilir ve ID değeri alınır,
    * daha önceden kayıt edilmiş ise, o zaman ID değeri seçilir ve alınır
    """
    async with AsyncSessionLocal() as session:
        stmt = select(Partiler.ID).filter(Partiler.Parti_ismi == parti_ismi)
        execute = await session.execute(stmt)
        parti_daha_onceden_kayit_edildi_mi = execute.scalar_one_or_none()

        if parti_daha_onceden_kayit_edildi_mi is None:
            new_instance = Partiler()
            new_instance.Parti_ismi = parti_ismi

            session.add(new_instance)

            await session.commit()

            await session.refresh(new_instance)

            ID_deger = new_instance.ID

            print(f"Parti ismi daha önce veritabanına kayıt edilmedi : {parti_ismi}\nŞimdi kaydedildi ve ID değeri : {ID_deger} döndürülecek")
            return ID_deger
        
        else:
            print(f"Parti ismi zaten veritabanında var : {parti_ismi} ID değeri döndürülüyor : {parti_daha_onceden_kayit_edildi_mi}")
            return parti_daha_onceden_kayit_edildi_mi


async def Yeni_Bir_Secim_Ekleme(secim_ismi : str):
    """
    * Yeni bir seçim adı eklenir 
    * Eğer seçim adı daha önce Seçimler tablosunda kayıt edilmişse, ID değeri alınır ve döndürürlür 
    * Eeğer seçim adı daha önce kayıt edilmemişse, o zaman yeni bir seçin adı kaydedilir ve ID değeri alınır ve döndürülür
    """

    async with AsyncSessionLocal() as session:
        stmt = select(Secimler.ID).filter(Secimler.Secim_ismi == secim_ismi)
        execute = await session.execute(stmt)
        secim_daha_onceden_kayit_edildi_mi = execute.scalar_one_or_none()

        if secim_daha_onceden_kayit_edildi_mi is None:
            new_instance = Secimler()
            new_instance.Secim_ismi = secim_ismi

            session.add(new_instance)

            await session.commit()

            await session.refresh(new_instance)

            ID_deger = new_instance.ID

            print(f"Secim ismi daha önce veritabanına kayıt edilmedi : {secim_ismi}\nŞimdi kaydedildi ve ID değeri : {ID_deger} döndürülecek")
            return ID_deger
        
        else:
            print(f"Secim ismi zaten veritabanında var : {secim_ismi} ID değeri döndürülüyor")
            return secim_daha_onceden_kayit_edildi_mi

async def Cografya_Kutuphanesine_Yeni_Bir_Deger_Ekleme(tanım_ekleme : str):

    """
    * Yeni bir tanım ekler şehir olmalı
    * Eğer tanım daha önce Cografya_Kutuphanesi tablosunda kayıt edilmişse, ID değeri alınır ve döndürürlür
    * Eeğer tanım daha önce kayıt edilmemişse, o zaman yeni bir tanım kaydedilir ve ID değeri alınır ve döndürülür
    """

    async with AsyncSessionLocal() as session:
        stmt = select(Cografya_Kutuphanesi.ID).filter(Cografya_Kutuphanesi.Tanım == tanım_ekleme)
        execute = await session.execute(stmt)
        tanim_daha_onceden_kayit_edildi_mi = execute.scalar_one_or_none()

        if tanim_daha_onceden_kayit_edildi_mi is None:
            new_instance = Cografya_Kutuphanesi()
            new_instance.Tanım = tanım_ekleme
            new_instance.UST_ID = 0

            session.add(new_instance)

            await session.commit()

            await session.refresh(new_instance)

            ID_deger = new_instance.ID

            print(f"Veribanına daha önce {tanım_ekleme} bir veri eklenmedi şimdi ekleniyor ve ID değeri : {ID_deger} döndürülecek")
            return ID_deger
        
        else:
            print(f"Tanım zaten veritabanında var : {tanım_ekleme} ID değeri döndürülüyor")
            return tanim_daha_onceden_kayit_edildi_mi
        

async def Parti_Sonuclarina_Yeni_Deger_Ekleme(Secim_ID : int,Parti_ID : int,Cografya_Kutuphanesi_ID : int,Parti_Oy_Sayisi : int,Parti_Oy_Orani : float = None):
    """
    * Parti Sonuçları tablosuna yeni bir değer ekler (Eğer kayıt edildiyse tekrar eklemez)
    * ID Değerini döndürür 
    * Daha sonra ID değeri kullanılarak Partinin Aldığı oy orani bulunacak 
    * Daha sonra Oy orani satiri güncellenecek 
    """
    async with AsyncSessionLocal() as session:
        
        stmt = select(Parti_Sonuclari_Tablosu.ID).filter(
        and_(
            Parti_Sonuclari_Tablosu.Parti_ID == Parti_ID,
            Parti_Sonuclari_Tablosu.Cografya_Kutuphanesi_ID == Cografya_Kutuphanesi_ID,
            Parti_Sonuclari_Tablosu.Secim_ID == Secim_ID
        )
    )

        execute = await session.execute(stmt)
        parti_sonuclari_kaydi = execute.scalar_one_or_none()

        if parti_sonuclari_kaydi is not None:
            print(f"Daha önceden Parti Sonuçları tablosunda Parti_ID değeri {Parti_ID} Cografya_Kutuphanesi_ID değeri {Cografya_Kutuphanesi_ID} ve Secim_ID değeri {Secim_ID} olan bir kayıt var. Yeni bir kayıt eklenmeyecek ve ID değer döndürülecek : {parti_sonuclari_kaydi}")
            return parti_sonuclari_kaydi
        
        else:
            new_instance = Parti_Sonuclari_Tablosu()
            new_instance.Secim_ID = Secim_ID
            new_instance.Parti_ID = Parti_ID
            new_instance.Cografya_Kutuphanesi_ID = Cografya_Kutuphanesi_ID
            new_instance.Parti_Oy_Sayisi = Parti_Oy_Sayisi
            new_instance.Parti_Oy_Orani = Parti_Oy_Orani

            session.add(new_instance)

            await session.commit()

            await session.refresh(new_instance)

            ID_deger = new_instance.ID

            print(f"Parti Sonuçları tablosuna yeni bir değer eklendi ID değeri : {ID_deger} döndürülecek")
            return ID_deger
    
async def Parti_Sonuclarinin_Oy_Oranini_Guncelleme(Parti_Sonuclari_ID_degeri : int,Oy_orani : float):
    """
    Parti Sonuçları tablosunda var olan bir kaydın oy oranını günceller 

    """

    async with AsyncSessionLocal() as session:
        stmt = select(Parti_Sonuclari_Tablosu).filter(Parti_Sonuclari_Tablosu.ID == Parti_Sonuclari_ID_degeri)
        execute = await session.execute(stmt)
        kayit_edilecek_Parti_Sonuclari_kaydi = execute.scalar_one_or_none()

        if kayit_edilecek_Parti_Sonuclari_kaydi is not None:
            kayit_edilecek_Parti_Sonuclari_kaydi.Parti_Oy_Orani = Oy_orani

            await session.commit()

            print(f"Parti Sonuçları tablosunda ID değeri {Parti_Sonuclari_ID_degeri} olan kaydın oy oranı güncellendi : {Oy_orani}")
        
        else:
            print(f"Parti Sonuçları tablosunda ID değeri {Parti_Sonuclari_ID_degeri} olan bir kayıt bulunamadı. Güncelleme yapılamadı.")
    
async def Secim_Genel_Bilgiler_yeni_deger_yukleme(Kayitli_Secmen_Sayisi : int,Oy_Kullanan_Secmen_Sayisi : int,
                                                  Gecerli_Oy_Sayisi : int,
                                                Cografya_Kutuphanesi_ID : int,Secim_ID : int):
    """
    * Secim_Genel_Bilgiler yeni bir değer ekler 
    * Eğer Cografya_Kutuphanesi_ID değeri daha önce Secim_Genel_Bilgiler tablosunda kayıt edilmişse, 
    * o zaman yeni bir kayıt eklenmez ve var olan kaydın ID değeri döndürülür
    """

    async with AsyncSessionLocal() as session:
        stmt = select(Secim_Genel_Bilgiler).filter(and_(
            Secim_Genel_Bilgiler.Cografya_Kutuphanesi_ID == Cografya_Kutuphanesi_ID,
            Secim_Genel_Bilgiler.Secim_ID == Secim_ID
        ))

        execute = await session.execute(stmt)
        secim_genel_bilgiler_kaydi = execute.scalar_one_or_none()
        
        if secim_genel_bilgiler_kaydi is not None:
            print(f"Cografya_Kutuphanesi_ID değeri : {Cografya_Kutuphanesi_ID} ve Seçim ID değeri : {Secim_ID} değeri daha önce  Secim_Genel_Bilgiler tablosuna kayit edildi")
            return secim_genel_bilgiler_kaydi.ID
        
        else:
            new_instance = Secim_Genel_Bilgiler()
            new_instance.Kayitli_Secmen_Sayisi = Kayitli_Secmen_Sayisi
            new_instance.Oy_Kullanan_Secmen_Sayisi = Oy_Kullanan_Secmen_Sayisi
            new_instance.Gecerli_Oy_Sayisi = Gecerli_Oy_Sayisi
            new_instance.Cografya_Kutuphanesi_ID = Cografya_Kutuphanesi_ID
            new_instance.Secim_ID = Secim_ID

            session.add(new_instance)

            await session.commit()

            await session.refresh(new_instance)

            ID_deger = new_instance.ID

            print(f"Secim_Genel_Bilgiler tablosuna yeni bir değer eklendi ID değeri : {ID_deger} döndürülecek")
            return ID_deger

async def Sehir_bulma_islemi(path_str_plakasi : str):
    """
    * Path ile tıklama sonrasında, Path'in il_id değeri alınır 
    * Daha sonra burada string değerden integer değere çevrilir 
    * Ardından, Coğrafya Kütüphanesindeki plaka numarasına erişmeye çalışılır 
    * En son olarak, Plaka numarasına karşılık gelen ve UST ID Değeri sıfır olan şehrin ID değerini döndürülür
    * Eğer bulunamazsa None olarak döndürülecek
    """

    integer_path_plakasi = int(path_str_plakasi)

    async with AsyncSessionLocal() as session:
        stmt = select(Cografya_Kutuphanesi.ID).filter(and_(
            Cografya_Kutuphanesi.UST_ID == 0,Cografya_Kutuphanesi.Plaka_numarasi == integer_path_plakasi
        ))

        execute = await session.execute(stmt)

        Sehir_ismi_var_mi = execute.scalar_one_or_none()

        if Sehir_ismi_var_mi:
            print(f"Pathin il idsine karşılık Sehir ismi bulundu Sehir ID Değeri : {Sehir_ismi_var_mi}")
            print(f"Sehir ismi döndürülecek")
            return Sehir_ismi_var_mi
        
        else:
            
            return None
       
async def Cografya_Kutuphanesine_Ilce_Ekleme(tanım_ekleme : str,UST_ID_sehir_ID_değeri : int):

    """
    * Cografya Kutuphanesine yeni bir ilçe eklenir
    * İlçenin bağlı olduğu UST ID yani şehir ID gönderilmelidir
    * Eğer ilçe daha önceden kayit edilmişse, o zaman kayıt edilmez ID değeri döner
    * Eğer ilçe daha önceden kayit edilmemeişse, kayıt edilir ve ID değeri döner
    """

    async with AsyncSessionLocal() as session:
        stmt = select(Cografya_Kutuphanesi.ID).filter(and_(
            Cografya_Kutuphanesi.Tanım == tanım_ekleme,
            Cografya_Kutuphanesi.UST_ID ==UST_ID_sehir_ID_değeri
        ))
        execute = await session.execute(stmt)
        tanim_daha_onceden_kayit_edildi_mi = execute.scalar_one_or_none()

        if tanim_daha_onceden_kayit_edildi_mi is None:
            new_instance = Cografya_Kutuphanesi()
            new_instance.Tanım = tanım_ekleme
            new_instance.UST_ID = UST_ID_sehir_ID_değeri

            session.add(new_instance)

            await session.commit()

            await session.refresh(new_instance)

            ID_deger = new_instance.ID

            print(f"Veribanına daha önce {UST_ID_sehir_ID_değeri}'e bağlı olan {tanım_ekleme} ilçe değeri kayıt edildi ve ID değeri dönecek")
            return ID_deger
        
        else:
            print(f"Tanım zaten veritabanında var : {tanım_ekleme} ID değeri döndürülüyor")
            return tanim_daha_onceden_kayit_edildi_mi
        

async def Illerin_plaka_kodlarini_getirme():
    """
    * İllerin plaka kodlarını alacak 
    * Ve Integer bir liste olarak döndürecek 
    """

    async with AsyncSessionLocal() as session:
        stmt = select(Cografya_Kutuphanesi.Plaka_numarasi).filter(Cografya_Kutuphanesi.UST_ID == 0).order_by(Cografya_Kutuphanesi.Plaka_numarasi.asc())
        execute = await session.execute(stmt)

        Plaka_numaralari_listesi = execute.scalars()

        return Plaka_numaralari_listesi
    

async def Yeni_Bir_Aday_Kaydetme(aday_ismi : str):
    """
    * Yeni bir aday kaydeder veya olan Adayın ID değerini döndürür
    """

    async with AsyncSessionLocal() as session:
        stmt = select(Adaylar.ID).filter(Adaylar.Aday_ismi == aday_ismi)
        execute = await session.execute(stmt)

        aday_id_değeri = execute.scalar_one_or_none()

        if aday_id_değeri is None:
            print(f"Aday ismi : {aday_ismi} daha önce kayıt edilmedi")

            new_instance = Adaylar()
            new_instance.Aday_ismi = aday_ismi

            session.add(new_instance)

            await session.commit()

            await session.refresh(new_instance)

            Aday_ID = new_instance.ID

            print(f"Aday ismi kayıt edildi : {aday_ismi} ve şimdi ID değeri döndürülecek : {Aday_ID}")
            return Aday_ID
        

        else:
            print(f"Aday ismi : {aday_ismi} zaten kayitli bu yüzden ID değeri dönecek aday id : {aday_id_değeri}")
            return aday_id_değeri
        

async def Aday_Sonuclar_Tablosu_na_deger_kaydetme(Secim_ID : int,Aday_ID : int,
                                                Cografya_Kutuphanesi_ID_ : int,
                                                Aday_Oy_Sayisi : int):
    """
    * Aday_Sonuclar_tablosuna yeni bir değer ekler veya değer daha önce kayıt edilmişse ve ID değerini döndürür 
    * ID değeri daha sonra Aday'ın aldığı oy oranini güncellemek için kullanılacak
    """

    stmt = select(Aday_Sonuclar_Tablosu.ID).filter(and_(
        Aday_Sonuclar_Tablosu.Secim_ID == Secim_ID,
        Aday_Sonuclar_Tablosu.Aday_ID == Aday_ID,
        Aday_Sonuclar_Tablosu.Cografya_Kutuphanesi_ID_ == Cografya_Kutuphanesi_ID_,
        Aday_Sonuclar_Tablosu.Aday_Oy_Sayisi == Aday_Oy_Sayisi
    ))

    async with AsyncSessionLocal() as session:
        execute = await session.execute(stmt)

        aday_sonuclara_daha_once_kayit_edildi_mi = execute.scalar_one_or_none()

        if aday_sonuclara_daha_once_kayit_edildi_mi:
            print(f"Aday sonuclara bu değer daha önce kayıt edildi ve ID değeri dönecek : {aday_sonuclara_daha_once_kayit_edildi_mi}")
            return aday_sonuclara_daha_once_kayit_edildi_mi
        
        else:
            new_instance = Aday_Sonuclar_Tablosu()
            new_instance.Aday_ID = Aday_ID
            new_instance.Secim_ID = Secim_ID
            new_instance.Aday_Oy_Sayisi = Aday_Oy_Sayisi
            new_instance.Secim_ID = Secim_ID
            new_instance.Cografya_Kutuphanesi_ID_ = Cografya_Kutuphanesi_ID_
            
            session.add(new_instance)

            await session.commit()

            await session.refresh(new_instance)

            Aday_Sonuclar_ID_degeri = new_instance.ID

            print(f"Aday sonuclar tablosuna yeni bir değer kaydedildi ve ID değeri döndürülecek ID Değreri . {new_instance.ID}")

            return Aday_Sonuclar_ID_degeri


async def Aday_Sonuclar_Tablosundaki_Oy_Oranini_Guncelleme(Aday_Sonucu_ID_değeri : int,Aday_oy_orani : float):
    """
    * Aday_Sonuclar_Tablosundaki_Oy_Oranini_Guncelleme işlemi uygulanacak
    * Belirtilen ID değeri eğer var ise güncelleme işlemi tamamlanacak
    """

    stmt = select(Aday_Sonuclar_Tablosu).filter(Aday_Sonuclar_Tablosu.ID == Aday_Sonucu_ID_değeri)

    async with AsyncSessionLocal() as session:
        execute = await session.execute(stmt)

        nesne_var_mi = execute.scalar_one_or_none()

        if nesne_var_mi:
            nesne_var_mi.Aday_Oy_Orani = Aday_oy_orani

            await session.commit()

            print(f"Aday oy orani güncellendi")
            