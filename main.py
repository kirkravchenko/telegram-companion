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
save_dialogue = False

def request(messages):
    response = client.chat.completions.create(
        model=get_property("model"),
        messages=messages,
        temperature=0.8,
        top_p=1
    )
    return response.choices[0].message.content


@bot.message_handler()
def command_help(message):
    prompter.user_messages.append(
        prompter.get_user_msg(message.text)
    )
    if len(prompter.user_messages) > 4:
        prompter.user_messages = prompter.user_messages[-4:]
    messages = prompter.system_message + [prompter.get_user_msg(message.text)]
    if save_dialogue:
        messages = prompter.system_message + prompter.user_messages
    print('Sending the messages to GPT:\n')
    pprint(messages)
    response = request(messages)
    prompter.user_messages.append(prompter.get_assistant_msg(response))
    bot.reply_to(message, response)
    print(
        '=========================================================================================================================================================================================================================================================================================================================================')


print("bot is running...")
bot.infinity_polling()
