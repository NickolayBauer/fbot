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
	try:
		curs.execute("SELECT cond FROM users WHERE user_id = %s;",(my_id,))	
		if (curs.fetchall()[0][0]) == conditions:
			return True
	except IndexError:
		pass

	return False
##################################есть ли данные###########################################################
def if_NULL(my_id):
	try:
		curs.execute("SELECT struc FROM users WHERE user_id = %s;",(my_id,))
		if curs.fetchone()[0] == '':
			return True
	except TypeError:
		return True
	return False

##########################################существует ли запись с таким id###################################
def exist(my_id):
	curs.execute("SELECT cond FROM users WHERE user_id = %s;",(my_id,))
	if curs.fetchone() == None:
		return False
	return True

#############################################приветствие####################################################
@bot.message_handler(commands=["start", "старт"])
def hello(message):
	bot.send_message(message.chat.id, """Привет, человек. Я помогу тебе составить программу тренировок.
		команды: \n/help\n/add_date\n/show_date\n/update""")
@bot.message_handler(commands=["help"])
def hello(message):
	bot.send_message(message.chat.id, """Привет, человек. Я помогу тебе составить программу тренировок.
		команды: \n
				   /add_date  - добавить данные\n
				   /show_date - показать данные\n
				   /update    - обновить данные""")


#####################################добавление данных в бд#################################################
@bot.message_handler(func=lambda message: True, commands=['add_date'])
def add_date1(message):
	if if_NULL(message.chat.id) == True:
		bot.send_message(message.chat.id,"""следующее твоё сообщение будет добавлено в базу данных\nВведи вес: """)
		curs.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s);",([message.chat.id,'NULL','NULL','NULL','NULL','NULL','weight']))
		conn.commit()
	else:
		bot.send_message(message.chat.id,"твои данные уже существуют, используй /update")


@bot.message_handler(func=lambda message: check('weight',message.chat.id), content_types = ['text'])
def add_date2(message):
	#тут нужно сделать проверку на нормальность данных
	curs.execute("UPDATE users SET weight = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('height', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Окей, теперь введи рост""")


@bot.message_handler(func=lambda message: check('height',message.chat.id), content_types = ['text'])
def add_date3(message):
	#тут нужно сделать проверку на нормальность данных
	curs.execute("UPDATE users SET height = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('age', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Окей, теперь введи возраст""")

@bot.message_handler(func=lambda message: check('age',message.chat.id), content_types = ['text'])
def add_date4(message):
	#тут нужно сделать проверку на нормальность данных
	curs.execute("UPDATE users SET age = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('gender', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Окей, теперь введи свой пол""")

@bot.message_handler(func=lambda message: check('gender',message.chat.id), content_types = ['text'])
def add_date5(message):
	#тут нужно сделать проверку на нормальность данных
	curs.execute("UPDATE users SET gender = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('struc', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""окей теперь укажи телосложение """)

@bot.message_handler(func=lambda message: check('struc',message.chat.id), content_types = ['text'])
def add_date6(message):
	#тут нужно сделать проверку на нормальность данных
	curs.execute("UPDATE users SET struc = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Готово, все твои данные созданы, ты можешь посмотреть их командой /show_date """)

# #################################обновление даннных в бд###################################################
@bot.message_handler(func=lambda message: True , commands=['update'])
def update1(message):
	if exist(message.chat.id) == True:

		keyboard = types.InlineKeyboardMarkup()
		callback_button1 = types.InlineKeyboardButton(text="вес", callback_data="weight")
		callback_button2 = types.InlineKeyboardButton(text="рост", callback_data="height")
		callback_button3 = types.InlineKeyboardButton(text="возраст", callback_data="age")
		callback_button4 = types.InlineKeyboardButton(text="телосложение", callback_data="struc")
		callback_button5 = types.InlineKeyboardButton(text="пол ?! (серьёзно?) ", callback_data="gender")
		keyboard.add(callback_button1,callback_button2,callback_button3,callback_button4,callback_button5)
		bot.send_message(message.chat.id, "что будем обновлять?", reply_markup=keyboard)

		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('update', message.chat.id))
		conn.commit()
	else:
		bot.send_message(message.chat.id,"""тебе нечего обновлять, добавь данные: /add_date""")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "weight":
        	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""введи новый вес""")
        	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('update_w', call.message.chat.id))
        	conn.commit()
        elif call.data == "height":
        	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""введи новый рост""")
        	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('update_h', call.message.chat.id))
        	conn.commit()
        elif call.data == "age":
        	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""введи новый возраст""")
        	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('update_a', call.message.chat.id))
        	conn.commit()
        elif call.data == "struc":
        	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""введи новое телосложение""")
        	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('update_s', call.message.chat.id))
        	conn.commit()
        elif call.data == "gender":
        	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""введи новый пол (ты просто ошибся, когда заполнял данные, да?)""")
        	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('update_a', call.message.chat.id))
        	conn.commit()

@bot.message_handler(func=lambda message: check('update_w',message.chat.id), content_types = ['text'])
def update_2(message):
	curs.execute("UPDATE users SET weight = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Отлично, мы обновили твой вес""")

@bot.message_handler(func=lambda message: check('update_h',message.chat.id), content_types = ['text'])
def update_3(message):
	curs.execute("UPDATE users SET height = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Отлично, мы обновили твой рост""")

@bot.message_handler(func=lambda message: check('update_a',message.chat.id), content_types = ['text'])
def update_4(message):
	curs.execute("UPDATE users SET age = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Отлично, мы обновили твой возраст""")

@bot.message_handler(func=lambda message: check('update_s',message.chat.id), content_types = ['text'])
def update_5(message):
	curs.execute("UPDATE users SET struc = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Отлично, мы обновили твоё телосложение""")

@bot.message_handler(func=lambda message: check('update_g',message.chat.id), content_types = ['text'])
def update_6(message):
	curs.execute("UPDATE users SET gender = %s WHERE user_id = %s;",(message.text, message.chat.id))
	conn.commit()
	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
	conn.commit()
	bot.send_message(message.chat.id,"""Мы обновили твой пол...""")



@bot.message_handler(func = lambda message: True, commands = ['show_date'])
def show1(message):
	if if_NULL(message.chat.id) == False:
		curs.execute("SELECT weight from users WHERE user_id = %s;",(message.chat.id,))
		w = str(curs.fetchone())+' '
		curs.execute("SELECT height from users WHERE user_id = %s;",(message.chat.id,))
		h = str(curs.fetchone())+' '
		curs.execute("SELECT age from users WHERE user_id = %s;",(message.chat.id,))
		a = str(curs.fetchone())+' '
		curs.execute("SELECT gender from users WHERE user_id = %s;",(message.chat.id,))
		g = str(curs.fetchone())+' '
		curs.execute("SELECT struc from users WHERE user_id = %s;",(message.chat.id,))
		c = str(curs.fetchone())+' '
		bot.send_message(message.chat.id,w + h + a + g + c)
	else:
		bot.send_message(message.chat.id,"твои данных ещё не существует, используй /add_date или /update") 

#############################################################################################################

if __name__ == "__main__":
    bot.polling(none_stop=True)


