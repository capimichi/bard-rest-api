from flasgger import Schema, fields


class Message:

    def __init__(self):
        self.text = None

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text