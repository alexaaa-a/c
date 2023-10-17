import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6634167674:AAH1-Igeht6dmwU7w1QtG1oxwdm9kpFeuY8",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()
    hobby = State()
    animal = State()




class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Заполнить анкету"  # Можно менять текст
text_button_1 = "Интересный факт"  # Можно менять текст
text_button_2 = "Веселое видео"  # Можно менять текст
text_button_3 = "О чат_боте"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.username}! Что будем делать?',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! Ваше _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер!Сколько вам лет?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Ваше хобби?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.hobby, message.chat.id)


@bot.message_handler(state=PollState.hobby)
def hobby(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['hobby'] = message.text
    bot.send_message(message.chat.id, 'Ваше любимое животное?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.animal, message.chat.id)

@bot.message_handler(state=PollState.animal)
def animal(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['animal'] = message.text
    bot.send_message(message.chat.id, f'Ваша анкета заполнена! \n'\
                                      f' Вас зовут {data["name"]} \n Вам {data["age"]} лет \n Ваше хобби - {data["hobby"]} \n Любимое животное - {data["animal"]}'
, reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Интересный факт](https://dymontiger.livejournal.com/15806868.html)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Веселое видео](https://www.youtube.com/watch?v=cOul5W0qSmo&t=188s)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, " Я чат-бот, предназначенный для анкитирования. Также я делюсь интересными фактами и забавными видео!", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()

