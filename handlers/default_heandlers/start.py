from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """Хандлер, реагирующий на команду start"""
    bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.full_name}! \U0001F91D\n"
                                        f"Вас приветствует бот по подбору лучших предложений по отелям.\n"
                                        f"Выберите действие из меню \U00002B07\n")
