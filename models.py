from sqlalchemy import Column, Integer, String, Float, Enum, Date, Time
from sqlalchemy.orm import declarative_base
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

class Weather(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    last_updated = Column(Date)
    sunrise = Column(Time)
    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_direction = Column(Enum(WindDirectionEnum))