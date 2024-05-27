import telebot
from telebot import types
import os
import datetime
import time
import random


bot = telebot.TeleBot('6928806121:AAHpUedibrQY4LU8_CIHu51d680kN41f9aM', parse_mode='Markdown')

main_menu = ('*Главное меню*\n\nУзнайте больше о Прикамье и его выдающихся жителях!\n\n'
             '*• Города:* Исследуйте историю населенных пунктов региона.\n'
             '*• Люди:* Откройте для себя биографии и достижения тех, кто оставил неизгладимый след в Пермском крае.'
             '\n\nВы также можете поделиться своей историей! Отправьте мне текстовый файл (.txt) с информацией '
             'о вашем городе или выдающейся личности, и после проверки модерацией они будут добавлены в бота.')

main_menu_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_button.add(
    types.KeyboardButton('Города'),
    types.KeyboardButton('Люди'),
    types.KeyboardButton('Контакты поддержки')
)

m1_p0_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
m1_p0_button.add(
    types.KeyboardButton('Определённый город'),
    types.KeyboardButton('Случайный город'),
    types.KeyboardButton('Главное меню')
)

m1_p1_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
m1_p1_button.add(
    types.KeyboardButton('Назад'),
    types.KeyboardButton('Главное меню')
)

m2_p0_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
m2_p0_button.add(
    types.KeyboardButton('Определённый человек'),
    types.KeyboardButton('Случайный человек'),
    types.KeyboardButton('Главное меню')
)

m2_p1_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
m2_p1_button.add(
    types.KeyboardButton('Назад'),
    types.KeyboardButton('Главное меню')
)

ex_errors = 0


def main():
    sleep = [0, 3, 10, 30, 60, 150, 300]

    while True:
        try:
            write_logs(f'{(datetime.datetime.today()).strftime("%d.%m.%Y %H:%M:%S")} -> Start')
            telegram_bot()
        except Exception as ex:
            global ex_errors
            if ex_errors < len(sleep):
                ex_errors += 1

            write_logs(f'{(datetime.datetime.today()).strftime("%d.%m.%Y %H:%M:%S")} -> Exception\n{ex}')
            time.sleep(sleep[ex_errors - 1])


def write_logs(text):
    with open("logs.txt", "a", encoding="utf-8") as logs_file:
        logs_file.write(f'{text}\n\n')


class User:
    def __init__(self, identifier):
        self.identifier = identifier
        user_id_str = "{:010d}".format(identifier)
        self.path = os.path.join("users", user_id_str[0], user_id_str[1], user_id_str[2], user_id_str[3],
                                 user_id_str[4], user_id_str[5], user_id_str[6], user_id_str[7], user_id_str[8],
                                 user_id_str[9])

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.mode = -1
            self.phase = 0

        else:
            with open(f'{self.path}/data.txt', "r", encoding='utf-8') as f:
                arr = f.readlines()
                self.mode = int(arr[1])
                self.phase = int(arr[2])

    def write(self):
        with open(f'{self.path}/data.txt', "w", encoding='utf-8') as f:
            f.write(f'{str(self.identifier)}\n{str(self.mode)}\n{str(self.phase)}')


def telegram_bot():
    @bot.message_handler(content_types=['text', 'document'])
    def send_text(message):
        global ex_errors
        ex_errors = 0

        try:
            user = User(message.chat.id)
        except Exception as ex:
            user_id_str = "{:010d}".format(message.chat.id)
            path = os.path.join("users", user_id_str[0], user_id_str[1], user_id_str[2], user_id_str[3],
                                user_id_str[4], user_id_str[5], user_id_str[6], user_id_str[7], user_id_str[8],
                                user_id_str[9])

            if os.path.exists(path):
                os.rmdir(path)

            user = User(message.chat.id)
            user.mode = 0
            user.phase = 0
            user.write()

            bot.send_message(
                message.chat.id,
                'К сожалению, произошла неожиданная ошибка. '
                'Поддержка рассмотрит Вашу проблему, чтобы подобные ошибки больше не тревожили Вас.'
            )
            bot.send_message(message.chat.id, main_menu, reply_markup=main_menu_button)

            raise Exception(f'Exception code: 152\nID: {message.chat.id}\nMessage: {message.text}\nException: "{ex}"')

        try:
            if message.content_type == 'document':
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                book = str(downloaded_file.decode('utf-8'))

                bot.send_message(
                    message.chat.id,
                    'Спасибо, мы ознакомимся с данным документом.\n'
                    'Такие статьи помогают нам развивать наш проект.'
                )

                if not os.path.exists(f'booksFromUsers'):
                    os.makedirs(f'booksFromUsers')

                n = 0
                file_name = (f'booksFromUsers/{user.identifier}_'
                             f'{(datetime.datetime.today()).strftime("%d%m%Y_%H%M%S")}{str(n)}')

                while os.path.exists(f'{file_name}.txt'):
                    n += 1
                    file_name = f'{file_name[:-(len(str(n-1)))]}{str(n)}'

                with open(f'{file_name}.txt', "w", encoding='utf-8') as f:
                    f.write(book)

            elif (user.mode == -1) or (message.text.lower() == '/start') or (message.text.lower() == 'главное меню'):
                if message.text.lower() != 'главное меню':
                    bot.send_message(
                        message.chat.id,
                        "*Приветствую Вас в боте о Прикамье и его выдающихся личностях!*\n\n"
                        "Я здесь, чтобы познакомить Вас с богатой историей этого региона.\n\n"
                        "Исследуйте населенные пункты Прикамья, узнайте о людях, которые оставили неизгладимый "
                        "след в его истории, и поделитесь своими собственными знаниями о регионе.\n\n"
                        "Начните ваше путешествие прямо сейчас и откройте для себя красоту и наследие Прикамья!"
                    )
                bot.send_message(message.chat.id, main_menu, reply_markup=main_menu_button)
                user.mode = 0
                user.phase = 0

            elif user.mode == 0:
                if message.text.lower() == 'города':
                    bot.send_message(
                        message.chat.id,
                        "Выберите режим работы при помощи кнопок ниже",
                        reply_markup=m1_p0_button
                    )
                    user.mode = 1

                elif message.text.lower() == 'люди':
                    bot.send_message(
                        message.chat.id,
                        "Выберите режим работы при помощи кнопок ниже",
                        reply_markup=m2_p0_button
                    )
                    user.mode = 2

                elif message.text.lower() == 'контакты поддержки':
                    bot.send_message(
                        message.chat.id,
                        "*Контакты поддержки:*\n"
                        "https://t.me/VladimirRumyantsev\n"
                        "https://t.me/LyutyChyort\n"
                        "https://t.me/kystikikolychie\n"
                        "https://t.me/Lisiy_Svet\n\n"
                        "Чтобы поддержать разработчиков финансово, напишите одному из контактов.",
                        reply_markup=main_menu_button, parse_mode='Markdown'
                    )

            elif user.mode == 1:
                if user.phase == 0:
                    if message.text.lower() == 'определённый город':
                        cities = os.listdir('data/cities')
                        line = ''
                        for i in cities:
                            line += f'\n• [{i}](tg://resolve?domain=history_of_parma_bot&text={i})'

                        bot.send_message(
                            message.chat.id,
                            f"Введите название города, о котором желаете узнать больше"
                            f"\n\nГорода, которые у нас есть:{line}",
                            reply_markup=m1_p1_button
                        )
                        user.phase = 1

                    elif message.text.lower() == 'случайный город':
                        arr = os.listdir('data/cities')
                        index = random.randint(0, len(arr) - 1)
                        city = arr[index]

                        bot.send_photo(message.chat.id, photo=open(f'data/cities/{city}/{city}.jpg', 'rb'))
                        with open(f'data/cities/{city}/{city}.txt', 'r') as file:
                            bot.send_message(message.chat.id, file.read(), reply_markup=m1_p0_button)

                elif (user.phase == 1) and (message.text.lower() == 'назад'):
                    bot.send_message(
                        message.chat.id,
                        "Выберите режим работы при помощи кнопок ниже",
                        reply_markup=m1_p0_button
                    )
                    user.phase = 0

                elif user.phase == 1:
                    city = str(message.text)[0].upper() + str(message.text)[1:].lower()
                    try:
                        bot.send_photo(message.chat.id, photo=open(f'data/cities/{city}/{city}.jpg', 'rb'))
                        with open(f'data/cities/{city}/{city}.txt', 'r') as file:
                            bot.send_message(message.chat.id, file.read(), reply_markup=m1_p1_button)

                        bot.send_message(
                            message.chat.id,
                            'Вы можете ввести название другого города, либо выйти в главное меню.',
                            reply_markup=m1_p1_button
                        )
                    except FileNotFoundError:
                        cities = os.listdir('data/cities')
                        line = ''
                        for i in cities:
                            line += f'\n• [{i}](tg://resolve?domain=history_of_parma_bot&text={i})'

                        bot.send_message(
                            message.chat.id,
                            'Данный город не найден в базе данных. '
                            'Вы можете ввести название другого города, либо выйти в главное меню.\n\n'
                            f'Города, которые у нас есть:{line}',
                            reply_markup=m1_p1_button
                        )
                    except Exception as ex:
                        raise Exception(f'Exception code: 238\nException: {ex}')

            elif user.mode == 2:
                if user.phase == 0:
                    if message.text.lower() == 'определённый человек':
                        people = os.listdir('data/people')
                        line = ''
                        for i in people:
                            line += f'\n• [{i}](tg://resolve?domain=history_of_parma_bot&text={i})'

                        bot.send_message(
                            message.chat.id,
                            f"Введите фамилию человека, о котором желаете узнать больше"
                            f"\n\nЛюди, которые у нас есть:{line}",
                            reply_markup=m2_p1_button
                        )
                        user.phase = 1

                    elif message.text.lower() == 'случайный человек':
                        arr = os.listdir('data/people')
                        index = random.randint(0, len(arr) - 1)
                        human = arr[index]

                        bot.send_photo(message.chat.id, photo=open(f'data/people/{human}/{human}.jpg', 'rb'))
                        with open(f'data/people/{human}/{human}.txt', 'r') as file:
                            bot.send_message(message.chat.id, file.read(), reply_markup=m2_p0_button)

                elif (user.phase == 1) and (message.text.lower() == 'назад'):
                    bot.send_message(
                        message.chat.id,
                        "Выберите режим работы при помощи кнопок ниже",
                        reply_markup=m2_p0_button
                    )
                    user.phase = 0

                elif user.phase == 1:
                    human = str(message.text)[0].upper() + str(message.text)[1:].lower()
                    try:
                        bot.send_photo(message.chat.id, photo=open(f'data/people/{human}/{human}.jpg', 'rb'))
                        with open(f'data/people/{human}/{human}.txt', 'r') as file:
                            bot.send_message(message.chat.id, file.read(), reply_markup=m2_p1_button)

                        bot.send_message(
                            message.chat.id,
                            'Вы можете ввести фамилию другого человека, либо выйти в главное меню.',
                            reply_markup=m2_p1_button
                        )
                    except FileNotFoundError:
                        people = os.listdir('data/people')
                        line = ''
                        for i in people:
                            line += f'\n• [{i}](tg://resolve?domain=history_of_parma_bot&text={i})'

                        bot.send_message(
                            message.chat.id,
                            'Данный человек не найден в базе данных. '
                            'Вы можете ввести фамилию другого человека, либо выйти в главное меню.\n\n'
                            f'Люди, которые у нас есть:{line}',
                            reply_markup=m2_p1_button
                        )
                    except Exception as ex:
                        raise Exception(f'Exception code: 238\nException: {ex}')

            user.write()

        except Exception as ex:
            bot.send_message(
                message.chat.id,
                'К сожалению, произошла неожиданная ошибка. '
                'Поддержка рассмотрит Вашу проблему, чтобы подобные ошибки больше не тревожили Вас.'
            )

            raise Exception(f'Exception code: 280\nID: {message.chat.id}\nMode: {str(user.mode)}\n'
                            f'Phase: {str(user.phase)}\nMessage: {message.text}\nException: "{ex}"')

    bot.polling()


if __name__ == '__main__':
    main()
