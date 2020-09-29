import telebot, time
from telebot import types

tconv = lambda x: time.strftime("%d.%m.%Y  %H:%M:%S", time.localtime(x)) #Конвертация даты в читабельный вид
bot = telebot.TeleBot('1224298024:AAGEpxPwEbFBbiBGIBPYqse7yvNXilona74')

#@bot.message_handler(commands=['start'])
#def start(message):
#    print(message)
#    bot.send_message(218264388, 'Котик, приветик!')

#@bot.message_handler(commands=['text'])
#def start(message):
#    bot.send_message(218264388, 'Котик, приветик!')

name = ''
surname = ''
phone = 0
info = ''
admin = 334316846

@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Ваше имя :")
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Ваша фамилия :')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Ваш номер телефона :')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global phone
    phone = message.text

    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    global info;
    info = 'Имя: '+name+', фамилия: '+surname+', номер телефона: '+phone;
    question = 'Имя: '+name+', фамилия: '+surname+', номер телефона: '+phone+'. Сохранить?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
     #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню : )')
#        print(call.message);
#        bot.send_message(call.message.chat.id, info)
        bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAIBH19xxo887BPKL_lp2rsDaw3i010zAAL3AANSiZEjonpibT_h-0cbBA')

        bot.send_message(admin, tconv(call.message.date))
        bot.send_message(admin, call.message.chat.id)
        bot.send_message(admin, 'Имя: '+name)
        bot.send_message(admin, 'Фамилия: '+surname)
        bot.send_message(admin, 'Номер телефона: '+phone)
    elif call.data == "no":
     #переспрашиваем
        bot.send_message(call.message.chat.id, 'НЕ запомню : )')
        bot.send_message(call.message.chat.id, 'Попробуй еще раз после /reg')

bot.polling(none_stop=True, interval=0)
