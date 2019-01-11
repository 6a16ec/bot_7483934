import db

def prepare_db():
    buttons_table = db.Table("buttons")
    buttons_table.create(["id", "text", "callback"], ["int(5) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)", "VARCHAR(128)"])
    buttons_table.close()

    keyboard_table = db.Table("keyboard")
    keyboard_table.create(["id", "name", "is_inline"], ["int(5) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)", "BOOLEAN DEFAULT false"])
    keyboard_table.close()

    bundles_table = db.Table("bundles")
    bundles_table.create(["id_keyboard", "id_button", "id_next_button", "newline"], ["INT(5)", "INT(5)", "INT(5)", "BOOLEAN DEFAULT false"])
    bundles_table.close()

def to2Array(array):

    if type(array) is list:
        type_list = [type(element) is list for element in array]

        if True in type_list:
            for i, element in enumerate(array):
                if type(element) is not list:
                    array[i] = [element]
        else:
            array = [array]
    else:
        array = [[array]]
    return array

def add(array, name = None, is_inline = False):

    array = to2Array(array)

    keyboard_table = db.Table("keyboard")
    keyboard_table.insert(["name", "is_inline"], [name, is_inline])
    keyboard_id = keyboard_table.select_by_max("id", "id")[0][0]

    keyboard_table.close()

    buttons_table = db.Table("buttons")
    buttons_ids = []
    for i, line in enumerate(array):
        buttons_ids.append([])
        for j, text in enumerate(line):
            buttons_table.insert("text", text)
            id = buttons_table.select_by_max("id", "id")
            id = id[0][0]
            buttons_ids[i].append(id)

    buttons_table.close()

    bundles_table = db.Table("bundles", True)

    for i, line in enumerate(buttons_ids):
        for j, id in enumerate(line):
            if j < len(line) - 1:
                newline = False
                next_id = line[j+1]
            else:
                if i < len(buttons_ids) - 1:
                    newline = True
                    next_id = buttons_ids[i+1][0]
                else:
                    newline = False
                    next_id = 0
            bundles_table.insert(["id_keyboard", "id_button", "id_next_button", "newline"], [keyboard_id, id, next_id, newline])

    bundles_table.close()

    print(keyboard_id)


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

if __name__ == "__main__":
    # prepare_db()
    add([["1", "2", "3"], ["4444"]])


    import mysql.connector as mariadb
    import config


    # def keyboard_init_data():
    #     table = Table("buttons")
    #     table.insert("text", "first-first")
    #     table.insert("text", "second-first")
    #     table.insert("text", "second-second")
    #     table.close()
    #
    #     table = Table("keyboard")
    #     table.insert("name", "test")
    #     table.close()
    #
    #     table = Table("bundles")
    #     table.insert(["id_keyboard", "id_prev_button", "id_button", "newline"], [1, 0, 1, 1])
    #     table.insert(["id_keyboard", "id_prev_button", "id_button"], [1, 1, 2])
    #     table.insert(["id_keyboard", "id_prev_button", "id_button"], [1, 2, 3])
    #     table.close()
    #
    #
    # def keyboard_init_read():
    #     table = Table("buttons")
    #     print(table.select_all())
    #     table.close()
    #
    #     table = Table("keyboard")
    #     print(table.select_all())
    #     table.close()
    #
    #     table = Table("bundles")
    #     print(table.select_all())
    #     table.close()
    #
    #
    # def keyboard_init_delete():
    #     table = Table("buttons")
    #     table.delete_table("Yes")
    #     table.close()
    #
    #     table = Table("keyboard")
    #     table.delete_table("Yes")
    #     table.close()
    #
    #     table = Table("bundles")
    #     table.delete_table("Yes")
    #     table.close()
    #
    #
    # def test():
    #     table = Table("buttons")
    #     print(table.select_by_max("*", "id"))
    #     table.close()
    #
    #
    # # if(__name__ == "__main__"): example()
    #
    # ### keyboard ###
    #
    # # if(__name__ == "__main__"): keyboard_init()
    # # if(__name__ == "__main__"): keyboard_init_data()
    # # if(__name__ == "__main__"): keyboard_init_read()
    # #
    #
    # if (__name__ == "__main__"):
    #     keyboard_init()
    #     keyboard_init_data()
    #     keyboard_init_read()
    #
    # # if(__name__ == "__main__"): keyboard_init_delete()
    #
    # ### keyboard ###
    #
    # # if(__name__ == "__main__"): test()







