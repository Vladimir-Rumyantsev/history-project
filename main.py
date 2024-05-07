import telebot
from telebot import types
import datetime
import time
import os
import random


bot = telebot.TeleBot('token')
users, talks = [], []
developers = [947467861]   # 1968018162


main_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_button.add(types.KeyboardButton('Вернуться в главное меню'))

random_city_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
random_city_button.add(types.KeyboardButton('Выбрать рандомный город'),
                       types.KeyboardButton('Вернуться в главное меню'))

start_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_button.add(types.KeyboardButton('Города'),
                 types.KeyboardButton('Люди'),
                 types.KeyboardButton('Написать в техподдержку'),
                 types.KeyboardButton('Поддержать разработчика'))

cites_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
cites_button.add(types.KeyboardButton('Выбрать определённый город'),
                 types.KeyboardButton('Выбрать рандомный город'),
                 types.KeyboardButton('Вернуться в главное меню'))

people_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
people_button.add(types.KeyboardButton('Узнать об определённом человеке'),
                  types.KeyboardButton('Выбрать случайного человека'),
                  types.KeyboardButton('Вернуться в главное меню'))


def clear_logs():
    with open("logs.txt", "w", encoding="utf-8") as logs_file:
        logs_file.write('')


def write_logs(text):
    with open("logs.txt", "a", encoding="utf-8") as logs_file:
        logs_file.write(f'{text}\n\n')


def read_users():
    try:
        with open('users.txt', 'r', encoding="utf-8") as users_file:
            arr = users_file.readlines()
            for i in arr:
                users.append(int(i))
    except:
        with open("errors.txt", "a", encoding="utf-8") as errors_file:
            errors_file.write(f'{(datetime.datetime.today()).strftime("%d.%m.%Y %H:%M:%S")} '
                              f'-> Была ошибка во время чтения "users.txt"\n\n')


def write_users(chat_id):
    with open("users.txt", "a", encoding="utf-8") as users_file:
        users_file.write(f'{chat_id}\n')


def read_talks():
    try:
        with open('talks.txt', 'r', encoding="utf-8") as talks_file:
            arr = talks_file.readlines()
            for i in arr:
                data = i.strip().split(' -> ')
                result = [int(data[0])]
                history = data[1].strip().split(', ')
                for j in history:
                    result.append(j)
                talks.append(result)
    except:
        with open("errors.txt", "a", encoding="utf-8") as errors_file:
            errors_file.write(f'{(datetime.datetime.today()).strftime("%d.%m.%Y %H:%M:%S")} '
                              f'-> Была ошибка во время чтения "talks.txt"\n\n')


def write_talks():
    with open("talks.txt", "w", encoding="utf-8") as talks_file:
        for i in talks:
            line = f'{i[0]} -> {i[1]}'
            if len(i) > 2:
                for j in i[2:]:
                    line = f'{line}, {j}'
            talks_file.write(f'{line}\n')


def write_errors(chat_id, history, expt):
    ln = len(history)
    if ln > 0:
        with open("errors.txt", "a", encoding="utf-8") as errors_file:
            line = f'{(datetime.datetime.today()).strftime("%d.%m.%Y %H:%M:%S")} -> {chat_id} -> {history[0]}'
            if ln > 1:
                for i in range(1, ln):
                    line = f'{line}, {history[i]}'
            errors_file.write(f'{line}\n{expt}\n\n')
    else:
        with open("errors.txt", "a", encoding="utf-8") as errors_file:
            errors_file.write(f'{(datetime.datetime.today()).strftime("%d.%m.%Y %H:%M:%S")}'
                              f' -> {chat_id} -> None\n{expt}\n\n')


def working(history, chat_id):
    main_menu = ('Главное меню\nТут будет написано много текста\nВы всегда можете воспользоваться командой /start '
                 'или кнопкой "Вернуться в главное меню", чтобы вернуться в главное меню')
    ln = len(history)

    if not history:
        return main_menu


    elif str(history[0]).lower() == 'люди':

        if ln < 2:
            return [False, people_button, 'Выберите режим работы, для этого воспользуйтесь кнопками ниже']

        if str(history[1]).lower() == 'узнать об определённом человеке':
            if ln == 2:
                return [False, main_button, 'Введите Фамилию нужного вам человека']
            return [True, start_button, 'Ещё в разработке', 'Возвращаемся в главное меню', main_menu]

        elif str(history[1]).lower() == 'выбрать случайного человека':
            return [True, start_button, 'Ещё в разработке', 'Возвращаемся в главное меню', main_menu]

        return [True, start_button, 'Возвращаемся в главное меню', main_menu]


    elif str(history[0]).lower() == 'города':

        if ln < 2:
            return [False, cites_button, 'Выберите режим работы, для этого воспользуйтесь кнопками ниже']

        if str(history[1]).lower() == 'выбрать определённый город':
            if ln == 2:
                return [False, main_button, 'Введите название города']

            try:
                with open(f'data/{str(history[-1]).lower()}.txt', 'r') as file:
                    text = file.read()
                bot.send_photo(chat_id, photo=open(f'data/{str(history[-1]).lower()}.jpg', 'rb'))
                return [False, main_button, text, 'Введите название другого города, либо выйдите в главное меню.']
            except:
                return [False, main_button, 'Данный город не найден в базе данных. '
                                            'Введите название другого города, либо выйдите в главное меню.']

        elif str(history[-1]).lower() == 'выбрать рандомный город':
            arr = os.listdir('data')
            index = random.randint(0, len(arr) - 1)
            city = str(arr[index])[:-4]

            with open(f'data/{city}.txt', 'r') as file:
                text = file.read()
            bot.send_photo(chat_id, photo=open(f'data/{city}.jpg', 'rb'))

            return [False, random_city_button, text]

        return [True, start_button, 'Возвращаемся в главное меню', main_menu]


    elif str(history[0]).lower() == 'написать в техподдержку':
        return [True, start_button, 'Telegram разработчика: @VladimirRumyantsev', main_menu]

    elif str(history[0]).lower() == 'поддержать разработчика':
        return [True, start_button, 'Карта Сбер: 2202203292922111\nКарта Тинькофф: 2200701057074624', main_menu]

    else:
        return [True, start_button, 'Главное меню', main_menu]


def telegram_bot():
    @bot.message_handler(content_types=['text'])
    def send_text(message):
        def delete_history():
            for j in range(len(talks)):
                if int(talks[j][0]) == message.chat.id:
                    talks.pop(j)
                    write_talks()

        user_history = []
        global ex_errors
        ex_errors = 0
        try:
            if not (message.chat.id in users):
                bot.send_message(
                    message.chat.id,
                    f'Первое сообщение пользователю\n'
                    f'Тут будет написано очень много текста'
                )
                bot.send_message(
                    message.chat.id,
                    f'{working([], message.chat.id)}', reply_markup=start_button
                )
                users.append(message.chat.id)
                write_users(message.chat.id)
            elif (message.text.lower() == '/start') or (message.text.lower() == 'вернуться в главное меню'):
                bot.send_message(
                    message.chat.id,
                    f'{working([], message.chat.id)}', reply_markup=start_button
                )
                delete_history()
            elif (message.chat.id in developers) and (str(message.text)[:7].lower() == '/answer'):
                x, recipient_id, text = str(message.text).split("\n", 2)
                bot.send_message(recipient_id, f'Вам сообщение от техподдержки:\n\n{text}')
                for i in developers:
                    bot.send_message(
                        i,
                        f'Пользователю {recipient_id} отправлено сообщение от техподдерки '
                        f'с таким текстом:\n\n{text}'
                    )
            elif (message.chat.id in developers) and (message.text.lower() == '/clear'):
                clear_logs()
                for i in developers:
                    bot.send_message(i, f'Логи отчищены!')
            else:
                for i in range(len(talks)):
                    if int(talks[i][0]) == message.chat.id:
                        (talks[i]).append(message.text)
                        write_talks()
                        user_history = (talks[i][1:]).copy()
                if not user_history:
                    talks.append([message.chat.id, message.text])
                    write_talks()
                    user_history.append(message.text)

                answer = working(user_history, message.chat.id)

                if answer[0]:
                    delete_history()
                for i in answer[2:]:
                    bot.send_message(
                        message.chat.id,
                        f'{i}', reply_markup=answer[1]
                    )

        except Exception as ex:
            bot.send_message(
                message.chat.id,
                f'Произошла неизвестная ошибка во время работы бота(((\n'
                f'Отчёт о Вашей ошибке отправлен разработчикам и поможет им продолжать совершенствовать '
                f'работоспособность бота\nЧтобы ошибка не повторилась — '
                f'советуем Вам воспользоваться командой /start, она вернёт Вас в главное меню'
            )
            user_history.append(message.text)
            for i in developers:
                bot.send_message(i, f'Во время работы с пользователем:\n{message.chat.id}\n\n'
                                    f'При получении такого сообщения:\n{message.text}\n\n'
                                    f'Произошла ошибка:\n{ex}')
            write_errors(message.chat.id, user_history, ex)

    bot.polling()


read_users()
read_talks()
ex_errors = 0
sleep = [0, 3, 10, 30, 60, 150, 300]
while True:
    try:
        write_logs(f'{(datetime.datetime.today()).strftime("%d.%m.%Y %H:%M:%S")} -> Start')
        telegram_bot()
    except Exception as ex:
        if ex_errors < len(sleep):
            ex_errors += 1

        if ex_errors <= 3:
            with open("errors.txt", "a", encoding="utf-8") as g_errors_file:
                g_errors_file.write(f'{(datetime.datetime.today()).strftime("%d.%m.%Y %H:%M:%S")}'
                                    f' -> Exception\n{ex}\n\n')
            write_logs(f'{(datetime.datetime.today()).strftime("%d.%m.%Y %H:%M:%S")} -> Exception\n{ex}')
        time.sleep(sleep[ex_errors - 1])
