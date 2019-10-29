from utils import get_keyboard, get_user_emo, is_cat
import logging
import os
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
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
        

def anketa_start(bot, update, user_data):
    update.message.reply_text("Как вас зовут? Напишите имя и фамилию", reply_markup=ReplyKeyboardRemove())
    return "name"

def anketa_get_name(bot, update, user_data):
    user_name = update.message.text
    if len(user_name.split(" ")) != 2:
        update.message.reply_text("Вы ввели не имя! Подумайте ещё!")
        return "name"
    else:
        user_data["anketa_name"] = user_name
        reply_Keyboard = [["1", "2", "3", "4", "5"]] 

        update.message.reply_text(
        "Оцените бота от 1 до 5",
        reply_markup = ReplyKeyboardMarkup(reply_Keyboard, one_time_keyboard=True)
        )
        return "raiting"

def anketa_rating(bot, update, user_data):
    user_data['anketa_rating'] = update.message.text
    update.message.reply_text("""Оставьте свой комментарий 
или введите /cancel для завершения""")
    return "comment"


def anketa_comment(bot, update, user_data):
    user_data['anketa_comment'] = update.message.text
    user_text = """
<b>Имя Фамилия:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}
<b>Комментарий:</b> {anketa_comment}""".format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def anketa_skip_comment(bot, update, user_data):
    user_text = """
<b>Имя Фамилия:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}""".format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode = ParseMode.HTML)
    return ConversationHandler.END


def dont_know(bot, update, user_data):
    update.message.reply_text("Не поняяяятнооо....")




