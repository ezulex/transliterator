import os
import requests
import telebot
from alphabet import Alphabet
from dotenv import load_dotenv

load_dotenv()
TG_API_TOKEN = os.environ.get("TG_API_TOKEN")
bot = telebot.TeleBot(TG_API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я помогу перевести тебе транслит, просто пришли сообщение")


def parse_text(text, count, dictionary):
    result_text = str()
    i = 0
    while 1:
        if i >= len(text):
            break
        if text[i:i + count] in dictionary:
            result_text += dictionary[text[i:i + count]]
            i += count
        elif text[i:i + count - 1] in dictionary:
            result_text += dictionary[text[i:i + count - 1]]
            i += count - 1
        elif text[i] in dictionary:
            result_text += dictionary[text[i]]
            i += 1
        else:
            result_text += text[i]
            i += 1
    return result_text


def get_translate(lang, text):
    url = f'https://api.mymemory.translated.net/get?q={text}&langpair={lang}|ru'

    try:
        response = requests.get(url)
    except requests.ConnectionError as e:
        print("Ошибка подключения:", e)
        translate_string = "При переводе что-то пошло не так"
    except requests.Timeout as e:
        print("Ошибка тайм-аута:", e)
        translate_string = "При переводе что-то пошло не так"
    except requests.RequestException as e:
        print("Ошибка запроса:", e)
        translate_string = "При переводе что-то пошло не так"
    else:
        if response.status_code == 200:
            response_data = response.json()
            translate_string = response_data["responseData"]["translatedText"]
        else:
            translate_string = "При переводе что-то пошло не так"
    finally:
        return translate_string


@bot.message_handler(func=lambda message: True)
def convert_message(message):
    global letter_length, language_dict, lang_abbr_api
    select_lang = 'georgian'
    actual_text = message.text

    # Условие для будущего добавления языков, в select_lang будем получать из бота выбранный язык перевода
    if select_lang == 'georgian':
        language_dict = Alphabet.get_alphabet_dict('georgian')
        letter_length = 3
        lang_abbr_api = 'ka'

    reply_text = parse_text(actual_text, letter_length, language_dict)
    translate_text = get_translate(lang_abbr_api, reply_text)

    result_text = reply_text + '\n\n' + translate_text
    bot.reply_to(message, result_text)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
