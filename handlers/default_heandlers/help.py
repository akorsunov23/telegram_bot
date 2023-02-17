from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'\U0001F6A9 /{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n\n'.join(text))
