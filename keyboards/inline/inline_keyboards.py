from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboards(array: list) -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardMarkup()
	for dict_info in array:
		for key, value in dict_info.items():
			keyboard.add(InlineKeyboardButton(text=key, callback_data=value))
	return keyboard
