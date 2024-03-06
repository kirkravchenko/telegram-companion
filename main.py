from openai import OpenAI
from jproperties import Properties
import telebot
import prompter
from pprintpp import pprint


def get_property(prop):
    configs = Properties()
    with open('project.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get(prop)[0]


bot = telebot.TeleBot(get_property("BOT_TOKEN"), parse_mode='MARKDOWN')
openai_token = get_property("openai_token")
client = OpenAI(api_key=openai_token)


def request(messages):
    response = client.chat.completions.create(
        model=get_property("model"),
        messages=messages,
        temperature=0.8,
        top_p=1
    )
    response = response.choices[0].message.content
    # print(f"ответ: " + response)
    messages.append(
        prompter.get_assistant_msg(response)
    )
    return response


@bot.message_handler()
def command_help(message):
    prompter.stanislav_messages.append(
        prompter.get_user_msg(message.text)
    )
    # print(f'вопрос: {message.text}')
    response = request(prompter.stanislav_messages)
    bot.reply_to(message, response)
    pprint(prompter.stanislav_messages)
    print('=========================================================================================================================================================================================================================================================================================================================================')


print("bot is running...")
bot.infinity_polling()
