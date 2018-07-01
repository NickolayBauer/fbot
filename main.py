import telebot
from telebot import types
import psycopg2
import os
import json
conn = psycopg2.connect(host='',
                        dbname='',
                        user='',
                        password='')
curs = conn.cursor()


bot = telebot.TeleBot("")

####################################находится ли id в определённом состоянии################################
def check(conditions, my_id):
	try:
		curs.execute("SELECT cond FROM users WHERE user_id = %s;",(my_id,))	
		if (curs.fetchall()[0][0]) == conditions:
			return True
	except:
		pass

	return False
##################################есть ли данные###########################################################
def if_NULL(my_id):
	try:
		curs.execute("SELECT struc FROM users WHERE user_id = %s;",(my_id,))
		if curs.fetchone()[0] == '':
			return True
	except:
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
@bot.message_handler(func=lambda message:  True, commands=['add_date'])
def add_date1(message):
	if if_NULL(message.chat.id) == True:
		bot.send_message(message.chat.id,"""следующее твоё сообщение будет добавлено в базу данных\nВведи вес: """)
		curs.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s);",([message.chat.id,'NULL','NULL','NULL','NULL','NULL','weight']))
		conn.commit()
	else:
		bot.send_message(message.chat.id,"твои данные уже существуют, используй /update")


@bot.message_handler(func=lambda message: check('weight',message.chat.id), content_types = ['text'])
def add_date2(message):
	if message.text.isdecimal() == True:
		#тут нужно сделать проверку на нормальность данных
		curs.execute("UPDATE users SET weight = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('height', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""Окей, теперь введи рост""")
	else:
		bot.send_message(message.chat.id,"""Просто введи цифру""")

@bot.message_handler(func=lambda message: check('height',message.chat.id), content_types = ['text'])
def add_date3(message):
	if message.text.isdecimal() == True:
		#тут нужно сделать проверку на нормальность данных
		curs.execute("UPDATE users SET height = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('age', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""Окей, теперь введи возраст""")
	else:
		bot.send_message(message.chat.id,"""Просто введи цифру""")
@bot.message_handler(func=lambda message: check('age',message.chat.id), content_types = ['text'])
def add_date4(message):
	if message.text.isdecimal() == True:
		#тут нужно сделать проверку на нормальность данных
		curs.execute("UPDATE users SET age = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('gender', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""Окей, теперь введи свой пол - М или Ж""")
	else:
		bot.send_message(message.chat.id,"""Просто введи цифру""")

@bot.message_handler(func=lambda message: check('gender',message.chat.id), content_types = ['text'])
def add_date5(message):
	if message.text in ['М','Ж']:
		#тут нужно сделать проверку на нормальность данных
		curs.execute("UPDATE users SET gender = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('struc', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""окей теперь укажи телосложение - Эктоморф, Мезоморф или Эндоморф""")
	else:
		bot.send_message(message.chat.id,"""Введи данные правильно \n- М или Ж  """)

@bot.message_handler(func=lambda message: check('struc',message.chat.id), content_types = ['text'])
def add_date6(message):
	if message.text in ['Эктоморф','Мезоморф','Эндоморф']:
	#тут нужно сделать проверку на нормальность данных
		curs.execute("UPDATE users SET struc = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""Готово, все твои данные созданы, ты можешь посмотреть их командой /show_date """)
	else:
		bot.send_message(message.chat.id,"""Введи данные правильно \n- Эктоморф, Мезоморф или Эндоморф""")

# #################################обновление даннных в бд###################################################
@bot.message_handler(func=lambda message:  True , commands=['update'])
def update1(message):
	if exist(message.chat.id) == True:

		keyboard = types.InlineKeyboardMarkup()
		callback_button1 = types.InlineKeyboardButton(text="вес", callback_data="weight")
		callback_button2 = types.InlineKeyboardButton(text="рост", callback_data="height")
		callback_button3 = types.InlineKeyboardButton(text="возраст", callback_data="age")
		callback_button4 = types.InlineKeyboardButton(text="телосложение", callback_data="struc")
		callback_button5 = types.InlineKeyboardButton(text="пол ?! (серьёзно?) ", callback_data="gender")
		callback_button6 = types.InlineKeyboardButton(text="ничего", callback_data="zero")
		keyboard.add(callback_button1,callback_button2,callback_button3,callback_button4,callback_button5,callback_button6)
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
        	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('update_g', call.message.chat.id))
        	conn.commit()
        elif call.data == "zero":
        	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""Окей, что-то ещё?""")
        	curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', call.message.chat.id))
        	conn.commit()	

@bot.message_handler(func=lambda message: check('update_w',message.chat.id), content_types = ['text'])
def update_2(message):
	if message.text.isdecimal() == True:
		curs.execute("UPDATE users SET weight = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""Отлично, мы обновили твой вес""")
	else:
		bot.send_message(message.chat.id,"""Просто введи цифру""")
@bot.message_handler(func=lambda message: check('update_h',message.chat.id), content_types = ['text'])
def update_3(message):
	if message.text.isdecimal() == True:
		curs.execute("UPDATE users SET height = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""Отлично, мы обновили твой рост""")
	else:
		bot.send_message(message.chat.id,"""Просто введи цифру""")

@bot.message_handler(func=lambda message: check('update_a',message.chat.id), content_types = ['text'])
def update_4(message):
	if message.text.isdecimal() == True:
		curs.execute("UPDATE users SET age = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""Отлично, мы обновили твой возраст""")
	else:
		bot.send_message(message.chat.id,"""Просто введи цифру""")
		
@bot.message_handler(func=lambda message: check('update_s',message.chat.id), content_types = ['text'])
def update_5(message):
	if message.text in ['Эктоморф','Мезоморф','Эндоморф']:
		curs.execute("UPDATE users SET struc = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""Отлично, мы обновили твоё телосложение""")
	else:
		bot.send_message(message.chat.id,"""Введи данные правильно \n- Эктоморф, Мезоморф или Эндоморф""")

@bot.message_handler(func=lambda message: check('update_g',message.chat.id), content_types = ['text'])
def update_6(message):
	if message.text in ['М','Ж']:
		curs.execute("UPDATE users SET gender = %s WHERE user_id = %s;",(message.text, message.chat.id))
		conn.commit()
		curs.execute("UPDATE users SET cond = %s WHERE user_id = %s;",('zero', message.chat.id))
		conn.commit()
		bot.send_message(message.chat.id,"""Мы обновили твой пол...""")
	else:
		bot.send_message(message.chat.id,"""Введи данные правильно \n- М или Ж  """)



@bot.message_handler(func = lambda message: True, commands = ['show_date'])
def show1(message):
	if if_NULL(message.chat.id) == False:
		curs.execute("SELECT weight, height, age, gender, struc from users WHERE user_id = %s;",(message.chat.id,))
		date = curs.fetchone()
		bot.send_message(message.chat.id,"Твои данные:\n\n"+"вес: "+str(date[0])+"\n"+"рост: "+str(date[1])+"\n"+"возраст: "+str(date[2])+"\n"+"пол: "+str(date[3])+"\n"+
										 "телосложение: "+str(date[4])+"\n")
	else:
		bot.send_message(message.chat.id,"твои данных ещё не существует, используй /add_date или /update") 



@bot.message_handler(func=lambda message:  check('zero',message.chat.id), commands=['find_program'])
def find_program(message):
	curs.execute("SELECT gender, struc from users WHERE user_id = %s;",(message.chat.id,))
	date = curs.fetchone()
	json_date  = []

	path_to_json = 'prog/'+date[0]+"/"+date[1]+"/"
	if  os.listdir(path_to_json) !=[]:
		json_files = [ x for x in os.listdir(path_to_json) if x.endswith("json") ]
		json_data = list()
		for json_file in json_files:
			json_file_path = os.path.join(path_to_json, json_file)
			with open (json_file_path, "r", encoding='utf-8') as f:
				bot.send_message(message.chat.id,  json.load(f)['text'])
	else:
		bot.send_message(message.chat.id,"Пока для таких параметров нет программы, попробуй использовать что-то ещё")

	"""keyboard = types.InlineKeyboardMarkup()
		callback_button1 = types.InlineKeyboardButton(text="следующая", callback_data="next")
		callback_button2 = types.InlineKeyboardButton(text="предыдущая", callback_data="undo")
		keyboard.add(callback_button1,callback_button2)
		bot.send_message(message.chat.id, list_program, reply_markup=keyboard)
	"""

#############################################################################################################
#добавить корректный ввод с помощью инлайн клавиатур
#Добавить статистику прогресса из json-бэкапов

if __name__ == "__main__":
    bot.polling(none_stop=True)


