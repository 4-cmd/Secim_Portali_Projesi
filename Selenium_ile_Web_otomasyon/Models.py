from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,Text,ForeignKey,DateTime,FLOAT
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from Pydantic_Page import py_settings_variable
from datetime import datetime


hours_minutes_seconds = datetime.now()


database_url = py_settings_variable.DATABASE_URL_STR

class Base(AsyncAttrs,DeclarativeBase):
    pass

class Cografya_Kutuphanesi(Base):
    __tablename__ = "Cografya_Kutuphanesi"
    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Tanım : Mapped[str] = mapped_column(String, nullable=True)
    UST_ID: Mapped[int] = mapped_column(Integer, nullable=True)
    Plaka_numarasi : Mapped[int] = mapped_column(Integer,nullable=True)
    


    # İlişki: Bir coğrafya birimine ait birçok sonuç olabilir
    aday_sonuclari: Mapped[list["Aday_Sonuclar_Tablosu"]] = relationship("Aday_Sonuclar_Tablosu", back_populates="cografya_birimi")
    parti_sonuclari : Mapped[list["Parti_Sonuclari_Tablosu"]] = relationship("Parti_Sonuclari_Tablosu",back_populates="Cografya_Kutuphanesi_One")
    secim_genel_bilgiler : Mapped[list["Secim_Genel_Bilgiler"]] = relationship("Secim_Genel_Bilgiler",back_populates="Cografya_Kutuphanesi_One")



class Partiler(Base):
    __tablename__ = "Partiler"
    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Parti_ismi: Mapped[str] = mapped_column(Text, nullable=True)

    Parti_Sonuclari : Mapped[list["Parti_Sonuclari_Tablosu"]] = relationship("Parti_Sonuclari_Tablosu",back_populates="Parti_Sonuclari_Tablo_One")

class Secimler(Base):
    __tablename__ = "Secimler"
    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Secim_ismi: Mapped[str] = mapped_column(String, nullable=True)
    
    aday_sonuclari: Mapped[list["Aday_Sonuclar_Tablosu"]] = relationship("Aday_Sonuclar_Tablosu", back_populates="secim",cascade="all, delete",passive_deletes=True)

    parti_sonuclari : Mapped[list["Parti_Sonuclari_Tablosu"]] = relationship("Parti_Sonuclari_Tablosu",back_populates="Parti_Sonuclari_Secimi",cascade="all, delete",passive_deletes=True)

    secim_genel_bilgiler : Mapped[list["Secim_Genel_Bilgiler"]] = relationship("Secim_Genel_Bilgiler",back_populates="secim_genel_bilgiler_one",cascade="all, delete",passive_deletes=True)



class Adaylar(Base):
    __tablename__ = "Adaylar"
    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Aday_ismi: Mapped[str] = mapped_column(String, nullable=True)

    aday_sonuclari: Mapped[list["Aday_Sonuclar_Tablosu"]] = relationship("Aday_Sonuclar_Tablosu", back_populates="aday")

class Aday_Sonuclar_Tablosu(Base):
    __tablename__ = "Aday_Sonuclar_Tablosu"
    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    Secim_ID: Mapped[int] = mapped_column(ForeignKey("Secimler.ID",ondelete="CASCADE"))
    secim: Mapped["Secimler"] = relationship("Secimler", back_populates="aday_sonuclari")

    Aday_ID: Mapped[int] = mapped_column(ForeignKey("Adaylar.ID"))
    aday: Mapped["Adaylar"] = relationship("Adaylar", back_populates="aday_sonuclari")

    Cografya_Kutuphanesi_ID_: Mapped[int] = mapped_column(ForeignKey("Cografya_Kutuphanesi.ID"))
    cografya_birimi: Mapped["Cografya_Kutuphanesi"] = relationship("Cografya_Kutuphanesi", back_populates="aday_sonuclari")

    Aday_Oy_Sayisi : Mapped[int] = mapped_column(Integer,nullable=True)
    Aday_Oy_Orani : Mapped[float] = mapped_column(FLOAT,nullable=True)
    


class Parti_Sonuclari_Tablosu(Base):
    __tablename__ = "Parti_Sonuclari_Tablosu"
    ID : Mapped[int] = mapped_column(Integer,primary_key=True)
    
    Secim_ID : Mapped[int] = mapped_column(ForeignKey("Secimler.ID",ondelete="CASCADE"))
    Parti_Sonuclari_Secimi : Mapped["Secimler"] = relationship("Secimler",back_populates="parti_sonuclari")

    Parti_ID : Mapped[int] = mapped_column(ForeignKey("Partiler.ID"))
    Parti_Sonuclari_Tablo_One : Mapped["Partiler"] = relationship("Partiler",back_populates="Parti_Sonuclari")

    Cografya_Kutuphanesi_ID : Mapped[int] = mapped_column(ForeignKey("Cografya_Kutuphanesi.ID"))
    Cografya_Kutuphanesi_One : Mapped["Cografya_Kutuphanesi"] = relationship("Cografya_Kutuphanesi", back_populates="parti_sonuclari")

    Parti_Oy_Sayisi : Mapped[int] = mapped_column(Integer,nullable=True)
    Parti_Oy_Orani : Mapped[float] = mapped_column(FLOAT,nullable=True)

    varsayilan_yaratilma_tarihi : Mapped[datetime] = mapped_column(DateTime,default=hours_minutes_seconds)

    # Cografya_Kutuphanesi_One


class Secim_Genel_Bilgiler(Base):
    __tablename__ = "Secim_Genel_Bilgiler"
    ID : Mapped[int] = mapped_column(Integer,primary_key=True)

    Kayitli_Secmen_Sayisi : Mapped[int] = mapped_column(Integer,nullable=True)
    Oy_Kullanan_Secmen_Sayisi : Mapped[int] = mapped_column(Integer,nullable=True)
    Gecerli_Oy_Sayisi : Mapped[int] = mapped_column(Integer,nullable=True)

    Cografya_Kutuphanesi_ID : Mapped[int] = mapped_column(ForeignKey("Cografya_Kutuphanesi.ID"))
    Cografya_Kutuphanesi_One :  Mapped["Cografya_Kutuphanesi"] = relationship("Cografya_Kutuphanesi", back_populates="secim_genel_bilgiler")

    Secim_ID : Mapped[int] = mapped_column(ForeignKey("Secimler.ID",ondelete="CASCADE"))
    secim_genel_bilgiler_one : Mapped["Secimler"] = relationship("Secimler",back_populates="secim_genel_bilgiler")



engine = create_async_engine(database_url,echo = True)
async def tablolari_yarat():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            print(f"Veritabanında var olan tabloların isimleri : {Base.metadata.tables.keys()}") 
        
        except Exception as Hata:
            print(f"Hata : {Hata}")
        

asyncio.run(tablolari_yarat())

