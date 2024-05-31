from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# URL de connexion à la base de données SQLite
DATABASE_URL = "sqlite:///../bdd/countries.db"

# Définir la base de données et la session
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Définir le modèle de données pour les continents
class Continent(Base):
    __tablename__ = "continents"

    code = Column(String, primary_key=True, index=True)
    latitude = Column(String)
    longitude = Column(String)
    name = Column(String)
    nameEs = Column(String)
    nameFr = Column(String)

    countries = relationship("Country", back_populates="continent")

# Définir le modèle de données pour les pays
class Country(Base):
    __tablename__ = "countries"

    code = Column(String, primary_key=True, index=True)
    continent_code = Column(String, ForeignKey("continents.code"))
    latitude = Column(String)
    longitude = Column(String)
    name = Column(String)
    nameEs = Column(String)
    nameFr = Column(String)
    nameNative = Column(Text)
    population = Column(Integer)
    pib = Column(Integer, default=0)

    continent = relationship("Continent", back_populates="countries")

class EncryptKey(Base):
    __tablename__ = "encrypt_key"

    key = Column(Text, primary_key=True)