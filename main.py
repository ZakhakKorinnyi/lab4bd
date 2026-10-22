from datetime import datetime
import services

def load_data():
    print("Очищення старих даних...")
    services.clear_old_data()

    print("Завантаження даних з CSV (перші 100 записів)...")
    count = services.process_and_load_csv()
    
    print(f"Успішно збережено {count} записів у базу даних!\n")

def show_data():
    records = services.get_data_for_show()
    print("\n--- Останні 10 записів з БД ---")
    for w in records:
        safe_icon = "Можна гуляти" if w.wind.is_safe_to_go_out else "Сильний вітер"
        print(f"{w.country} ({w.last_updated}) | Вітер: {w.wind.wind_kph} км/год | {safe_icon}")
    print("-------------------------------\n")

def search_weather():
    print("\n--- ПОШУК ПОГОДИ ---")
    search_country = input("Введіть назву країни (наприклад, Ukraine): ").strip()
    search_date = input("Введіть дату у форматі YYYY-MM-DD: ").strip()
    
    try:
        # Форматування введеної дати
        date_obj = datetime.strptime(search_date, '%Y-%m-%d').date()
        
        # Пошук записів у базі за країною та датою
        results = services.search_weather_logic(search_country, date_obj)
        
        if not results:
            print("За вашим запитом нічого не знайдено.\n")
            return
            
        print(f"\nЗнайдено записів: {len(results)}")
        for w in results:
            # Зчитування статусу безпеки
            safe_icon = "Можна гуляти" if w.wind.is_safe_to_go_out else "Сильний вітер, залишайтесь вдома"
            
            # Виведення всієї наявної інформації
            print(f"Країна: {w.country}")
            print(f"Дата оновлення: {w.last_updated}, Схід сонця: {w.sunrise}")
            print(f"Вітер: {w.wind.wind_kph} км/год, Напрямок: {w.wind.wind_direction.value}, Кут: {w.wind.wind_degree}°")
            print(f"Статус: {safe_icon}\n")
            
    except ValueError:
        print("Невірний формат дати! Використовуйте YYYY-MM-DD.\n")

def menu():
    while True:
        print("=== КОНСОЛЬНЕ МЕНЮ ===")
        print("1. Завантажити дані з CSV в базу")
        print("2. Вивести дані на екран")
        print("3. Пошук за країною та датою")
        print("4. Вихід")
        choice = input("Оберіть дію (1-4): ")
        
        if choice == '1':
            load_data()
        elif choice == '2':
            show_data()
        elif choice == '3':
            search_weather()
        elif choice == '4':
            print("Вихід з програми...")
            break
        else:
            print("Невірна команда.\n")

if __name__ == '__main__':
    menu()