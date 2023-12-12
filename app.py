import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет!\nЧтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют:\n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Видимо, что-то пошло не так :)\nДанные нужно вводить через пробел:\n<имя валюты> <в какую валюту перевести> \
<количество>\nСимволы <> вводить не надо\nНапример: биткоин доллар 1\nУвидеть список всех доступных валют:\n/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        raw_data = message.text.split(' ')

        def create_line_for_processing():
            result = []
            number_of_spaces = 0
            other_symbols = '''!()-[]{};?"@#$%:'\\,./^&amp;*_'''
            for elem in raw_data:
                new_elem = ''
                if len(elem) != 0:
                    for i in range(len(elem)):
                        if elem[i].isalpha() or elem[i].isdigit():
                            number_of_spaces = 1
                            new_elem += elem[i]
                        elif elem[i] in other_symbols:
                            pass
                        else:
                            if number_of_spaces > 1:
                                pass
                            else:
                                new_elem += elem[i]
                                number_of_spaces += 1
                    result.append(new_elem.strip())
            return result
        final_data = create_line_for_processing()

        if final_data[-2].isdigit() and final_data[-1].isdigit():
            raise ConvertionException('Вы ввели несколько чисел вместо одного:\nПосмотрите ещё раз,'
                                      'как нужно вводить данные\n'
                                      '/help')

        elif len(final_data) < 3:
            raise ConvertionException('Вы ввели мало параметров, чего-то не хватает\nПосмотрите ещё раз,'
                                      'как нужно вводить данные\n'
                                      '/help')

        quote, base, amount = final_data
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base * float(amount)} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()


