from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_foto() -> ReplyKeyboardMarkup:
	keyboards = ReplyKeyboardMarkup(True, True)
	keyboards.add(KeyboardButton('Да'))
	keyboards.add(KeyboardButton('Нет'))
	return keyboards
