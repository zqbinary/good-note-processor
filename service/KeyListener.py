import keyboard

from service.TextProcessor import TextProcessor


class KeyListener:

    def __init__(self):
        self.setup_listener()

    def action_ai(self):
        text_processor = TextProcessor()
        text_processor.action('ai')
        pass

    def on_key_event(self, event):
        print(event, event.name, keyboard.is_pressed('right alt'))
        print('=======')

    def action_man(self):
        text_processor = TextProcessor()
        text_processor.action()

    def setup_listener(self):
        # keyboard.on_press(self.on_key_event)

        keyboard.add_hotkey(keyboard.get_hotkey_name(['alt', 'b']), self.action_man)
        keyboard.add_hotkey(keyboard.get_hotkey_name(['alt', '<']), self.action_ai)
        keyboard.wait('insert')
