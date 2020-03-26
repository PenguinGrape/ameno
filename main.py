import json
import requests
import telebot
from PIL import Image, ImageDraw, ImageFont

config = json.load(open("/etc/ameno/config.json", "rb"))
token = config['token']
download_to = config['download_to']
bot = telebot.TeleBot(token)


def ameno(file):
    image = Image.open(file)
    tool = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    # I used this one: https://www.dafont.com/ameno.font
    font = ImageFont.truetype("/etc/ameno/ameno.ttf", int(width/7))
    x = int(width / 2 - width / 3.5)
    y = int(height * 0.77)
    tool.text((x, y), "DORIME", (255, 255, 255), font=font)
    image.save(f'{download_to}/output.jpg', 'JPEG', quality=100)


download = 'https://api.telegram.org/file/bot' + token + '/'


@bot.message_handler(content_types=["photo"])
def meme(message):
    photo = message.photo[-1].file_id
    path = bot.get_file(file_id=photo).file_path
    with open(f'{download_to}/temp.jpg', 'wb') as file:
        r = requests.get(download + path)
        for chunk in r:
            file.write(chunk)
    ameno(f'{download_to}/temp.jpg')
    f = open(f'{download_to}/output.jpg', 'rb')
    bot.send_photo(message.chat.id, f, None)


if __name__ == '__main__':
    bot.polling(none_stop=True)
