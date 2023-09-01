import datetime
import sqlite3
from loader import bot
from site_API import get_random_cat_fact


# HANDLERS
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "Hi! This bot can generate random facts about cats.\n"
                          "For start, select /random command")


@bot.message_handler(commands=['random'])
def random_handler(message):
    random_cat_fact = get_random_cat_fact()

    user_id = message.from_user.id
    username = message.from_user.username
    date_and_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS history(
                    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    username TEXT NOT NULL,
                    date_and_time TEXT NOT NULL,
                    random_cat_fact)""")
        cursor.execute("""INSERT INTO history (user_id, username, date_and_time, random_cat_fact)
                        VALUES (?, ?, ?, ?)""", (user_id, username, date_and_time, random_cat_fact))
        connect.commit()

    bot.send_message(message.chat.id, random_cat_fact)


@bot.message_handler(commands=['history'])
def history_handler(message):
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""SELECT random_cat_fact FROM history ORDER BY request_id DESC LIMIT 0, 3""")
        last_three_facts = []
        for cat_fact in cursor:
            last_three_facts.append(cat_fact[0])
        last_three_facts.reverse()
        last_three_facts.insert(0, 'The last three randomly generated facts about cats')
        for index, cat_fact in enumerate(last_three_facts[1:], 1):
            last_three_facts[index] = f'{index}. {cat_fact}'
        last_three_facts_str = '\n\n'.join(last_three_facts)
    bot.send_message(message.chat.id, last_three_facts_str)


@bot.message_handler(func=lambda message: True)
def any_others(message):
    bot.reply_to(message, "Sorry, I don't understand you. I can only generate random cat facts.\n"
                          "You can get it, using command /random")