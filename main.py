import matplotlib.pyplot as plt
import kivy.garden.matplotlib.backend_kivyagg as file

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from user_login_blu3.user_auth import UserLogin





#let user create an account
class SignUpScreen(Screen):
    def signUp(self):
        #get input data
        email = self.ids.add_email.text
        username =self.ids.add_username.text
        password = self.ids.add_user_password.text

        if (email and username and password) != '':

            #call to signup
            signup_info=UserLogin(username,password,email)
            signup_info.sign_up()
            #clear inputs
            self.ids.add_email.text = ""
            self.ids.add_username.text = ""
            self.ids.add_user_password.text = ""
            self.parent.current = "Home"
#let user login
class LoginScreen(Screen):
    def login(self):


        # retrieve user info
        username = self.ids.username.text
        password = self.ids.user_password.text
        login_info = UserLogin(username,password)
        signed_in=login_info.sign_in()
        #clear inputs
        self.ids.username.text = ""
        self.ids.user_password.text = ""
        if signed_in==True:
            self.parent.current="Home"

# for updating user's password
class ForgotScreen(Screen):
    def forgot_pass(self):
        #collect user info
        username = self.ids._username.text
        email = "".join(UserLogin(username,"").get_email())

        new_pass = self.ids.new_password.text
        new_info= UserLogin(username,"",email).change_pass(new_pass)

        # clear inputs
        self.ids._username.text = ""
        self.ids.new_password.text = ""

        #go to homescreen
        self.parent.current = "Home"




class HomeScreen(Screen):
    pass
class TabManager(ScreenManager):
    pass
class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class blu3whaleApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette ="DeepPurple"
        return Builder.load_file("GUI.kv")


blu3whaleApp().run()