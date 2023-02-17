from datetime import datetime
from telebot.apihelper import ApiTelegramException
from database import db
from keyboards.reply.action import request_foto
from keyboards.inline.inline_keyboards import keyboards
from loader import bot
from states.contact_information import StateHighprice
from telebot.types import Message, CallbackQuery
from handlers.search_hotels import search_hotel


@bot.message_handler(commands=['highprice'])
def get_city(message: Message) -> None:
    """
    Хандлер, реагирующий на команду highprice.
    После инициализации команду начинает опрос пользователя и возвращает найденные отели по высокой цене.
    """
    bot.send_message(message.from_user.id, f'Вы выбрали поиск дорогих отелей в городе \U00002705\n\n'
                                           f'{message.from_user.full_name} введите город для поиска \U0001F307')
    bot.set_state(message.from_user.id, StateHighprice.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.from_user.full_name


@bot.message_handler(state=StateHighprice.city)
def get_region(message: Message) -> None:
    """ Хандлер, выдающий пользователю варианты на выбор региона. """
    if message.text:
        bot.set_state(message.from_user.id, StateHighprice.region_selection, message.chat.id)
        dict_region = search_hotel.search_region(city=message.text)
        kb_region = keyboards(array=dict_region)
        if len(dict_region) > 0:
            bot.send_message(message.from_user.id, 'Уточните пожалуйста регион \U00002B07', reply_markup=kb_region)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['city'] = message.text
        else:
            bot.send_message(message.from_user.id, 'По вашему запросу ничего не найдено \U0001F612\n'
                                                   'Пожалуйста выберите действие из меню, и введите другой город.')
    else:
        bot.send_message(message.from_user.id, 'Для продолжения необходимо ввести город \U0001F612')


@bot.callback_query_handler(func=lambda call: True, state=StateHighprice.region_selection)
def callback(call: CallbackQuery) -> None:
    """
    Хандлер, обрабатывает нажатие варианта на клавиатуре, и
    запрашивает у пользователя кол-во отелей для просмотра.
    """
    bot.set_state(call.from_user.id, StateHighprice.amount_hostels, call.message.chat.id)
    bot.answer_callback_query(call.id, show_alert=True, text=f'Запомнил, ищем по ID: {call.data}  \U0001F504')
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['id_region'] = call.data

    bot.send_message(call.from_user.id, 'Сколько отелей хотите посмотреть? \U000027A1')


@bot.message_handler(state=StateHighprice.amount_hostels)
def get_start_date(message: Message) -> None:
    """
    Хандлер, проверяет введенное количество отелей на максимально допустимое кол-во,
    затем запрашивает информацию о дате начала проживания.
    """
    max_hotels = 10
    if message.text.isdigit() and int(message.text) <= max_hotels:
        bot.send_message(message.from_user.id, 'Введите дату начала проживания (дд-мм-гггг) \U000027A1')
        bot.set_state(message.from_user.id, StateHighprice.start_date, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['amount_hostels'] = message.text
    else:
        bot.send_message(message.from_user.id, f'Отелей возможно вывести не больше {max_hotels} \U0001F612')


@bot.message_handler(state=StateHighprice.start_date)
def get_end_date(message: Message) -> None:
    """
    Хандлер, проверяет введенную дату на корректность, согласно шаблону,
    затем запрашивает информацию об окончании проживания.
    """
    form_date = '%d-%m-%Y'
    try:
        if bool(datetime.strptime(message.text, form_date)):
            if datetime.strptime(message.text, form_date) >= datetime.today():
                bot.send_message(message.from_user.id, 'Введите дату окончания проживания (дд-мм-гггг) \U000027A1')
                bot.set_state(message.from_user.id, StateHighprice.end_date, message.chat.id)

                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data['start_date'] = message.text
            else:
                bot.send_message(message.from_user.id, f'Пожалуйста, проверьте дату на корректность \U0001F937\n'
                                                       f'Дата начала проживание не может быть раньше сегодняшней')
    except ValueError:
        bot.send_message(message.from_user.id, f'Пожалуйста, проверьте дату на корректность \U0001F937\n'
                                               f'И введите согласно образца -> (дд-мм-гггг)')


@bot.message_handler(state=StateHighprice.end_date)
def get_foto(message: Message) -> None:
    """
    Хандлер, проверяет введенную дату на корректность, согласно шаблону,
    затем запрашивает желание на просмотр фото.
    """
    form_date = '%d-%m-%Y'
    try:
        if bool(datetime.strptime(message.text, form_date)):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                if datetime.strptime(message.text, form_date) > datetime.strptime(data['start_date'], form_date):
                    bot.send_message(message.from_user.id, 'Хотели бы вы посмотреть фото? \U000027A1',
                                     reply_markup=request_foto())
                    bot.set_state(message.from_user.id, StateHighprice.foto, message.chat.id)
                    data['end_date'] = message.text
                else:
                    bot.send_message(message.from_user.id, f'Пожалуйста, проверьте дату на корректность \U0001F937\n'
                                                           f'Дата окончания не может быть ранее начальной\n'
                                                           f'И введите согласно образца -> (дд-мм-гггг)')
    except ValueError:
        bot.send_message(message.from_user.id, f'Пожалуйста, проверьте дату на корректность \U0001F937\n'
                                               f'И введите согласно образца -> (дд-мм-гггг)')


@bot.message_handler(state=StateHighprice.foto)
def get_amount_foto(message: Message) -> None:
    """
    Хандлер, проверяет нажатие кнопки и при положительном ответе запрашивает кол-во фото.
    При отрицательном ответе начинает поиск и выдаёт найденную информацию.
    """
    if message.text.title() == "Да":
        bot.send_message(message.from_user.id, 'Сколько фото для каждого отеля показать? \U000027A1')
        bot.set_state(message.from_user.id, StateHighprice.amount_foto, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['foto'] = message.text

    else:
        bot.set_state(message.from_user.id, StateHighprice.amount_foto, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['foto'] = message.text
            text = '\U0000263A Спасибо за предоставленную информацию: ' \
                   '\n\U00002714 Город для поиска - {city} ' \
                   '\n\U00002714 ID региона для поиска - {id}' \
                   '\n\U00002714 Кол-во отелей - {amount} ' \
                   '\n\U00002714 Период проживания {start} - {end}' \
                   '\n\U00002714 Показать фото - {foto}' \
                   '\n\nНачинаю поиск! \U000023F2 Пожалуйста, подождите'.format(
                    city=data['city'],
                    id=data['id_region'],
                    amount=data['amount_hostels'],
                    foto=data['foto'],
                    start=data['start_date'],
                    end=data['end_date']
                    )
            bot.send_message(message.from_user.id, text)

            info_for_user = search_hotel.search_info(id_region=data['id_region'], sort="PRICE_HIGH_TO_LOW",
                                                     count=data['amount_hostels'], max_price=5000, min_price=150,
                                                     start_data=data['start_date'], end_data=data['end_date'])
            for mg in info_for_user:
                db.add_data(id_user=message.from_user.id, command='/highprice',
                            date_time=str(datetime.today().strftime('%d-%m-%Y %H:%M')), info=mg)
                bot.send_message(message.from_user.id, mg)

            bot.set_state(message.from_user.id, StateHighprice, message.chat.id)


@bot.message_handler(state=StateHighprice.amount_foto)
def send_info_user(message: Message) -> None:
    """
    Хандлер, проверяет кол-во желаемых фото с допустимым количеством.
    При положительном результате начинает поиск и выдаёт найденную информацию.
    """
    max_foto = 10
    if message.text.isdigit() and int(message.text) <= max_foto:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['amount_foto'] = message.text

            text = '\U0000263A Спасибо за предоставленную информацию: ' \
                   '\n\U00002714 Город для поиска - {city} ' \
                   '\n\U00002714 ID региона для поиска - {id}' \
                   '\n\U00002714 Кол-во отелей - {amount} ' \
                   '\n\U00002714 Период проживания {start} - {end}' \
                   '\n\U00002714 Показать фото - {foto} ' \
                   '\n\U00002714 Кол-во фото - {am_foto} ' \
                   '\n\nНачинаю поиск! \U000023F2 Пожалуйста, подождите'.format(
                    city=data['city'],
                    id=data['id_region'],
                    amount=data['amount_hostels'],
                    foto=data['foto'],
                    am_foto=data['amount_foto'],
                    start=data['start_date'],
                    end=data['end_date']
                    )
            bot.send_message(message.from_user.id, text)

            info_for_user = search_hotel.search_info(id_region=data['id_region'], count=data['amount_hostels'],
                                                     sort="PRICE_HIGH_TO_LOW", max_price=5000, min_price=150,
                                                     foto=data['foto'], amount_foto=data['amount_foto'],
                                                     start_data=data['start_date'], end_data=data['end_date'])
            for elem in info_for_user:
                try:
                    if isinstance(elem, tuple):
                        if len(elem[0]) > 0:
                            db.add_data(id_user=message.from_user.id, command='/highprice',
                                        date_time=str(datetime.today().strftime('%d-%m-%Y %H:%M')), info=elem[1])
                            bot.send_media_group(message.chat.id, media=elem[0])
                            bot.send_message(message.from_user.id, elem[1])
                        else:
                            db.add_data(id_user=message.from_user.id, command='/highprice',
                                        date_time=str(datetime.today().strftime('%d-%m-%Y %H:%M')), info=elem[1])
                            bot.send_message(message.from_user.id, 'Фото не нашлось \U0001F612')
                            bot.send_message(message.from_user.id, elem[1])
                    else:
                        db.add_data(id_user=message.from_user.id, command='/lowprice',
                                    date_time=str(datetime.today().strftime('%d-%m-%Y %H:%M')), info=elem)
                        bot.send_message(message.from_user.id, text=elem)

                except ApiTelegramException:
                    bot.send_message(message.from_user.id, 'Произошла ошибка на сервере \U0001F612\n'
                                                           'Пожалуйста, повторите запрос')

            bot.set_state(message.from_user.id, StateHighprice, message.chat.id)
    else:
        bot.send_message(message.from_user.id, f'Количество фото не должно превышать {max_foto} \U0001F612')
