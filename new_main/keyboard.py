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
            array[i] = [data]

    if toString == True:
        for i, line in enumerate(array):
            for j, object in enumerate(line):
                if type(object) == type(0):
                    array[i][j] = str(object)

                if type(array[i][j]) != type("string"):
                    # print(object, type(object))
                    array = [[]]
                    break

    return array


def reply(array, one_time_keyboard = False, resize_keyboard = True):
    array = to2Array(array, True)

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)

    for line in array:
        keyboard.row(*line)

    return keyboard


def remove():
    return types.ReplyKeyboardRemove()

def force_reply():
    return types.ForceReply()

def url(text, url):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=text, url=url))
    return keyboard


def inline(array, callback = None):
    array = to2Array(array)
    if callback != None:
        callback = to2Array(callback)
    else:
        callback = array

    # print(array, callback)

    max_len = len(max(array, key=len))
    keyboard = types.InlineKeyboardMarkup(row_width = max_len)
    for i, line in enumerate(array):
        buttons = []
        for j, text in enumerate(line):
            button = types.InlineKeyboardButton(text = text, callback_data = callback[i][j])
            buttons.append(button)
        # print("new line")
        keyboard.add(*buttons)

    return keyboard

def test():
    k = []
    for ind, (code, extension, resolution) in enumerate(self.formats):
        k.append([InlineKeyboardButton("{0}, {1}".format(extension, resolution),
                                       callback_data="{} {}".format(code, self.link))])
    kb = InlineKeyboardMarkup().add(k)