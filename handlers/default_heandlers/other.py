from telebot.types import Message
from loader import bot


@bot.message_handler(content_types=['text'])
def bot_start(message: Message) -> None:
	"""Хандлер, реагирующий на команду приветствие"""
	greetings = ['Привет', 'Здравтвуй', 'Здорова', 'Приветики', 'Здравствуйте', 'Добрый день']
	if message.text.title() in greetings:
		bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.full_name}! \U0001F91D"
												f"\nВас приветствует бот по подбору лучших предложений по отелям."
												f"\nВыберите действие из меню \U00002B07\n")
	else:
		bot.send_message(message.from_user.id, f"К сожалению я вас не понимаю \U0001F440\n"
												f"Выберите команду - /start")
