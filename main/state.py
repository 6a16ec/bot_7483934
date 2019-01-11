import message

class State:
    def __init__(self, number):
        self.number = number

    def start_message(self):
        message.Message.data()







def database_init():
    table = Table("stat")
    table.create(["id", "text", "callback"], ["int(5) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)", "VARCHAR(128)"])
    table.close()

    table = Table("keyboard")
    table.create(["id", "name", "is_inline"], ["int(5) PRIMARY KEY AUTO_INCREMENT", "VARCHAR(128)", "BOOLEAN DEFAULT false"])
    table.close()

    table = Table("bundles")
    table.create(["id_keyboard", "id_prev_button", "id_button", "newline"], ["INT(5)", "INT(5)", "INT(5)", "BOOLEAN DEFAULT false"])
    table.close()

def keyboard_init_data():
    table = Table("buttons")
    table.insert("text", "first-first")
    table.insert("text", "second-first")
    table.insert("text", "second-second")
    table.close()

    table = Table("keyboard")
    table.insert("name", "test")
    table.close()

    table = Table("bundles")
    table.insert(["id_keyboard", "id_prev_button", "id_button", "newline"], [1, 0, 1, 1])
    table.insert(["id_keyboard", "id_prev_button", "id_button"], [1, 1, 2])
    table.insert(["id_keyboard", "id_prev_button", "id_button"], [1, 2, 3])
    table.close()

def keyboard_init_read():
    table = Table("buttons")
    print(table.select_all())
    table.close()

    table = Table("keyboard")
    print(table.select_all())
    table.close()

    table = Table("bundles")
    print(table.select_all())
    table.close()

def keyboard_init_delete():
    table = Table("buttons")
    table.delete_table("Yes")
    table.close()

    table = Table("keyboard")
    table.delete_table("Yes")
    table.close()

    table = Table("bundles")
    table.delete_table("Yes")
    table.close()

