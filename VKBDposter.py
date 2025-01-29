import requests
import re
import random
from datetime import datetime, timedelta
from config_reader import config

class VKBDposter:
    """Поздравлятель"""

    def __init__(self, UniDate, BD, date_start, date_end):
        """Конструктор"""

        # Получение значений токенов и группы, а также указание версии API
        TOKEN = config.VK_TOKEN.get_secret_value()
        OWNER_ID = config.GROUP_ID_MINUS.get_secret_value()
        GROUP_ID = config.GROUP_ID.get_secret_value()
        V = 5.199

        # Запуск процесса поздравления
        Starter = self.Poster(TOKEN = TOKEN,OWNER_ID = OWNER_ID, GROUP_ID = GROUP_ID, V = V, UniDate = UniDate, BD = BD, date_start = date_start, date_end = date_end)

    #Если придётся грузить из внешнего источника фотки, то нужно доделать эту функцию. Тут пример: https://gist.github.com/trolleway/f3b489f025bab923b8a5e1c9600e3b71
    #Тут метод и описание от вк: https://dev.vk.com/ru/api/upload/wall-photo
    # def Photo_loader(TOKEN, GROUP_ID, V):
    #     PUGet = requests.get('https://api.vk.com/method/photos.getWallUploadServer?',
    #                            params={
    #                                'access_token': TOKEN,
    #                                'group_id': GROUP_ID,
    #                                'v': V
    #                            }).json()
    #     Url_Response = PUGet['response']['upload_url']
    #
    #     PULoad = requests.post(Url_Response, files=pic.jpg)
    #
    #     return Url_Response

    def Albumination(self, TOKEN, OWNER_ID, V):
        """Вовзращает owner_id и id для функции поиска фото"""

        # Сам метод
        Album = requests.get('https://api.vk.com/method/photos.getAlbums?',
                             params={
                                 'access_token': TOKEN,
                                 'owner_id': OWNER_ID,
                                 'v': V
                             }).json()

        # Поиск альбома с конкретным названием
        AlbumBDay = [item for item in Album['response']['items'] if item.get('title') == 'ДеньРождения']

        # Сохранение только owner_id и id
        AlbumrespDict = [{'owner_id': item.get('owner_id'), 'id': item.get('id')} for item in AlbumBDay]

        # Использование первого результата из списка, если появятся альбомы со схожим названием
        Albumresp = AlbumrespDict[0]
        return Albumresp

    def RandPhoto(self, TOKEN, V, Album_Data):
        """Возвращает случайное фото для прикрепления к посту"""

        # Получаем все фотографии из альбома
        Photer = requests.get('https://api.vk.com/method/photos.get?',
                              params={
                                  'access_token': TOKEN,
                                  'owner_id': Album_Data['owner_id'],
                                  'album_id': Album_Data['id'],
                                  'v': V
                              }).json()

        # Получаем общее количество фотографий для задания границы генерации рандомизатора (-1, потому что от 0)
        Photo_Count = Photer['response']['count'] - 1

        # Создаём список для рандомайзера
        Attach = []

        # Загоняем нужные поля в список, представляем их в виде, читаемом вк (подробнее в самом методе)
        for item in Photer['response']['items']:
            Attach.append(f"photo{item['owner_id']}_{item['id']}")

        # Генерируем случайное значение
        Random_Photo_Value = random.randint(0,Photo_Count)

        # Выбираем случайную фотку
        Random_Photo = Attach[Random_Photo_Value]

        return Random_Photo

    def Get_BD(self, TOKEN, GROUP_ID, V, BD, date_start, date_end):
        """Получение списка именинников, форматирование сообщения в соответствии со списком"""

        #Обработка пустого значения для значения по умолчанию
        if BD == None:
            BD = datetime.now().strftime("%#d.%#m")
            print(str(BD))

        offset = 0
        count = 1001 #Должен быть задан до перебора
        BDsItems = []
        while offset < count:
            # Получаем полный список пользователей группы
            BDs = requests.get('https://api.vk.com/method/groups.getMembers?',
                               params={
                                   'access_token': TOKEN,
                                   'group_id': GROUP_ID,
                                   'offset': offset,
                                   'fields': 'bdate',
                                   'v': V
                               }).json()
            count = BDs['response']['count']
            offset += 1000
            # Срезаем лишнее из ответа от ВК
            BDsItems.extend(BDs['response']['items'])

        # Пустой словарь для людей
        People_Dict = []
        n = 1 #Счётчик
        # Перебор для получения только интереусющих данных
        for item in BDsItems:
            #Если у пользователя полная дата: 1.1.1111
            if 'bdate' in item and item['bdate'][:-5] == BD:
                BDsItem = {
                    'n': n,
                    'id': item['id'],
                    'bdate': item['bdate'],
                    'name': item['first_name'],
                    'surname': item['last_name']
                }

                n += 1
                People_Dict.append(BDsItem)
            #Если у пользователя скрыт год: 1.1
            elif 'bdate' in item and item['bdate'] == str(BD):
                BDsItem = {
                    'n': n,
                    'id': item['id'],
                    'bdate': item['bdate'],
                    'name': item['first_name'],
                    'surname': item['last_name']
                }

                n += 1
                People_Dict.append(BDsItem)

        # Пустая строка для части сообщения с перечислением людей
        people = ""

        # Часть сообщения с перечислением людей
        for hooman in People_Dict:
            # Точка для последнего в перечислении
            if hooman['n'] == n-1:
                Message_People_Item = f"*ffid{hooman['id']} ({hooman['name']} {hooman['surname']}). "
                people += Message_People_Item
            else:
                Message_People_Item = f"*ffid{hooman['id']} ({hooman['name']} {hooman['surname']}), "
                people += Message_People_Item

        #Задаём параметры даты начала скидки и даты окончания скидки
        if date_start != None:
            pass
        #Если дата начала пустая
        else:
            date_starter = datetime.now()
            date_start = date_starter.strftime("%d.%m")
            date_ender = date_starter + timedelta(days=7)
            date_end = date_ender.strftime("%d.%m")

        #Аргументы для подстановки в текст из текстового файла
        arguments = {
            "people": people,
            "date_start": date_start,
            "date_end": date_end
        }

        # Само сообщение.
        if People_Dict[0:]:
            print(People_Dict)
            with open("hint.txt", 'r', encoding='utf8') as Text_msg:
                Messager = Text_msg.read()
                #Функция подстановки аргументов
                def argument_replacement(match):
                    arg_name = match.group(1)
                    if arg_name in arguments:
                        return str(arguments[arg_name])
                    else:
                        raise ValueError(f"Аргумент '{arg_name}' не найден в словаре аргументов")

                try:
                    # Проводим замену с помощью re.sub()
                    Message = re.sub(r'\{([^}]+)\}', argument_replacement, Messager)
                    return Message
                except ValueError as e:
                    raise ValueError(f"Ошибка подстановки аргументов: {e}")

        else:
            #Возвращаем ошибку в UI пользователю
            raise ValueError("Некого поздравлять  :С")

        return Message

    def Poster(self, TOKEN, OWNER_ID, GROUP_ID, V, UniDate, BD, date_start, date_end):
        """Функция отправки поста в группу"""

        # Получение альбома
        Album_Data = self.Albumination(TOKEN = TOKEN, OWNER_ID = OWNER_ID, V = V)

        # Получение фото
        ATTACHMENTS = self.RandPhoto(TOKEN = TOKEN, V = V, Album_Data = Album_Data)

        # Генерация сообщения
        MESSAGE = self.Get_BD(TOKEN = TOKEN, V = V, GROUP_ID = GROUP_ID, BD = BD, date_start= date_start, date_end = date_end)

        # Генерация даты отложенного поста
        if UniDate:
            PUBLISHING_DATE = UniDate #self.get_unix_timestamp_plus_one_hour()
        else:
            PUBLISHING_DATE = ''

        # Часть функции для загрузки из внешнего источника
        #Upload_Link = Photo_loader(TOKEN = TOKEN, GROUP_ID = GROUP_ID, V = V)

        # Сам метод отправки поста
        B_Data = requests.get('https://api.vk.com/method/wall.post?',
                              params={
                                  'access_token':TOKEN,
                                  'owner_id': OWNER_ID,
                                  'from_group': 1,
                                  'message': MESSAGE,
                                  'attachments': ATTACHMENTS,
                                  'publish_date': PUBLISHING_DATE,
                                  'v': V
                              })

        print(B_Data.text)

if __name__ == "__main__":

    Poster = VKBDposter(UniDate=None, BD = None, date_start= None, date_end=None)