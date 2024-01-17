import requests
import telebot
from alphabet import Alphabet

TG_API_TOKEN = ''

bot = telebot.TeleBot(TG_API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я бот, который поможет тебе перевести транслит")


#Парсинг текста на символы, дописать для парсинга по последовательностям,
# count, максимальная последовательность для языка
def parse_text(text, count, dictionary):
    len_text = len(text)
    result_text = str()
    last_result = True
    for i in range(0, len_text):
        if text[i:i + count] in dictionary.keys():
            temp_text = dictionary[text[i:i + count]]
            last_result = True
        else:
            if not last_result:
                temp_text = text[i:i + count][-1]
            else:
                temp_text = text[i:i + count]
                last_result = False
        result_text = result_text + temp_text

    if count == 1:
        return result_text
    else:
        parse_text(result_text, count - 1, dictionary)


#Запрос к API, добавить проверку кода ответа и выбрасывание исключений
def get_translate(lang, text):
    url = f'https://api.mymemory.translated.net/get?q={text}&langpair={lang}|ru'

    response = requests.get(url)
    response_data = response.json()
    translate_string = response_data["responseData"]["translatedText"]
    return translate_string


#Ответ бота
@bot.message_handler(func=lambda message: True)
def convert_message(message):
    language_dict = Alphabet.get_alphabet_dict('georgian')
    actual_text = message.text.lower()
    reply_text = str()

    len_actual_text = len(actual_text)

    #Переписать в функции parse_text для работы с последовательностью символов, а не по одному
    for i in range(0, len_actual_text):
        if actual_text[i] in language_dict.keys():
            temp_text = language_dict[actual_text[i]]
        else:
            temp_text = actual_text[i]
        reply_text = reply_text + temp_text

    translate_text = get_translate('ka',reply_text)
    result_text = reply_text + '\n\n' + translate_text
    bot.reply_to(message, result_text)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
