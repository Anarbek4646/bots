# sql = stucturucted query lenguage
# subd система управление базой данных

import sqlite3
from random import choice
from sqlalchemy.dialects.sqlite import aiosqlite


def sql_create():
    global db, cursor
    db = sqlite3.connect('bot.sqlite3')
    cursor = db.cursor()

    if db:
        print('db connected')

    db.execute("""CREATE TABLE IF NOT EXISTS ivan (id INTEGER PRIMARY KEY,username TEXT,name TEXT,age INTEGER,gender TEXT,region TEXT, photo TEXT)""")
    db.commit()



async def sql_command_insert(state):
    async with state.proxy() as data:
        # Пример использования контекстного менеджера для работы с базой данных
        with sqlite3.connect('bot.sqlite3') as db:
            cursor = db.cursor()
            # Убедитесь, что вы правильно указали названия столбцов и их количество соответствует количеству передаваемых значений
            cursor.execute("INSERT INTO ivan (id, username, name, age, gender, region, photo) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (data['id'], data['username'], data['name'], data['age'], data['gender'], data['region'], data['photo']))
            db.commit()


async def sql_command_delete(user_id):
        cursor.execute("DELETE FROM ivan WHERE id = ?", (user_id,))
        db.commit

async def sql_command_random(message):
    result = cursor.execute("select * from ivan").fetchall()
    random_user = choice(result)
    await message.answer_photo(random_user[6],
                               caption=f'{random_user[2]} {random_user[3]} {random_user[4]} {random_user[5]} {random_user[1]}')

async def sql_command_find2(message):
    result = cursor.execute(f"select * from ivan where id = {message.from_user.id}").fetchone()
    random_user = result
    await message.answer_photo(random_user[6],
                               caption=f'{random_user[2]} {random_user[3]} {random_user[4]} {random_user[5]} {random_user[1]}')

async def sql_command_find(message):

    result = cursor.execute(f"select * from ivan where id = {message.from_user.id}").fetchone()
    random_user = result
    print(result)
    return random_user




async def sql_name_update(message):
    cursor.execute("UPDATE ivan SET name = ? WHERE id = ?", (message.text, message.from_user.id))
    db.commit()
async def sql_photo_update(message):
    cursor.execute("UPDATE ivan SET photo = ? WHERE id = ?", (message.text, message.from_user.id))
    db.commit()


# async def sql_command_update_name(message):
#     result = cursor.execute(f"""update ivan set name = ? where id = {message.from_user.id}""", message.text)
#     db.commit()
