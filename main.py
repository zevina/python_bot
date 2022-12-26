# выполнено совместно с Рябовым Андреем
import logging
import token_bot
import model
import sqlite3

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = token_bot.TOKEN


def start(update, context):
    update.message.reply_text(
        "Привет! Выбери действие:\n"
        "\n/show    - показать весь телефонный справочник"
        "\n/find       - найти человека в справочнике по фамилии"
        "\n/add       - добавить запись в телефонный справочник"
        "\n/delete   - удалить строку из телефонного справочника"
    )


def find(update, context):
    update.message.reply_text("Введите фамилию:\n")
    return 1


def add(update, context):
    update.message.reply_text("Введите фамилию и телефон через пробел:\n")
    return 1


def delete(update, context):
    conn = sqlite3.connect('peoples.db')
    cursor = conn.cursor()
    cursor.execute("select * from people")
    results = cursor.fetchall()
    update.message.reply_text("Телефонный справочник:\n")
    update.message.reply_text("\n".join([str(i) for i in results]))
    update.message.reply_text("\nВведите номер строки для удаления:\n")
    return 1


def stop(update, context):
    update.message.reply_text("Пока!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    show_handler = ConversationHandler(

        entry_points=[CommandHandler('show', model.show_list)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, model.show_list)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    find_handler = ConversationHandler(

        entry_points=[CommandHandler('find', find)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, model.find_list)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    add_handler = ConversationHandler(

        entry_points=[CommandHandler('add', add)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, model.add_to_list)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    delete_handler = ConversationHandler(

        entry_points=[CommandHandler('delete', delete)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, model.delete_from_list)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)
    dp.add_handler(show_handler)
    dp.add_handler(find_handler)
    dp.add_handler(add_handler)
    dp.add_handler(delete_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
