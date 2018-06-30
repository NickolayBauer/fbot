import telebot
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(host='',
                        dbname='postgres',
                        user='postgres',
                        password='')
curs = conn.cursor()


bot = telebot.TeleBot("")

####################################находится ли id в определённом состоянии################################
def check(conditions, my_id):
	curs.execute("SELECT cond FROM users_test WHERE user_id = %s;",(my_id,))	
	if (curs.fetchall()[0][0]) == conditions:
		return True
	return False


##########################################существует ли запись с таким id###################################
def not_exist(my_id):
	curs.execute("SELECT cond FROM users_test WHERE user_id = %s;",(my_id,))
	if curs.fetchone() == None:
		return True
	return False

#############################################приветствие####################################################
@bot.message_handler(commands=["start", "старт"])
def hello(message):
	bot.send_message(message.chat.id, """Привет, человек. Я помогу тебе составить программу тренировок.
		команды: \n/help\n/add_date\n/show_date\n/update""")



#####################################добавление данных в бд#################################################
@bot.message_handler(func=lambda message: not_exist(message.chat.id), commands=['add_date'])
def add_date(message):
	bot.send_message(message.chat.id,"""следующее твоё сообщение будет добавлено в базу данных""")
	curs.execute("INSERT INTO users_test VALUES (%s,%s,%s);",(['NULL',message.chat.id,'first_add']))
	conn.commit()	


@bot.message_handler(func=lambda message: check('first_add',message.chat.id), content_types = ['text'])
def add_date(message):
	
	curs.execute("UPDATE users_test SET info_user = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users_test SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Данные успешно добавлены!""")

#################################обновление даннных в бд###################################################
@bot.message_handler(func=lambda message: not not_exist(message.chat.id) , commands=['update'])
def add_date(message):
	bot.send_message(message.chat.id,"""следующее твоё сообщение обновит базу данных""")
	curs.execute("UPDATE users_test SET cond = %s WHERE user_id = %s;",('update', message.chat.id))
	conn.commit()

@bot.message_handler(func=lambda message: check('update',message.chat.id), content_types = ['text'])
	curs.execute("UPDATE users_test SET info_user = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()curs.execute("UPDATE users_test SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Данные успешно обновлены!""")

#############################################################################################################
@bot.message_handler(func=lambda message: not not_exist(message.chat.id), commands=['add_date'])
def add_date(message):
	bot.send_message(message.chat.id,"""Твои данные уже есть в базе данных! Используй команду /update""")
#############################################################################################################
if __name__ == "__main__":
    bot.polling(none_stop=True)


