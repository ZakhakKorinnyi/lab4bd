from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Weather, Wind

# Підключення до бази даних
engine = create_engine('mysql+pymysql://root:@localhost/weather_db')
Session = sessionmaker(bind=engine)
session = Session()

def clear_database():
    session.query(Wind).delete()
    session.query(Weather).delete()
    session.commit()

def save_record(weather_record):
    session.add(weather_record)

def commit_changes():
    session.commit()

def get_recent_weather():
    return session.query(Weather).limit(10).all()

def search_by_country_and_date(search_country, date_obj):
    return session.query(Weather).filter(
        Weather.country.ilike(f"%{search_country}%"),
        Weather.last_updated == date_obj
    ).all()