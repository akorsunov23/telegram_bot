from loader import bot
from states.contact_information import StateHistory
from telebot.types import Message
from database import db


@bot.message_handler(commands=['history'])
def get_start(message: Message) -> None:
	"""
	Хандлер, реагирующий на команду history.
	Запрашивает у пользователя кол-во запросов, и начинает поиск истории в базе данных
	и возвращает информацию о его действиях.
	"""
	bot.send_message(message.from_user.id, f'Вы выбрали показ истории запросов \U00002705\n\n'
										f'Какое количество последних записей показать? \U000027A1')
	bot.set_state(message.from_user.id, StateHistory.amount_requests, message.chat.id)


@bot.message_handler(state=StateHistory.amount_requests)
def get_history(message: Message) -> None:
	if message.text.isdigit():
		history = db.get_data(id_user=message.from_user.id, amount=int(message.text))
		if len(history) == 0:
			bot.send_message(message.from_user.id, 'Ваша история пуста \U0001F937')
		else:
			bot.send_message(message.from_user.id, f'{message.from_user.full_name}, ищу в базе данных \U0001F5C2')
			for elem in history:
				text = '\U0001F4CE\nВведённая команда: {command}\n' \
					'Дата-время запроса: {dtime}\n' \
					'Найденная информация: \n{info}'.format(
						command=elem[0],
						dtime=elem[1],
						info='\n'.join(elem[2].split('\\n'))
						)
				bot.send_message(message.from_user.id, text)
		bot.set_state(message.from_user.id, StateHistory, message.chat.id)
	else:
		bot.send_message(message.from_user.id, 'Только цифры! \U0001F937')
