import keyboard

from service.TextProcessor import TextProcessor


class KeyListener:

    def __init__(self):
        self.setup_listener()

    def on_key_event(self, event):
        if event.name == 'b' and keyboard.is_pressed('alt'):
            text_processor = TextProcessor()
            text_processor.action()

    def setup_listener(self):
        keyboard.on_press(self.on_key_event)
        keyboard.wait('insert')
