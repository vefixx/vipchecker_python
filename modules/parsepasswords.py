import json
import random
from random import randint

#Парсинг ников
def main():
    with open('playersNicknames.json', 'r') as json_file:
        data = json.load(json_file)

    nicknames = [item['nick'] for item in data]

    # Парсинг паролей

    # Чтение данных из файла JSON
    with open('data.json', 'r') as file:
        data = json.load(file)

    with open(rf'readyData\data{str(random.randint(1,999))}.txt', 'w') as file:
        for nickname in nicknames:
            filtered_data = [entry for entry in data if entry["nick"] == nickname]

            if filtered_data:  # Проверка наличия паролей для данного никнейма
                passwords_set = set(entry["password"] for entry in filtered_data)  # Используем set для хранения уникальных паролей
                passwords = ' '.join(passwords_set)
                result = f"{nickname} {passwords}"

                file.write(result + '\n')


    # Парсинг данных, которые имеют DELUXE логи
    with open(rf'readyData\deluxe{randint(0,999)}.txt', 'w') as file:
        for nickname in nicknames:
            filtered_data = [entry for entry in data if entry["server"] == 'DELUXE' and entry["nick"] == nickname]
            passwords = [entry["password"] for entry in filtered_data if entry["password"]]  # Убираем пустые пароли
            if passwords:
                result = f"{nickname} {' '.join(passwords)}"
                file.write(result + '\n')

if __name__ == '__main__':
    main()