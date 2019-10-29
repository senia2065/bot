from utils import get_keyboard, get_user_emo, is_cat
import logging
import os
from glob import glob
from random import choice

def hallou(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data["emo"] = emo
    text = "Привет, {} {}".format(update.message.chat.first_name, emo)
    logging.info("User: %s, Chat id: %s, Message: %s",  
                 update.message.chat.username, update.message.chat.id, update.message.text)
    
    update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = "Привет,{} {} ! Ты написал {}".format(update.message.chat.first_name, user_data["emo"],
                      update.message.text) 
    logging.info("User: %s, Chat id: %s, Message: %s",  
                 update.message.chat.username, update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def send_cat_picture(bot, update, user_data):
        cat_list = glob("images/*kot*.jpg")
        cat_pic = choice(cat_list)
        bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, "rb"), reply_markup=get_keyboard())


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text("Готово: {}".format(get_user_emo(user_data)), reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text("Готово: {}".format(get_user_emo(user_data)), reply_markup=get_keyboard())


def change_avatar(bot, update, user_data):
    if "emo" in user_data:
        del user_data["emo"]
    emo = get_user_emo(user_data)
    update.message.reply_text("Готово: {}".format(emo), reply_markup=get_keyboard())

def check_user_photo(bot, update, user_data):
    update.message.reply_text("Проверяю на котэ")
    os.makedirs('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    photo_file.download(filename)
    if is_cat(filename):
        update.message.reply_text("Обнаружен котэ! Добавляю в библиотеку!")
        new_filename = os.path.join('images', 'Kot_{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename)
    else:
        update.message.reply_text("К сожалению, котиков не нашел!")
        os.remove(filename)
        

