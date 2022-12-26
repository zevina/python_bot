import sqlite3
from telegram.ext import ConversationHandler


def show_list(update, context):
    conn = sqlite3.connect('peoples.db')
    cursor = conn.cursor()
    cursor.execute("select * from people")
    results = cursor.fetchall()
    update.message.reply_text("Телефонный справочник:\n")
    update.message.reply_text("\n".join([str(i) for i in results]))
    conn.commit()
    conn.close()
    return ConversationHandler.END


def find_list(update, context):
    surname = update.message.text
    conn = sqlite3.connect('peoples.db')
    cursor = conn.cursor()
    cursor.execute(f"select * from people where Surname like '%{surname}%'")
    results = cursor.fetchall()
    update.message.reply_text("\n".join([str(i) for i in results]))
    conn.commit()
    conn.close()
    return ConversationHandler.END


def add_to_list(update, context):
    data = update.message.text
    res = data.split()
    conn = sqlite3.connect('peoples.db')
    cursor = conn.cursor()
    cursor.execute(
        f"insert into people (Surname, phone)"
        f"values ('{res[0]}', {res[1]})")
    cursor.execute("select * from people")
    results = cursor.fetchall()
    update.message.reply_text("\n".join([str(i) for i in results]))
    conn.commit()
    conn.close()
    return ConversationHandler.END



def delete_from_list(update, context):
    id = update.message.text
    conn = sqlite3.connect('peoples.db')
    cursor = conn.cursor()
    cursor.execute(
        f"delete from people where id={id}"
    )
    cursor.execute("select * from people")
    results = cursor.fetchall()
    update.message.reply_text("Телефонный справочник:\n")
    update.message.reply_text("\n".join([str(i) for i in results]))
    conn.commit()
    conn.close()
    return ConversationHandler.END

