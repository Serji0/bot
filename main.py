#!/usr/bin/env python3
import logging
import datetime
import os

import data_control
from configuration import Configuration

import telegram
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

mode = ''
event_id = 0
event_teams = ''
max_bet = ''

b_line = KeyboardButton('Линия')
b_account = KeyboardButton('Личный кабинет')
b_info = KeyboardButton('Справка')
b_register = KeyboardButton('Зарегистрироваться')
b_rules = KeyboardButton('Правила')
b_support = KeyboardButton('Поддержка')
b_balance = KeyboardButton('Баланс')
b_record = KeyboardButton('История ставок')
b_deposit = KeyboardButton('Пополнить счет')
b_withdraw = KeyboardButton('Вывести средства')
b_yes = KeyboardButton('Да, всё верно')
b_no = KeyboardButton('Ввести ещё раз')
b_back = KeyboardButton('Назад')
b_cancel = KeyboardButton('Отмена')
b_home = KeyboardButton('На главную')

main_keyboard = ReplyKeyboardMarkup([[b_line], [b_account], [b_info]], one_time_keyboard=0)
start_keyboard = ReplyKeyboardMarkup([[b_register]], one_time_keyboard=1)
info_keyboard = ReplyKeyboardMarkup([[b_rules], [b_support], [b_home]], one_time_keyboard=0)
account_keyboard = ReplyKeyboardMarkup([[b_balance], [b_record], [b_back], [b_home]], one_time_keyboard=0)
balance_keyboard = ReplyKeyboardMarkup([[b_deposit], [b_withdraw], [b_back], [b_home]], one_time_keyboard=0)
register_keyboard = ReplyKeyboardMarkup([[b_yes], [b_no]], one_time_keyboard=0)
bet_keyboard = ReplyKeyboardMarkup([[b_yes], [b_cancel]], one_time_keyboard=0)
sport_keyboard = ReplyKeyboardMarkup([[]], one_time_keyboard=0)
leagues_keyboard = ReplyKeyboardMarkup([[]], one_time_keyboard=0)
events_keyboard = ReplyKeyboardMarkup([[]], one_time_keyboard=0)
ratios_keyboard = ReplyKeyboardMarkup([[]], one_time_keyboard=0)


# Обработка текста
def echo(bot, update):
    """
    Общая обработка текста
    :param bot:
    :param update:
    :return:
    """
    global mode
    global qiwi
    global sport_keyboard
    global leagues_keyboard
    global events_keyboard
    global ratios_keyboard
    global event_id
    global event_teams
    global b_back
    global choice
    global max_bet
    utext = update.message.text
    utext_cf = utext.casefold()
    uchat = update.message.chat_id

    if utext_cf == 'зарегистрироваться' or utext_cf == 'ввести ещё раз':
        bot.sendMessage(chat_id=uchat, text='Введите свой QIWI-кошелек в формате +7ХХХХХХХХХХ \n  Например: "+79106887538"')
        mode = 'qiwi'
    elif utext_cf == 'на главную':
        mode = ''
        bot.sendMessage(chat_id=uchat, text='Выберите пункт', reply_markup=main_keyboard)
    elif utext_cf == 'да, всё верно':
        con.add_user(uchat, qiwi, 0)
        mode = ''
        bot.sendMessage(chat_id=uchat, text='Вы уcпешно зарегистрированы', reply_markup=main_keyboard)
    elif utext_cf == 'линия':
        sports = con.get_sports()
        sports1 = []
        for sport in sports:
            sports1.append([sport])
        sports1.append([b_home])
        sport_keyboard = ReplyKeyboardMarkup(sports1, one_time_keyboard=0)
        bot.sendMessage(chat_id=uchat, text='Выберите вид спорта', reply_markup=sport_keyboard)
        mode = 'sport'
    elif utext_cf == 'личный кабинет':
        user = con.get_user_by_telegram_id(uchat)
        response = 'Ваш аккаунт - ' + str(user[3])
        bot.sendMessage(chat_id=uchat, text=response, reply_markup=account_keyboard)
    elif utext_cf == 'баланс':
        user = con.get_user_by_telegram_id(uchat)
        response = 'Ваш баланс равен ' + str(user[2]) + 'р.'
        bot.sendMessage(chat_id=uchat, text=response, reply_markup=balance_keyboard)
        mode = 'balance'

    elif mode == 'balance':
        if utext_cf == 'назад':
            user = con.get_user_by_telegram_id(uchat)
            response = 'Ваш аккаунт - ' + str(user[3])
            bot.sendMessage(chat_id=uchat, text=response, reply_markup=account_keyboard)
            mode = ''
        elif utext_cf == 'пополнить счет':
            response = 'На данный момент, бот работает с одной платёжной системой: QIWI. Для того, чтобы делать ставки, пополните пожалуйста счёт со своего QIWI-кошелька, который вы указали при регистрации. Ваш баланс пополнится в течение пяти минут. \n' \
                       'Сделайте перевод на QIWI-кошелёк бота: +79106887538. \n' \
                       'Всегда могут возникнуть технические неполадки. Если происходит задержка с пополнением более 10 минут, вы можете написать в тех. поддержку: @ioffside.'
            bot.sendMessage(chat_id=uchat, text=response, reply_markup=main_keyboard)
            mode = ''
        elif utext_cf == 'вывести средства':
            bot.sendMessage(chat_id=uchat, text='Введите сумму для вывода в рублях')
            mode = 'withdraw'

    elif mode == 'withdraw':
        con.add_request(uchat, utext_cf, 'withdraw')
        bot.sendMessage(chat_id=uchat, text='Ваш запрос принят', reply_markup=main_keyboard)

    elif utext_cf == 'история ставок':
        bets = con.get_bets(uchat)
        response = ''
        if not bets:
            response = 'Вы пока не сделали ни одной ставки'
        else:
            for bet in bets:
                event = con.get_event_by_id(bet[5])
                response += 'Номер: ' + str(bet[0]) + ' ' + str(event[3]) + ' - ' + str(event[4]) + ' ' + str(
                    bet[1]) + ' ' + str(
                    bet[3]) + 'р. Коэфф: ' + str(bet[2]) + ' '
                if str(bet[4]) == 'unknown':
                    response += 'Не рассчитана'
                else:
                    response += str(bet[4])
                response += '\n'

        bot.sendMessage(chat_id=uchat, text=response, reply_markup=main_keyboard)
    elif mode == 'qiwi':
        if utext_cf[0] == '+' and len(utext_cf) > 11 and len(utext_cf) < 15:
            mode = ''
            qiwi = utext_cf
            bot.sendMessage(chat_id=uchat, text='Ваш qiwi-кошелек - ' + qiwi + ' ?', reply_markup=register_keyboard)
        else:
            bot.sendMessage(chat_id=uchat, text='Ошибка, попробуйте еще раз', reply_markup=start_keyboard)
            mode = ''
    elif mode == 'sport':
        leagues = con.get_leagues_by_sport(str(utext_cf))
        leagues1 = []
        for league in leagues:
            leagues1.append([league])
        leagues1.append([b_back])
        leagues1.append([b_home])
        leagues_keyboard = ReplyKeyboardMarkup(leagues1, one_time_keyboard=0)
        bot.sendMessage(chat_id=uchat, text='Выберите лигу', reply_markup=leagues_keyboard)
        mode = 'league'

    elif mode == 'league':
        if utext_cf == 'назад':
            mode = 'sport'
            bot.sendMessage(chat_id=uchat, text='Выберите пункт', reply_markup=sport_keyboard)
        else:
            events = con.get_events_by_league(str(utext_cf))
            events1 = []
            for event in events:
                events1.append([event])
            events1.append([b_back])
            events1.append([b_home])
            events_keyboard = ReplyKeyboardMarkup(events1, one_time_keyboard=0)
            bot.sendMessage(chat_id=uchat, text='Выберите событие', reply_markup=events_keyboard)
            mode = 'event'

    elif mode == 'event':
        if utext_cf == 'назад':
            mode = 'league'
            bot.sendMessage(chat_id=uchat, text='Выберите пункт', reply_markup=leagues_keyboard)
        else:
            event = con.get_ratios_by_teams(str(utext_cf))
            event.append([b_back])
            event.append([b_home])
            max_bet = con.get_maxbet_by_teams(str(utext_cf))
            event_teams = str(utext_cf)
            event_id = con.get_event_id_by_teams(str(utext_cf))
            ratios_keyboard = ReplyKeyboardMarkup(event, one_time_keyboard=0)
            bot.sendMessage(chat_id=uchat, text='Выберите исход', reply_markup=ratios_keyboard)
            mode = 'bet'

    elif mode == 'bet':
        if utext_cf == 'назад':
            mode = 'event'
            bot.sendMessage(chat_id=uchat, text='Выберите исход', reply_markup=events_keyboard)
        else:
            response = 'Ваш выбор: ' + event_teams + ' ' + \
                       str(utext_cf) + '. Пожалуйста, введите сумму ставки в рублях. Max = ' + str(max_bet)
            choice = str(utext_cf)
            bot.sendMessage(chat_id=uchat, text=response)
            mode = 'make_bet'

    elif mode == 'make_bet':
        response = con.add_bet(uchat, event_teams, choice, str(utext_cf))
        bot.sendMessage(chat_id=uchat, text=response, reply_markup=main_keyboard)

    elif utext_cf == 'назад':
        mode = ''
        bot.sendMessage(chat_id=uchat, text='Выберите пункт', reply_markup=main_keyboard)

    elif utext_cf == 'справка':
        mode = ''
        response = 'Приветствуем вас в пункте "Справка".\n' \
                   '"Справка" поможет вам, если вы ввёли неверно свой QIWI-кошелёк при регистрации. Пожалуйста, напишите запрос на адрес: @ioffside и вам сменят указанный при регистрации кошелек, на кошелек, с которого вы собираетесь пополнять счёт. Очень просим, делайте запрос в одном посте, с максимальной информацией. \n' \
                   'Так как бот молодой, то и событий пока будет немного. Только основные чемпионаты в разных видах спорта. \n' \
                   'Общие положения: \n' \
                   'Максимальная сумма ставки: 1000 руб\n' \
                   'Минимальная сумма ставки: 5 руб. \n' \
                   'Правила рассчёта ставок: \n' \
                   'Футбол:\n' \
                   'Ставка будет рассчитана, если матч доигран до конца или там было сыграно не менее 65 минут 00 секунд. \n' \
                   'Хоккей: \n' \
                   'Ставка будет рассчитана, если матч доигран до конца или там было сыграно не менее 54 минуты 00 секунд. \n' \
                   'Баскетбол: \n' \
                   'Ставка будет рассчитана, если матч доигран до конца или там было сыграно не менее 39 минут 00 секунд (для НБА). \n' \
                   'Ставка будет рассчитана, если матч доигран до конца или там было сыграно не менее 33 минуты 00 секунд (для евробаскетбола). \n' \
                   'Теннис: \n' \
                   'Если матч не доигран по какой-либо причине, то ставка рассчитывается с коэффициентом 1. \n' \
                   'Киберспорт: \n' \
                   'Если матч не доигран по какой-либо причине, то ставка рассчитывается с коэффициентом 1. \n'
        bot.sendMessage(chat_id=uchat, text=response, reply_markup=main_keyboard)

    '''
    global mode
    utext = update.message.text
    utext_cf = utext.casefold()
    uchat = update.message.chat_id

    # Несколько тестовых проверок на совпадения
    if 'привет' in utext_cf:
        bot.sendMessage(chat_id=uchat, text='Привет, друг! Хочешь кофейку, или секретное задание?',
                        reply_markup=keyboard)
    elif utext_cf == 'справка':
        response = 'Список доступных команд:\n' \
                   '/start - Проверка работоспособности бота\n' \
                   '/help - Справка по использованию бота\n\n' \
                   'Для добавления нового события нажмите на кнопку "Добавить событие", а затем введите информацию о нем в формате:\n' \
                   '{Дата события} {Время события} {Описание события}\n' \
                   'Например:\n' \
                   '01.01.2017 00:00 Поздравить друзей с Новым Годом\n' \
                   '< или >\n' \
                   '01.01.17 00:00 Поздравить друзей с Новым Годом\n\n' \
                   'Также, поддерживается расширенный формат ввода\n' \
                   'После указания даты и времени можно указать дату и время ' \
                   'напоминания по такому же формату и категорию вида < #{категория} >\n' \
                   'Например:\n' \
                   '08.02.2017 09:00 01.02.2017 20:00 #работа День Рождения начальника\n\n' \
                   'Для удаления события нажмите на кнопку "Удалить событие", а затем введите его описание\n' \
                   'Все прошедшие события удаляются автоматически\n' \
                   'Бот умеет говорить умные фразы! Пообщайтесь с ним!'
        bot.sendMessage(chat_id=update.message.chat_id, text=response, reply_markup=keyboard)
    elif utext.casefold() == 'добавить событие':
        mode = '+'
        response = 'Введите данные о событии в формате:\n[Дата события] [Время события] [Описание события]\n\n' \
                   'Например:\n' \
                   '01.01.2345 00:00 Отпраздновать Галактический Новый Год!\n' \
                   '20.12.16 18:00 Экзамен в Технопарке\n\n' \
                   'Для отмены ввода напишите "Отмена"'
        bot.sendMessage(chat_id=uchat, text=response)
    elif utext_cf == 'удалить событие':
        response = 'О каком событии мне не напоминать тебе? Введи название события, пожалуйста.\n\n' \
                   'Для отмены ввода напишите "Отмена"'
        bot.sendMessage(chat_id=uchat, text=response)
        mode = '-'
    elif utext_cf == 'список активных задач':
        db_control.start()
        chat_id = update.message.chat_id
        event_list = db_control.get_info(chat_id)
        if event_list == '':
            response = 'Хмм... Кажется, активных событий сейчас нет. Может, настало время исправить это?'
        else:
            response = 'Список текущих активных задач:\n\n'
            response += event_list
        bot.sendMessage(chat_id=update.message.chat_id, text=response, reply_markup=keyboard)
    elif utext_cf == 'отмена':
        mode = ''
        bot.sendMessage(chat_id=uchat, text='Выберите действие', reply_markup=keyboard)
    elif mode == '+':
        lang = language_processing.LanguageProcessing()
        result = lang.analyse(uchat, utext)
        if result:
            delay = round((result[0].date_notify - datetime.datetime.now()).total_seconds())

            if delay < 0:
                bot.sendMessage(chat_id=uchat,
                                text='Пожалуй, я не смогу напомнить о событии, '
                                     'если время напоминания уже прошло ¯\_(ツ)_/¯\n'
                                     'Возможно, время указано неправильно?',
                                reply_markup=keyboard)
            else:
                # Запись события в базу данных
                # Исправить
                db_control.start()
                db_control.add_event(result[0])
                queue.put(Job(callback, delay, repeat=False,
                              context=db_control.get_last_id()))
                db_control.stop()
                mode = ''
                # Уведомление об успешной записи
                if delay > 0:
                    bot.sendMessage(chat_id=uchat,
                                    text='Хорошо, я напомню тебе об этом {date}.'.format(
                                        date=result[0].date_notify_conv),
                                    reply_markup=keyboard)
        else:
            bot.sendMessage(chat_id=uchat,
                            text='Что-то пошло не так, не могу понять что. '
                                 'Может, погода испортилась и мои шестеренки теперь хуже крутятся. '
                                 'Попробуй еще раз, пожалуйста!')
    elif mode == '-':
        db_control.start()
        msg = db_control.delete_event(utext, uchat)
        db_control.stop()
        mode = ''
        bot.sendMessage(chat_id=uchat,
                        text=msg, reply_markup=keyboard)
    else:
        response = 'Что-то пошло не так, не могу понять что. ' \
                   'Вернее, понять могу, но говорить не буду. ' \
                   'Попробуй ещё раз, пожалуйста!\n' \
                   'Введите /help для получения справки.'
        bot.sendMessage(chat_id=uchat, text=response, reply_markup=keyboard)
'''


def start(bot, update):
    user = con.get_user_by_telegram_id(update.message.chat_id)
    if user:
        bot.sendMessage(chat_id= update.message.chat_id, text='Мы рады, что вы вернулись', reply_markup=main_keyboard)
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                    text='Чтобы начать делать ставки в боте, в котором вы сейчас находитесь, необходимо пройти регистрацию. Пожалуйста, нажмите "Зарегистрироваться" и следуйте дальнейшим инструкциям бота. Обращаем ваше внимание на то, что при регистрации вводите ТОЧНЫЙ свой QIWI-кошелек, с которого будете пополнять и именно на этот же кошелек вам будут приходить ваши выигрыши.',
                    reply_markup=start_keyboard)
    logging.info('Command \'start\' invoked by chat id [{0}]'.format(update.message.chat_id))


def telegram_command_handle(updater):
    """
    Обработка команд из чата Telegram
    :param updater:
    :return:
    """

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)


def terminal_command_handle():
    while True:
        # Приём команд на выполнение
        '''response = input('> ').casefold()
        if response == 'stop':
            break
        elif response == 'ping':
            print('pong')
        elif response == 'eadd':
            # Добавляет тестовое событие в базу данных
            e = events.Event(0, datetime.datetime.now(), datetime.datetime.now(), 0, 'datacontrol add')
            db_control.start()
            # Добавляем событие и присваиваем ему id количества имеющихся элементов в базе
            db_control.add_event(e)
            db_control.stop()
        elif response == 'eshow':
            # Выводит события из базы данных на экран
            db_control.start()
            for event in db_control.get_events(False):
                print(event)
            db_control.stop()
        elif response == 'lreq':
            request = input('Enter a message to analyse: ')
            # В тестовом режиме передается wit-токен равный нулю
            lang = language_processing.LanguageProcessing()
            print(lang.analyse(0, request))
        else:
            print('Unknown command')'''


if __name__ == "__main__":
    # Настройка логирования
    if not os.path.exists('logs/main.log'):
        if not os.path.exists('logs/'):
            os.mkdir('logs/')
        with open('logs/main.log', 'w') as f:
            f.write('[[[ LOGFILE BOUND TO < {} >  MODULE ]]]\n\n'.format(os.path.split(__file__)[1]))
    logging.basicConfig(filename='logs/main.log', format='<%(asctime)s> [%(name)s] [%(levelname)s]: %(message)s',
                        level=logging.INFO)

    # Настройка конфигурирования
    bot_conf = Configuration('conf/access.ini')

    logging.info('Script execution started')
    print('Script started')

    try:
        telegram_token = bot_conf.get_option('Main', 'TelegramToken')
        updater = Updater(token=telegram_token)
    except (telegram.error.InvalidToken, ValueError):
        print('Critical Error > Telegram Access Token is invalid. Terminal halted.\nCheck the configuration file.')
        exit()

    con = data_control.Connection('root', 'Yor8nsKt', 'betbot')

    # Обработка команд из чата Telegram
    telegram_command_handle(updater)
    updater.start_polling()

    logging.info('Started main updater polling')
    print('Running the main script normally')

    # Режим терминала
    terminal_command_handle()

    # Отключение бота
    logging.info('Stopping main updater polling')
    print('Stopping the main script...')
    updater.stop()
    logging.info('Script execution ended')
    print('Main script stopped')
