from datetime import datetime

date1_str = input("Введите первую дату (ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")
date2_str = input("Введите вторую дату (ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")

try:

    date1 = datetime.strptime(date1_str, "%Y-%m-%d %H:%M:%S")
    date2 = datetime.strptime(date2_str, "%Y-%m-%d %H:%M:%S")
    
    
    difference = (date1 - date2).total_seconds()
    
    print(f"Разница в секундах: {difference}")
except ValueError as e:
    print(f"Ошибка: {e}. Пожалуйста, вводите даты в правильном формате.")