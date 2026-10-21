import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Weather, Wind, WindDirectionEnum

# Підключення до бази даних
engine = create_engine('postgresql+psycopg2://postgres:12345@localhost/weather_db')
Session = sessionmaker(bind=engine)
session = Session()

def map_wind_direction(direction_str):
    """
    Перетворює 16-точкову розу вітрів з Kaggle (наприклад, NNE, WSW) 
    на нашу 8-точкову, яка задана в Enum.
    """
    mapping = {
        'N': 'N', 'S': 'S', 'E': 'E', 'W': 'W',
        'NE': 'NE', 'NNE': 'NE', 'ENE': 'NE',
        'NW': 'NW', 'NNW': 'NW', 'WNW': 'NW',
        'SE': 'SE', 'SSE': 'SE', 'ESE': 'SE',
        'SW': 'SW', 'SSW': 'SW', 'WSW': 'SW'
    }
    return mapping.get(direction_str.upper(), 'N')

def load_data():
    print("Очищення старих даних...")
    session.query(Wind).delete()
    session.query(Weather).delete()
    session.commit()

    print("Завантаження даних з CSV (перші 100 записів)...")
    count = 0
    with open('weather.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if count >= 100:  # 100 рядків, щоб база не зависала при 13 тисячах
                break
            
            # Форматування дати та часу
            date_str = row['last_updated'].split()[0]  # Відкидаємо час, залишаємо лише дату
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_obj = datetime.strptime(row['sunrise'], '%I:%M %p').time()
            
            # Чи безпечно виходити на вулицю?
            wind_speed = float(row['wind_kph'])
            is_safe = wind_speed < 12.0

            # Створення основної таблиці
            weather = Weather(
                country=row['country'],
                last_updated=date_obj,
                sunrise=time_obj,
                is_safe_to_go_out=is_safe
            )
            
            # Створення пов'язаної таблиці вітру
            wind = Wind(
                wind_degree=int(row['wind_degree']),
                wind_kph=wind_speed,
                wind_direction=WindDirectionEnum[map_wind_direction(row['wind_direction'])]
            )
            
            # Зв'язуємо один до одного і додаємо
            weather.wind = wind
            session.add(weather)
            count += 1
            
    session.commit()
    print(f" Успішно збережено {count} записів у базу даних!\n")

def show_data():
    records = session.query(Weather).limit(10).all()
    print("\n--- Останні 10 записів з БД ---")
    for w in records:
        safe_icon = " Можна гуляти" if w.is_safe_to_go_out else " Сильний вітер"
        print(f"{w.country} | Вітер: {w.wind.wind_kph} км/год ({w.wind.wind_direction.value}) | {safe_icon}")
    print("-------------------------------\n")

def menu():
    while True:
        print("=== КОНСОЛЬНЕ МЕНЮ ===")
        print("1. Завантажити дані з CSV в базу")
        print("2. Вивести дані на екран")
        print("3. Вихід")
        choice = input("Оберіть дію (1-3): ")
        
        if choice == '1':
            load_data()
        elif choice == '2':
            show_data()
        elif choice == '3':
            print("Вихід з програми...")
            break
        else:
            print("Невірна команда.\n")

if __name__ == '__main__':
    menu()