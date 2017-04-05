#!/usr/bin/env python3
import logging
import datetime
import os

import data_control
from configuration import Configuration

import telegram
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

b_line = KeyboardButton('Линия')
b_account = KeyboardButton('Личный кабинет')
b_info = KeyboardButton('Справка')
b_register = KeyboardButton('Зарегистрироваться')
b_balance = KeyboardButton('Баланс')
b_record = KeyboardButton('История ставок')
b_deposit = KeyboardButton('Пополнить счет')
b_withdraw = KeyboardButton('Вывести средства')
b_yes = KeyboardButton('Да, всё верно')
b_no = KeyboardButton('Ввести ещё раз')
b_back = KeyboardButton('Назад')
b_cancel = KeyboardButton('Отмена')
b_home = KeyboardButton('На главную')
b_rules = KeyboardButton('Правила приёма ставок')
b_feedback = KeyboardButton('Отзывы и пожелания')

main_keyboard = ReplyKeyboardMarkup([[b_line], [b_account], [b_info]], one_time_keyboard=0)
start_keyboard = ReplyKeyboardMarkup([[b_register]], one_time_keyboard=1)
info_keyboard = ReplyKeyboardMarkup([[b_rules], [b_feedback], [b_home]], one_time_keyboard=0)
account_keyboard = ReplyKeyboardMarkup([[b_balance], [b_record], [b_home]], one_time_keyboard=0)
balance_keyboard = ReplyKeyboardMarkup([[b_deposit], [b_withdraw], [b_back], [b_home]], one_time_keyboard=0)
register_keyboard = ReplyKeyboardMarkup([[b_yes], [b_no]], one_time_keyboard=0)

dic = dict()


# Обработка текста
def echo(bot, update):
    """
    Общая обработка текста
    :param bot:
    :param update:
    :return:
    """

    global dic

    global b_back
    utext = update.message.text
    utext_cf = utext.casefold()
    uchat = update.message.chat_id

    if utext_cf == 'зарегистрироваться' or utext_cf == 'ввести ещё раз':
        bot.sendMessage(chat_id=uchat,
                        text='Введите свой QIWI-кошелек в формате +7ХХХХХХХХХХ \n  Например: "+79106887538"')
        dic[str(uchat)]['mode'] = 'qiwi'
    elif utext_cf == 'на главную':
        dic[str(uchat)]['mode'] = ''
        bot.sendMessage(chat_id=uchat, text='Выберите пункт', reply_markup=main_keyboard)
    elif utext_cf == 'справка':
        dic[str(uchat)]['mode'] = 'info'
        bot.sendMessage(chat_id=uchat, text='Выберите пункт', reply_markup=info_keyboard)
    elif utext_cf == 'да, всё верно':
        con.add_user(uchat, dic[str(uchat)]['qiwi'], 0)
        dic[str(uchat)]['mode'] = ''
        bot.sendMessage(chat_id=uchat, text='Вы уcпешно зарегистрированы', reply_markup=main_keyboard)
    elif utext_cf == 'линия':
        sports = con.get_sports()
        sports1 = []
        for sport in sports:
            sports1.append([sport])
        sports1.append([b_home])
        dic[str(uchat)]['sport_keyboard'] = ReplyKeyboardMarkup(sports1, one_time_keyboard=0)
        bot.sendMessage(chat_id=uchat, text='Выберите вид спорта', reply_markup=dic[str(uchat)]['sport_keyboard'])
        dic[str(uchat)]['mode'] = 'sport'
    elif utext_cf == 'личный кабинет':
        user = con.get_user_by_telegram_id(uchat)
        response = 'Ваш аккаунт - ' + str(user[3])
        bot.sendMessage(chat_id=uchat, text=response, reply_markup=account_keyboard)
    elif utext_cf == 'баланс':
        user = con.get_user_by_telegram_id(uchat)
        response = 'Ваш баланс равен ' + str(user[2]) + 'р.'
        bot.sendMessage(chat_id=uchat, text=response, reply_markup=balance_keyboard)
        dic[str(uchat)]['mode'] = 'balance'

    elif dic[str(uchat)]['mode'] == 'balance':
        if utext_cf == 'назад':
            user = con.get_user_by_telegram_id(uchat)
            response = 'Ваш аккаунт - ' + str(user[3])
            bot.sendMessage(chat_id=uchat, text=response, reply_markup=account_keyboard)
            dic[str(uchat)]['mode'] = ''
        elif utext_cf == 'пополнить счет':
            response = 'На данный момент, бот работает с одной платёжной системой: QIWI. Для того, чтобы делать ставки, пополните пожалуйста счёт со своего QIWI-кошелька, который вы указали при регистрации. Ваш баланс пополнится в течение пяти минут. \n' \
                       'Сделайте перевод на QIWI-кошелёк бота: +79106887538. \n' \
                       'Всегда могут возникнуть технические неполадки. Если происходит задержка с пополнением более 10 минут, вы можете написать в тех. поддержку: @ioffside.'
            bot.sendMessage(chat_id=uchat, text=response, reply_markup=main_keyboard)
            dic[str(uchat)]['mode'] = ''
        elif utext_cf == 'вывести средства':
            bot.sendMessage(chat_id=uchat, text='Введите сумму для вывода в рублях \n' \
                            'Для отмены вывода нажмите "На главную"')
            dic[str(uchat)]['mode'] = 'withdraw'

    elif dic[str(uchat)]['mode'] == 'withdraw':
        if utext_cf == 'назад':
            user = con.get_user_by_telegram_id(uchat)
            response = 'Ваш баланс равен ' + str(user[2]) + 'р.'
            bot.sendMessage(chat_id=uchat, text=response, reply_markup=balance_keyboard)
            dic[str(uchat)]['mode'] = 'balance'
        else:
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
                response += 'Номер: ' + str(bet[0]) + ' ' + str((event[5]).strftime(' %d.%m.%y %H:%M')) + ' ' + str(
                    event[3]) + ' - ' + str(event[4]) + ' ' + str(
                    bet[1]) + ' ' + str(
                    bet[3]) + 'р. Коэфф: ' + str(bet[2]) + ' '
                if str(bet[4]) == 'unknown':
                    response += 'Не рассчитана'
                else:
                    response += str(bet[4])
                response += '\n'

        bot.sendMessage(chat_id=uchat, text=response, reply_markup=main_keyboard)
    elif dic[str(uchat)]['mode'] == 'qiwi':
        if utext_cf[0] == '+' and len(utext_cf) > 11 and len(utext_cf) < 15:
            dic[str(uchat)]['mode'] = ''
            dic[str(uchat)]['qiwi'] = utext_cf
            bot.sendMessage(chat_id=uchat, text='Ваш qiwi-кошелек - ' + dic[str(uchat)]['qiwi'] + ' ?',
                            reply_markup=register_keyboard)
        else:
            bot.sendMessage(chat_id=uchat, text='Ошибка, попробуйте еще раз', reply_markup=start_keyboard)
            dic[str(uchat)]['mode'] = ''
    elif dic[str(uchat)]['mode'] == 'sport':
        leagues = con.get_leagues_by_sport(str(utext_cf))
        leagues1 = []
        for league in leagues:
            leagues1.append([league])
        leagues1.append([b_back])
        leagues1.append([b_home])
        dic[str(uchat)]['leagues_keyboard'] = ReplyKeyboardMarkup(leagues1, one_time_keyboard=0)
        bot.sendMessage(chat_id=uchat, text='Выберите лигу', reply_markup=dic[str(uchat)]['leagues_keyboard'])
        dic[str(uchat)]['mode'] = 'league'

    elif dic[str(uchat)]['mode'] == 'league':
        if utext_cf == 'назад':
            dic[str(uchat)]['mode'] = 'sport'
            bot.sendMessage(chat_id=uchat, text='Выберите пункт', reply_markup=dic[str(uchat)]['sport_keyboard'])
        else:
            dic[str(uchat)]['league'] = str(utext_cf)
            events = con.get_events_by_league(str(utext_cf))
            events1 = []
            for event in events:
                events1.append([event])
            events1.append([b_back])
            events1.append([b_home])
            dic[str(uchat)]['events_keyboard'] = ReplyKeyboardMarkup(events1, one_time_keyboard=0)
            bot.sendMessage(chat_id=uchat, text='Выберите событие', reply_markup=dic[str(uchat)]['events_keyboard'])
            dic[str(uchat)]['mode'] = 'event'

    elif dic[str(uchat)]['mode'] == 'event':
        if utext_cf == 'назад':
            dic[str(uchat)]['mode'] = 'league'
            bot.sendMessage(chat_id=uchat, text='Выберите пункт', reply_markup=dic[str(uchat)]['leagues_keyboard'])
        else:
            event = con.get_ratios_by_teams(str(utext_cf), dic[str(uchat)]['league'])
            event.append([b_back])
            event.append([b_home])
            dic[str(uchat)]['max_bet'] = con.get_maxbet_by_teams(str(utext_cf), dic[str(uchat)]['league'])
            dic[str(uchat)]['event_teams'] = str(utext_cf)
            dic[str(uchat)]['event_id'] = con.get_event_id_by_teams(str(utext_cf), dic[str(uchat)]['league'])
            dic[str(uchat)]['ratios_keyboard'] = ReplyKeyboardMarkup(event, one_time_keyboard=1)
            bot.sendMessage(chat_id=uchat, text='Выберите исход', reply_markup=dic[str(uchat)]['ratios_keyboard'])
            dic[str(uchat)]['mode'] = 'bet'

    elif dic[str(uchat)]['mode'] == 'bet':
        if utext_cf == 'назад':
            dic[str(uchat)]['mode'] = 'event'
            bot.sendMessage(chat_id=uchat, text='Выберите исход', reply_markup=dic[str(uchat)]['events_keyboard'])
        else:
            balance = str(con.get_user_by_telegram_id(uchat)[2])
            response = 'Ваш выбор: ' + dic[str(uchat)]['event_teams'] + ' ' + \
                       str(utext_cf) + '. Пожалуйста, введите сумму ставки в рублях. Min = 5, Max = ' + \
                       str(dic[str(uchat)][
                               'max_bet']) + '\n(Ваш баланс = ' + balance + 'р.)' + '\n Для отмены ввода введите "отмена"'
            dic[str(uchat)]['choice'] = str(utext_cf)
            bot.sendMessage(chat_id=uchat, text=response)
            dic[str(uchat)]['mode'] = 'make_bet'

    elif dic[str(uchat)]['mode'] == 'make_bet':
        if utext_cf == 'отмена':
            dic[str(uchat)]['mode'] = 'event'
            bot.sendMessage(chat_id=uchat, text='Выберите исход', reply_markup=dic[str(uchat)]['ratios_keyboard'])
        else:
            response = con.add_bet(uchat, dic[str(uchat)]['event_teams'], dic[str(uchat)]['choice'], str(utext_cf), dic[str(uchat)]['league'])
            bot.sendMessage(chat_id=uchat, text=response, reply_markup=main_keyboard)

    elif dic[str(uchat)]['mode'] == 'info':
        dic[str(uchat)]['mode'] = ''
        if str(utext_cf) == 'правила приёма ставок':
            response = 'Приветствуем вас в пункте "Справка".\n' \
                       '"Справка" поможет вам, если вы ввёли неверно свой QIWI-кошелёк при регистрации. Пожалуйста, напишите запрос на адрес: @ioffside и вам сменят указанный при регистрации кошелек, на кошелек, с которого вы собираетесь пополнять счёт. Очень просим, делайте запрос в одном посте, с максимальной информацией. \n' \
                       'Так как бот молодой, то и событий пока будет немного. Только основные чемпионаты в разных видах спорта. \n' \
                       'Общие положения: \n' \
                       'Максимальная сумма ставки зависит от события\n' \
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
        elif str(utext_cf) == 'отзывы и пожелания':
            response = 'Дорогие клиенты, мы не просим у вас документы, мы стараемся быстро рассчитывать ставки после окончания матчей (до 5 минут). \n' \
                       ' Так же мы стараемся почти мгновенно пополнять счёта, и самое главное так же быстро выплачивать ваши выигрыши. \n' \
                       'Если у вас есть какое-то пожелание, или вы чем-то недовольны, то напишите нам свои слова по адресам: @ioffside , @blockbet. \n'
        else:
            response = 'Что-то пошло не так, попробуйте еще раз'
        bot.sendMessage(chat_id=uchat, text=response, reply_markup=main_keyboard)
    elif utext_cf == 'назад':
        dic[str(uchat)]['mode'] = ''
        bot.sendMessage(chat_id=uchat, text='Выберите пункт', reply_markup=main_keyboard)


def start(bot, update):
    global dic
    user = con.get_user_by_telegram_id(update.message.chat_id)
    dic[str(update.message.chat_id)] = {'mode': '', 'qiwi': '', 'event_id': '', 'event_teams': '',
                                        'sport_keyboard': ReplyKeyboardMarkup([[]], one_time_keyboard=0),
                                        'leagues_keyboard': ReplyKeyboardMarkup([[]], one_time_keyboard=0),
                                        'events_keyboard': ReplyKeyboardMarkup([[]], one_time_keyboard=0),
                                        'ratios_keyboard': ReplyKeyboardMarkup([[]], one_time_keyboard=1),
                                        'choice': '', 'max_bet': '', 'league': ''}
    if user:
        bot.sendMessage(chat_id=update.message.chat_id, text='Мы рады, что вы вернулись', reply_markup=main_keyboard)
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
        response = input('> ').casefold()
        if response == 'stop':
            break
        else:
            print('Unknown command')


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
    # bot_conf = Configuration('conf/access.ini')

    logging.info('Script execution started')
    print('Script started')

    try:
        telegram_token = '374736040:AAHG-ZGYmDZu4HtSSIw0H0VoITf36DfV3Ts'
        # bot_conf.get_option('Main', 'TelegramToken')
        updater = Updater(token=telegram_token)
    except (telegram.error.InvalidToken, ValueError):
        print('Critical Error > Telegram Access Token is invalid. Terminal halted.\nCheck the configuration file.')
        exit()

    con = data_control.Connection('root', 'Yor8nsKt', 'betbot')

    users = (con.get_all_users())
    for user in users:
        logging.info('user added ' + str(user))
        dic[str(user)] = {'mode': '', 'qiwi': '', 'event_id': '', 'event_teams': '',
                          'sport_keyboard': ReplyKeyboardMarkup([[]], one_time_keyboard=0),
                          'leagues_keyboard': ReplyKeyboardMarkup([[]], one_time_keyboard=0),
                          'events_keyboard': ReplyKeyboardMarkup([[]], one_time_keyboard=0),
                          'ratios_keyboard': ReplyKeyboardMarkup([[]], one_time_keyboard=0),
                          'choice': '', 'max_bet': '', 'league': ''}

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
