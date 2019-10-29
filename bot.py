
import logging
import settings
from handlers import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    logging.info("bot poschol")


    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", hallou, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex("^(Прислать котика)$"), send_cat_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex("^(Сменить аватарку)$"), change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
   
    mybot.start_polling()
    mybot.idle()
    
if __name__ == "__main__":
        main()