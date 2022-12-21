import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в слудующем формате: \n<имя валюты цену которой вы хотите узнать> \
<имя валюты в которой вы хотите узнать цену первой валюты> \
<количество первой валюты>\n<Увидеть список всех доступных валют: /values >'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Принимается только 3 параметра.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} равен {total_base} {base} '
        bot.send_message(message.chat.id, text)

bot.polling()
