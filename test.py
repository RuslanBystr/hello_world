from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class CheckUser:
    """Check user in db"""
    def __init__(self, login, password):
        self.__login = login
        self.__password = password

    def Check(self):
        if self.__login and self.__password:
            return True
        return False

    def met(self):
        pass


class MyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gl = GridLayout(cols=1, rows=7)
        self.bl = BoxLayout(orientation='vertical')

        self.login = TextInput()
        self.password = TextInput()

    def build(self):
        self.title = "MyFknApp"

        self.bl.add_widget(Label(text='Login'))
        self.bl.add_widget(self.login)
        self.bl.add_widget(Label(text='Password'))
        self.bl.add_widget(self.password)
        self.bl.add_widget(Button(text='Sign-in'), on_press=CheckUser(self.login, self.password).met)# CheckUser(self.login, self.password).Check
        self.gl.add_widget(self.bl)

        return self.gl

if __name__ == '__main__':
    MyApp().run()