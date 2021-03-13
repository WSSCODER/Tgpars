import time
import json
from pyrogram import Client
from pyrogram.errors import FloodWait

app = Client('session', workdir='./session')  # Настройки сессии клиента
chat = 'BinanceRussian'  # Название чата или его ID
string_format = '{id}\n'  # Формат строки для записи

def parser(id):
    """ Функция парсинга пользователей """

    members = []
    offset = 0
    limit = 200
    while True:
        try:
            chunk = app.get_chat_members(id, offset)
            print(chunk)           

        except FloodWait as e:
            time.sleep(e.x)
            continue

        if not chunk:
            break

        members.extend(chunk)
        offset += len(chunk)
    return members

def template(data, template):
    """ Функция нормализатора строк """

    data = json.loads(str(data))
    data['user'].setdefault('first_name', '-')
    data['user'].setdefault('last_name', '-')
    data['user'].setdefault('username', '-')
    data['user'].setdefault('phone_number', '-')
    return template.format(id=data['user']['id'],
                           first_name=data['user']['first_name'],
                           last_name=data['user']['last_name'],
                           username= '@'+data['user']['username'],
                           phone_number=data['user']['phone_number'],
                           status=data['status'])

def wfile(data, template_format, path):
    """ Функция записи строк в файл """

    with open(path, 'w', encoding='utf8') as file:
        #file.writelines('Количество пользователей: {0}\n\n'.format(len(data)))
        file.writelines([template(user, template_format) for user in data])
        
def main():
    with app:
        data = parser(chat)
        wfile(data, string_format, './chats/{0}.txt'.format(chat))
        #text = '''ПРИВЕТ'''
        #Отправка сообщений пользователям, но меня быстро банили, возможно из-за того, что акк свежий   
        '''
        mess=0
        f = open("chats/{0}.txt".format(chat))  # Чтение из файла построчно
        line = f.readline()
        while line:
            try:
                app.send_message(int(line), text)
                mess +=1
                print ('Отправил сообщений: {mess}, последнее для {line}'.format (mess=mess, line=line))
                line = f.readline()
                time.sleep(1)

            except FloodWait as e:
                time.sleep(e.x)
                continue

        f.close()
        '''
        print('Сбор данных закончен!')
        
if __name__ == '__main__':

    main()
