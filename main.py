from openai import OpenAI
from jproperties import Properties
import telebot
import gpt


def get_property(prop):
    configs = Properties()
    with open('project.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get(prop)[0]


bot = telebot.TeleBot(get_property("BOT_TOKEN"), parse_mode='MARKDOWN')
openai_token = get_property("openai_token")
client = OpenAI(api_key=openai_token)
sarcastic = gpt.Sarcastic()


def request(companion):
    response = client.chat.completions.create(
        model=get_property("model"),
        messages=companion.messages,
        temperature=0.8,
        top_p=1
    )
    response = response.choices[0].message.content
    print(f"ответ: " + response)
    msg = gpt.create_assistant(response)
    companion.messages.append(msg)
    return response


@bot.message_handler()
def command_help(message):
    msg = gpt.create_user(message.text)
    sarcastic.messages.append(msg)
    print(f'вопрос: {message.text}')
    response = request(sarcastic)
    bot.reply_to(message, response)
    gpt.print_messages(sarcastic)


print("bot is running...")
bot.infinity_polling()
