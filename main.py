from flask import Flask, request, render_template
import json
import time
t = time.localtime()
now = time.strftime('%H:%M:%S', t)

application = Flask(__name__)  # создаем Flask-приложение

DB_FILE = "./data/db.json"


# функция чтения сообщений из файла
def load_messages():
    json_file = open(DB_FILE, "r")
    data = json.load(json_file)
    return data["messages"]


all_messages = load_messages() # Список всех сообщний

# функция соханения сообщений в файл
def save_messages():
    data = {
        "messages": all_messages
    }
    json_file = open(DB_FILE, "w")
    json.dump(data, json_file)
    return


@application.route('/')
def index_page():
    return 'Hello, welcome to SkBox Chat'


@application.route('/chat')
def display_chat():
    return render_template('Forms.html')


@application.route('/send_message')
def send_message():
    sender = request.args['name']
    text = request.args['text']
    # получили инфо от пользователя и добавляем сообщение в список

    add_message(sender, text)

    save_messages()
    return 'OK'


@application.route('/get_messages')
def get_messages():
    return {'messages': all_messages}


def add_message(sender, text):
    # 1. Подготовить словарь с данными сообщения
    new_message = {
        "sender": sender,
        "text": text,
        "time": now  # ToDo: здесь должно быть текущее время (это будет д/з). Done
    }
    if (100 >= (len(sender)) >= 3) and (3000 >= (len(text)) >= 1):
        # 2. Добавить полученный словарь в список сообщений
        all_messages.append(new_message)
    else:
        return 'ERROR'


def print_message(message):
    print(f"[{message['sender']}]: {message['text']} / {message['time']}")


for message in all_messages:
    print_message(message)

application.run(host='0.0.0.0', port=80)  # запускаем приложение

