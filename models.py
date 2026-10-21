from sqlalchemy import Column, Integer, String, Float, Enum, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class WindDirectionEnum(enum.Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"
    NE = "NE"
    NW = "NW"
    SE = "SE"
    SW = "SW"

class Wind(Base):
    __tablename__ = 'wind_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(Integer, ForeignKey('weather_data.id'), unique=True)
    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_direction = Column(Enum(WindDirectionEnum))
    is_safe_to_go_out = Column(Boolean, nullable=True) # <-- Тепер колонка тут

    weather = relationship("Weather", back_populates="wind")

class Weather(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(255), nullable=False)
    last_updated = Column(Date)
    sunrise = Column(Time)
    

    wind = relationship("Wind", back_populates="weather", cascade="all, delete-orphan", uselist=False)