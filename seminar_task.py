import logging
import emoji
import token_bot

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = token_bot.TOKEN


def start(update, context):
    update.message.reply_text(
        "Привет! Выберете:\n\n/calc - калькулятор\n/conv - конвертер")


def calc(update, context):
    update.message.reply_text("Введите выражение:\n")
    return 1


def calculate(update, context):
    try:
        calc_value = eval(update.message.text)
        update.message.reply_text(emoji.emojize(f":brain: Ответ: {calc_value}"))
        update.message.reply_text(emoji.emojize("Вы и сами могли это посчитать! :face_with_rolling_eyes:"))
        return ConversationHandler.END
    except Exception:
        update.message.reply_text(emoji.emojize(":warning: Введите правильное выражение"))


def conv(update, context):
    update.message.reply_text("Введите массу в килограммах:\n")
    return 1


def convert(update, context):
    try:
        conv_value = int(update.message.text)
        update.message.reply_text(emoji.emojize(f":brain: Масса: {conv_value * 1000} грамм"))
        update.message.reply_text(emoji.emojize("Это было слишком просто! :exploding_head:"))
        return ConversationHandler.END
    except Exception:
        update.message.reply_text(emoji.emojize(":warning: Введите целое число"))


def stop(update, context):
    update.message.reply_text("Вы и сами могли это посчитать! :face with rolling eyes:")
    return ConversationHandler.END



def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    calc_handler = ConversationHandler(

        entry_points=[CommandHandler('calc', calc)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, calculate)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('conv', conv)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, convert)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)
    dp.add_handler(calc_handler)
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
