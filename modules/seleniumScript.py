from modules.imports import *
import json


def check_nickname(nickname):
    pattern = r"[*&%$^+\-@'()/?\\|]"
    if re.search(pattern, nickname):
        return False
    else:
        return True


def main():
    countFoundPasswords = 0
    chrome_options = Options()

    settings = modules.mainfile.getSettings()
    headless = settings['headless']

    if headless == 'False':
        print('У вас выключен headless. Это может вызвать проблемы. (Прочитать о проблемах можно в README.txt)'
              ' Вы можете включить его в настройках поставив значение "True"')
    elif headless == 'True':
        chrome_options.add_argument("--headless")

    s = Service(executable_path=r'ChromiumDriver/chromedriver.exe')
    driver = webdriver.Chrome(service=s, chrome_options=chrome_options)

    # Получаем всех игроков со скриншота
    modules.mainfile.main(modules.mainfile.getPlayers('test.png'))

    def addCookie():
        # Открываем JSON-файл
        with open('config/cookies.json', 'r') as file:
            data = json.load(file)

        # Извлекаем значение "cookie" из данных
        cookie_value = data["cookie"]

        # Разделяем значение "cookie" на отдельные куки
        cookie_list = cookie_value.split("; ")

        # Создаем список словарей с куками
        cookies = []
        for cookie_str in cookie_list:
            name, value = cookie_str.split("=", 1)
            cookie = {"name": name.strip(), "value": value.strip()}
            cookies.append(cookie)

        # Выводим список кук
        for cookie in cookies:
            driver.add_cookie(cookie)

        # После добавления кук, обновите страницу или перейдите на другую страницу
        driver.refresh()

    def wait_for_element(driver, selector, timeout=10):
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            return element
        except TimeoutException:
            print(f"Элемент с селектором '{selector}' не появился в течение {timeout} секунд")
            return None

    # Загрузка JSON файла
    with open('playersNicknames.json', 'r') as json_file:
        nicknames_data = json.load(json_file)

    # Получение значения поля "nick" для каждого объекта в списке
    nicknames = [item['nick'] for item in nicknames_data]

    # Загрузка данных из файла JSON
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    try:
        driver.maximize_window()
        driver.get('https://vipchecker.ru/')

        addCookie()

        driver.get('https://vipchecker.ru/vip-checker')
        # первый никнейм
        if nicknames:

            first_nickname = nicknames[0]
            if len(first_nickname) > 3 and check_nickname(first_nickname):

                input_nickname = wait_for_element(driver,
                                                  timeout=5,
                                                  selector='body > div > div.page-wrapper > div > div:nth-child(2) > div > div.panel-wrapper.collapse.in > div > form > center > input')

                if input_nickname:
                    input_element = driver.find_element(by=By.CSS_SELECTOR,
                                                        value='body > div > div.page-wrapper > div > div:nth-child(2) > div > div.panel-wrapper.collapse.in > div > form > center > input')
                    input_element.clear()
                    input_element.send_keys(first_nickname)

                buttonCheck = driver.find_element(by=By.CSS_SELECTOR,
                                                  value='body > div > div.page-wrapper > div > div:nth-child(2) > div > div.panel-wrapper.collapse.in > div > form > center > button')
                buttonCheck.click()
                time.sleep(1)

                tr_elements = driver.find_elements(by=By.CSS_SELECTOR,
                                                   value='body > div > div.page-wrapper > div > div:nth-child(6) > div > div > table > tbody > tr')

                if tr_elements:
                    tr_elements = driver.find_elements(by=By.XPATH,
                                                       value='/html/body/div/div[2]/div/div[3]/div/div/table/tbody/tr')
                else:
                    tr_elements = driver.find_elements(by=By.CSS_SELECTOR,
                                                       value='body > div > div.page-wrapper > div > div:nth-child(5) > div > div > table > tbody > tr')

                count = 0
                for tr in tr_elements:

                    if count > 0:
                        td_elements_into_tr = tr.find_elements(by=By.TAG_NAME, value='td')
                        if len(td_elements_into_tr) >= 6:
                            password = td_elements_into_tr[1]
                            server = td_elements_into_tr[5]
                            try:
                                input_element = password.find_element(by=By.TAG_NAME, value="input")
                                password_text = input_element.get_property('value')
                                server_text = server.text

                                if len(password_text) > 0:  # Проверка наличия пароля
                                    data_dict = {'nick': first_nickname, 'password': password_text,
                                                 'server': server_text}
                                    data.append(data_dict)
                            except:
                                pass
                    else:
                        count += 1

                count = 0
                print(data)
                print(first_nickname)
            else:
                print('Никнейм меньше 4 символов')
                input_nickname = wait_for_element(driver,
                                                  timeout=5,
                                                  selector='body > div > div.page-wrapper > div > div:nth-child(2) > div > div.panel-wrapper.collapse.in > div > form > center > input')

                if input_nickname:
                    input_element = driver.find_element(by=By.CSS_SELECTOR,
                                                        value='body > div > div.page-wrapper > div > div:nth-child(2) > div > div.panel-wrapper.collapse.in > div > form > center > input')
                    input_element.clear()
                    input_element.send_keys('nonefound')
                print('test')
                buttonCheck = driver.find_element(by=By.CSS_SELECTOR,
                                                  value='body > div > div.page-wrapper > div > div:nth-child(2) > div > div.panel-wrapper.collapse.in > div > form > center > button')
                print('test232323232')
                buttonCheck.click()
                time.sleep(1)
                print(first_nickname, data)

        # Начало цикла для проверки всех оставшихся пользователей, не включая первый
        if len(nicknames) > 1:
            for nickname in nicknames[1:]:
                time.sleep(11)
                if len(nickname) > 3 and check_nickname(nickname):
                    # Основное условие, дальше идем по автоматизации этих ников в поле ввода
                    input_nickname = driver.find_element(by=By.CSS_SELECTOR,
                                                         value='body > div > div.page-wrapper > div > div:nth-child(3) > div > div.panel-wrapper.collapse.in > div > form > center > input')
                    input_nickname.clear()
                    input_nickname.send_keys(str(nickname))
                    button_check = driver.find_element(by=By.CSS_SELECTOR,
                                                       value='body > div > div.page-wrapper > div > div:nth-child(3) > div > div.panel-wrapper.collapse.in > div > form > center > button')

                    button_check.click()

                    tr_elements = driver.find_elements(by=By.CSS_SELECTOR,
                                                       value='body > div > div.page-wrapper > div > div:nth-child(5) > div > div > table > tbody > tr')

                    if tr_elements:
                        tr_elements = driver.find_elements(by=By.XPATH,
                                                           value='/html/body/div/div[2]/div/div[3]/div/div/table/tbody/tr')
                    else:
                        tr_elements = driver.find_elements(by=By.CSS_SELECTOR,
                                                           value='body > div > div.page-wrapper > div > div:nth-child(6) > div > div > table > tbody > tr')

                    count2 = 0
                    for tr in tr_elements:
                        if count2 > 0:
                            td_elements_into_tr = tr.find_elements(by=By.TAG_NAME, value='td')
                            if len(td_elements_into_tr) >= 6:
                                password = td_elements_into_tr[1]
                                server = td_elements_into_tr[5]

                                try:
                                    input_element = password.find_element(by=By.TAG_NAME, value="input")
                                    password_text = input_element.get_property('value')
                                    server_text = server.text

                                    if len(password_text) > 0:  # Проверка наличия пароля
                                        countFoundPasswords += 1
                                        data_dict = {'nick': nickname, 'password': password_text, 'server': server_text}
                                        data.append(data_dict)
                                except:
                                    pass
                        else:
                            count2 += 1

                    print(Fore.YELLOW + f'По нику {nickname} было найдено {countFoundPasswords} паролей' + Style.RESET_ALL)
                    countFoundPasswords = 0

        with open('data.json', 'w') as file:
            json.dump(data, file)

        modules.parsepasswords.main()
    except Exception as ex:
        print('Основная ошибка:', ex)

    finally:
        os.remove('data.json')
        os.remove('playersNicknames.json')
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
