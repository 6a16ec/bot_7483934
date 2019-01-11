import keyboard

class Message:
    def __init__(self, text, reply_kb_now = None, inline_kb_now = None, reply_kb = False, inline_kb = False):
        self.text = text
        self.reply_kb_now = reply_kb_now
        self.inline_kb_now = inline_kb_now
        self.reply_kb = reply_kb
        self.inline_kb = inline_kb
        pass
        self.docs = None

    def data(self):
        pass