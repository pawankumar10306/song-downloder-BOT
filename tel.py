from ytmdl import search,download
import telebot

# Insert your bot's token here
TOKEN = "7259601459:AAGrb7gX9Mie7HDYhzKLhbrTo9MgnI3CVyE"

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello! I am your song Downloder bot.Send me a song name")

# Handle text messages
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    payloads = search(message.text)
    result = download(payloads)
    for item in result:
        title = item.get('title')
        image = item.get('image')
        url = item.get('url')
        description = item.get('description')

        try:
            bot.send_audio(
                chat_id=message.chat.id,
                audio = url,
                title = title,
                caption = description,
                thumbnail = image
                )
        except Exception as e:
            bot.send_message(message.chat.id,f"An error occurred: {e}\nAudio URL: {url}\n<b>Title: {title}</b>\nDescription: {description}")

    bot.send_message(message.chat.id,"Thanks for Using Song Downloder")


# Start the bot
if __name__ == '__main__':
    bot.polling()