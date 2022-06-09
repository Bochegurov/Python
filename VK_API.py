# coding: utf-8
import  json
import requests
import sqlite3


def get_json(url, data=None):
    result = requests.get(url=url, params=data)
    result = result.json()
    with open('vk_bade.json', 'w') as opened_file:
        json.dump(result, opened_file, indent=4, ensure_ascii=False)


def get_id_info():
    id_prof = input("Введите id профиля ")
    access_token = input("Введите access token профиля ")
    url = "https://api.vk.com/method/friends.get?user_id=" + str(id_prof.strip()) + "&access_token=" + str(
         access_token.strip()) + "&fields=bdate,sex&v=5.131"

    return url


def create_bd():
    try:
        check_db = open('VK_database.db', 'r')
        check_db.close()
    except FileNotFoundError:
        sqlite_connection = sqlite3.connect('VK_database.db')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        cursor.execute('''create table VK_database(id text, name text, surname text, sex text, birthday text)''')

def input_bd():
    with open('vk_bade.json', 'r') as opened_file:
        policy = json.load(opened_file)
    connection = sqlite3.connect('VK_database.db')
    cursor = connection.cursor()
    try:
        for line in policy['response']['items']:
            try:
                line['bdate']
            except KeyError:
                cursor.execute(
                    "insert into VK_database(id,name,surname,sex,birthday) values('%s','%s','%s','%s','%s')" % (
                        line["id"],
                        line["first_name"],
                        line["last_name"],
                        line['sex'],
                        '------'))
            else:
                cursor.execute(
                    "insert into VK_database(id,name,surname,sex,birthday) values('%s','%s','%s','%s','%s')" % (
                        line["id"],
                        line["first_name"],
                        line["last_name"],
                        line['sex'],
                        line['bdate']))
    except KeyError:
        print("Не верный access token или id пользователя не совпадает с access token ")
    connection.commit()


if __name__ == "__main__":
    url = get_id_info()
    get_json(url)
    create_bd()
    input_bd()