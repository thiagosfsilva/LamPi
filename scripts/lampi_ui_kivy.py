from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "LightBlue"  # "Purple", "Red"
        self.theme_cls.theme_style = "Dark"  # "Light"

        screen = Screen()
        screen.add_widget(
            MDRectangleFlatButton(
                text="Hello, World",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )
        return screen


MainApp().run()


#  from types import LambdaType
# import kivy
# from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.dropdown import DropDown
# from kivy.uix.button import Button

# PiDrop = DropDown()
# for index in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
#     btn = Button(text='Pi %d' % index, size_hint_y=None, height=44)
#     btn.bind(on_release=lambda btn: PiDrop.select(btn.text))
#     PiDrop.add_widget(btn)

# class LamPiUi(App):
#     def build(self):
#         return PiDrop

# if __name__ == '__main__':
#     LamPiUi().run()
