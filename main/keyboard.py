from aiogram import types
import db

def func():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("1")
    kb.row("1", "2")
    kb.row("1", "2", "3")
    return kb

def get(kb_name = None, kb_id = None):
    keyboard_table = db.Table("keyboard")
    if(kb_id != None):
        table = keyboard_table.select(["name", "is_inline"], "id", kb_id)
        kb_name, is_inline = table[0]
    elif(kb_name != None):
        table = keyboard_table.select(["id", "is_inline"], "name", kb_name)
        kb_id, is_inline = table[0]
    else:
        keyboard_table.close()
        return
    keyboard_table.close()

    bundles_table = db.Table("bundles")
    bundles = bundles_table.select(["id_button", "id_next_button", "newline"], "id_keyboard", kb_id)
    bundles_table.close()

    button_next = {}; button_newline = {}
    for bundle in bundles:
        id_button, id_next, newline = bundle
        button_next[id_button] = id_next
        button_newline[id_button] = newline

    #
    #
    button_text = {}
    buttons_table = db.Table("buttons")
    if(is_inline == False):
        buttons = buttons_table.select_many_key(["id", "text"], "id", list(button_next.keys()))
    buttons_table.close()

    ### end work with BD
    for button in buttons:
        id, text = button
        button_text[id] = text

    button_id_first = 0
    for button_id in list(button_next.keys()):
        if button_id not in list(button_next.items()):
            button_id_first = button_id
            break

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_id_now = button_id_first
    line = []
    while button_next[button_id_now] != 0:
        if button_newline[button_id_now] == False:
            line.append(button_text[button_id_now])
        else:
            line.append(button_text[button_id_now])
            keyboard.row(*line)
            line = []
        button_id_now = button_next[button_id_now]
    line.append(button_text[button_id_now])
    keyboard.row(*line)

    return keyboard


def to2Array(array):
    if(type(array) is not list): array = [array]
    for i, element in enumerate(array):
        if(type(element) is not list): array[i] = [element]
    return array


def add(array, name = None, is_inline = False):
    array = to2Array(array)

    keyboard_table = db.Table("keyboard")
    if(name != None): keyboard_table.insert(["name", "is_inline"], [name, is_inline])
    else: keyboard_table.insert("is_inline", is_inline)
    keyboard_id = keyboard_table.select_by_max("id", "id")[0][0]
    keyboard_table.close()

    buttons_table = db.Table("buttons")
    id_buttons = []
    for line in array:
        id_buttons_line = []
        for element in line:
            buttons_table.insert("text", element)
            id_button = buttons_table.select_by_max("id", "id")[0][0]
            id_buttons_line.append(id_button)
        id_buttons.append(id_buttons_line)
    buttons_table.close()

    bundles_table = db.Table("bundles", True)
    id_prev = 0
    for id_line in id_buttons:
        for i, id in enumerate(id_line):
            last_in_line = False
            if i == len(id_line) - 1:
                last_in_line = True
            bundles_table.insert(["id_keyboard", "id_prev_button", "id_button", "newline"], [keyboard_id, id_prev, id, last_in_line])
            id_prev = id
    bundles_table.close()

    print(keyboard_id)

def removeReply():
    return types.ReplyKeyboardRemove()








if(__name__ == "__main__"):
    # get(kb_id = 1)

    add([["create"], ["work list", "haos list"], ["settings"]])
    # get(kb_id = 1)

# class commonKeyboard:
# 	def get(name, one_time_keyboard = False):
# 		kb = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = one_time_keyboard)
# 		keyboard = config.keyboards[name]
# 		for line_number in range(len(keyboard)):
# 			kb.row(*keyboard[line_number])
# 		return kb
# 	def close():
# 		return types.ReplyKeyboardRemove()
#
# class messageKeyboard:
# 	def get(name):
# 		kb = types.InlineKeyboardMarkup()
# 		keyboard = config.keyboards[name]
# 		for line_number in range(len(keyboard)):
# 			buttons = []
# 			for button in keyboard[line_number]:
# 				buttons.append(types.InlineKeyboardButton(text = button, callback_data = button))
# 				kb.add(*buttons)
# 		return kb
#
# 		bot.reply_to(message, "Сам {!s}".format(message.text)