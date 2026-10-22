import csv
from datetime import datetime
import repository
from models import Weather, Wind, WindDirectionEnum

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

def clear_old_data():
    repository.clear_database()

def process_and_load_csv():
    count = 0
    with open('weather.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if count >= 100:  # 100 рядків, щоб база не зависала при 13 тисячах
                break
            
            # Форматування дати та часу
            date_str = row['last_updated'].split()[0] 
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_obj = datetime.strptime(row['sunrise'], '%I:%M %p').time()
            
            # Чи безпечно виходити на вулицю?
            wind_speed = float(row['wind_kph'])
            is_safe = wind_speed < 12.0

            # Створення основної таблиці
            weather = Weather(
                country=row['country'],
                last_updated=date_obj,
                sunrise=time_obj
            )
            
            # 4. Створення таблиці вітру
            wind = Wind(
                wind_degree=int(row['wind_degree']),
                wind_kph=wind_speed,
                wind_direction=WindDirectionEnum[map_wind_direction(row['wind_direction'])],
                is_safe_to_go_out=is_safe 
            )
            
            # Зв'язуємо один до одного і додаємо
            weather.wind = wind
            repository.save_record(weather)
            count += 1
            
    repository.commit_changes()
    return count

def get_data_for_show():
    return repository.get_recent_weather()

def search_weather_logic(search_country, date_obj):
    return repository.search_by_country_and_date(search_country, date_obj)