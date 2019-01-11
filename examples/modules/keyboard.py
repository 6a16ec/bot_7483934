from aiogram import types


def toArray(object):
    if type(object) == type([]):
        array = object
    elif type(object) == type("string") or type(object) == type(0):
        array = [object]
    else:
        array = []
    return array


def to2Array(object, toString = False):
    array = toArray(object)

    for i, data in enumerate(array):
        if type(data) == type("string") or type(data) == type(0):
            array = [array]
            break

    if toString == True:
        for i, line in enumerate(array):
            for j, object in enumerate(line):
                if type(object) == type(0):
                    array[i][j] = str(object)

                if type(array[i][j]) != type("string"):
                    print(object, type(object))
                    array = [[]]
                    break

    return array


def reply(array):
    array = to2Array(array, True)
    print(array)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for line in array:
        keyboard.row(*line)

    return keyboard


def remove():
    return types.ReplyKeyboardRemove()



def inline(array, callback = None):
    array = to2Array(array)
    if callback != None:
        callback = to2Array(callback)
    else:
        callback = array

    print(array, callback)

    max_len = len(max(array, key=len))
    keyboard = types.InlineKeyboardMarkup(row_width = max_len)
    for i, line in enumerate(array):
        buttons = []
        for j, text in enumerate(line):
            button = types.InlineKeyboardButton(text = text, callback_data = callback[i][j])
            buttons.append(button)
        print("new line")
        keyboard.add(*buttons)

    return keyboard


if __name__ == "__main__":
    print("ok, hello")
    print(to2Array(None))
    print(to2Array("string"))
    print(to2Array(777))
    print(to2Array([666, 555, 444, "str"]))
    print([[0]])

    print("eeee")
