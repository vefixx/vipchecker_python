import pytesseract
import cv2
import json


data = []

def getPlayers(img_source):
    with open(r'config/tesseract.json', 'r') as file:
        tesseract = json.load(file)
    pytesseract.pytesseract.tesseract_cmd = f'{tesseract["tesseract"]}'

    img = cv2.imread(img_source)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(img, config=config, lang='eng')

    lines = text.strip().split("\n")  # Разделяем исходный текст на отдельные строки

    players = []  # Список, в котором будут храниться списки слов для каждой строки

    for line in lines:
        words = line.split()  # Разделяем каждую строку на отдельные слова
        players.append(words)  # Добавляем список слов в общий список

    return players


def main(previous_players):
    players = previous_players.copy()  # Создаем копию предыдущего списка

    # Проверка 6 раз
    for i in range(3):
        current_players = getPlayers('test.png')
        if current_players != previous_players:
            players = current_players
            previous_players = current_players
            print('перезапись')

    for list_player in players:
        if len(list_player) >= 2:
            player_nickname = list_player[1]
            data_dict = {'nick': player_nickname}
            data.append(data_dict)

    with open('playersNicknames.json', 'w') as file:
        json.dump(data, file)


def getSettings():
    with open('config/settings.json', 'r') as file:
        data = json.load(file)

    return data


if __name__ == '__main__':
    main(getPlayers('test.png'))
