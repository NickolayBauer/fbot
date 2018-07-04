from telebot import types
def fkey():

	keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
	add = types.KeyboardButton(text="Добавить данные")
	update = types.KeyboardButton(text = "Обновить мои данные")
	find = types.KeyboardButton(text = "Найти программу")
	show = types.KeyboardButton(text = "Показать мои данные")
	info = types.KeyboardButton(text = "Как пользоваться ботом?")
		
	keyboard.add(add,update,find,show,info)
	return keyboard

