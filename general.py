import modules.seleniumScript
import os
from colorama import Fore, Style

#запус основного скрипта

username = ''
def init():
    global username

    if os.path.exists('readyData') and os.path.isdir('readyData'):
        print('good')
    else:
        print(Fore.RED + 'ВНИМАНИЕ! У вас нет в директории папки readyData. Создайте ее' + Style.RESET_ALL)
        return False

    if os.path.exists('test.png'):
        print('good 2')
    else:
        print(Fore.RED + 'Не найден скриншот с табом!!' + Style.RESET_ALL)
        return False

def info():
    from art import text2art
    ascii_art = text2art("vefixx")
    print(Fore.RED + "Hello World!" + Style.RESET_ALL)

    # Вывод ASCII-арта
    print(ascii_art)

    username = os.getlogin()
    print(f'Привет, {username}!')

def main():
    info()
    print(Fore.GREEN + 'Инициализируем все скрипты.. Это может занять несколько секунд')
    try:
        if init() == False:
            exit()

        print('Готово! Все скрипты были успешно добавлены!')
        print('Запускаем главный скрипт и начинаем работу..')
        modules.seleniumScript.main()
    except Exception as ex:
        print(Fore.RED + f'Произошла ошибка при загрузке файлов! {ex}' + Style.RESET_ALL)



if __name__ == '__main__':
    main()

    #input(Style.RESET_ALL + 'press enter')
