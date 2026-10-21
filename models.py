from sqlalchemy import Column, Integer, String, Float, Enum, Date, Time, ForeignKey
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

# Нова таблиця для категорії "Вітер"
class Wind(Base):
    __tablename__ = 'wind_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(Integer, ForeignKey('weather_data.id'), unique=True) # Зв'язок з основною таблицею
    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_direction = Column(Enum(WindDirectionEnum))

    # Налаштування зв'язку для зручного доступу з коду
    weather = relationship("Weather", back_populates="wind")

# Оновлена основна таблиця (без колонок вітру)
class Weather(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    last_updated = Column(Date)
    sunrise = Column(Time)

    # Налаштування зв'язку з новою таблицею вітру
    wind = relationship("Wind", back_populates="weather", cascade="all, delete-orphan", uselist=False)