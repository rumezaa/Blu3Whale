#mainimports

import json
import kivy
import kivymd
import weakref

import plyer
from kivy.app import App



#utils
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from backend_kivyagg import FigureCanvasKivyAgg

#widgets
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage,Image
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.imagelist import SmartTileWithLabel
from kivy.uix.videoplayer import VideoPlayer
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextFieldRound
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.core.window import Window


#backend
from plyer import notification as n

from notes_blu3.note_saver import Notes
from wellness_processor_blu3.wellness_db import WellnessTrack
from user_login_blu3.user_auth import UserLogin
from recipie_finder_blu3.recipe import RecipeFinder
import matplotlib.pyplot as plt
import numpy as np


Window.size = (380,580)




#stuff
class Content(MDBoxLayout):
    pass
class Recipe(MDGridLayout):
    pass
class Scroll(ScrollView):
    pass
class View(SmartTileWithLabel):
    pass
class Ingred(Label):
    pass
class Instrucs(Label):
    pass




#developing dialog for choosing tracking categories
class Categories(OneLineAvatarIconListItem):
    divider = None

    def set_check(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
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
        self.username = self.ids.username.text
        password = self.ids.user_password.text
        login_info = UserLogin(self.username,password)
        signed_in=login_info.sign_in()
        #clear inputs

        if signed_in==True:
            self.parent.current="Home"


# for updating user's password
class ForgotScreen(Screen):
    def forgot_pass(self):
        #collect user info
        username = self.ids._username.text
        email = UserLogin(username,"").get_email()



        new_pass = self.ids.new_password.text
        try:
            new_info= UserLogin(username,"",email).change_pass(new_pass)

        # clear inputs
            self.ids._username.text = ""
            self.ids.new_password.text = ""

        #go to homescreen
            self.parent.current = "Home"
        except:
            print("username incorrect")


#carries our basic graph funcs
class HomeScreen(Screen):

    def customize(self,user):
        self.user = user


        if UserLogin(self.user, "").get_newusers() == [True]:

            self.show_tracker(self.user)

        elif UserLogin(user, "").get_newusers() == [False]:

            self.create_tracker(self.user)
    #for past users
    def show_tracker(self,user):
        self.username = user
        graph_data = list(WellnessTrack(self.user).create_visual())
        headers = graph_data[1]
        data_set = graph_data[0]


        fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(aspect="equal"))

        #meta data
        wedges, texts  = ax.pie(data_set,textprops=dict(color="w"))

        #initiating the legend
        ax.legend(wedges, headers,
                  title="KEY",
                  loc="center",
                  prop={'size': 7}
                  )
        fig.set_facecolor('#eeeeee')

        #making the donut graph
        circ = plt.Circle((0, 0), 0.70, fc='#eeeeee')
        fig = plt.gcf()

        # Adding Circle in Pie chart
        fig.gca().add_artist(circ)

        ax.set_title(f"{self.username} - your doing great!")
        #create the graph


        plt.axis("equal")

        self.ids.create_graph.clear_widgets()
        self.ids.create_graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        b=MDIconButton(icon="plus-circle-outline" )
        b.bind(on_press =lambda x:self.update_tracker(self.user,headers))




        self.ids.create_graph.add_widget(b)

    #for new users
    def create_tracker(self,user):
        self.ids.create_graph.clear_widgets()
        new_graph = MDIconButton(icon="plus-circle-outline")
        new_graph.bind(on_press= lambda x: self.new_track(user))
        self.ids.create_graph.add_widget(new_graph)

    #for selecting the tracking categories
    def new_track(self,user):
        dialog=MDDialog(title="Choose Categories",
                type="confirmation",
                items=[
                    Categories(text="meals_eaten"),
                    Categories(text="activity"),
                    Categories(text="water_intake")])
        dialog.open()


        # WellnessTrack(user).create_DB()



    #for updating the user's graph
    def update_tracker(self,user,categories):
        self.user = user
        self.categories = categories

        #getting user's categories
        cat_1 = MDTextField(hint_text=self.categories[0])
        cat_2 = MDTextField(hint_text=self.categories[1])
        cat_3 = MDTextField(hint_text=self.categories[2])
        cat_4 = MDTextField(hint_text=self.categories[3])

        #adding widgets to the card
        self.ids.create_graph.add_widget(cat_1)
        self.ids.create_graph.add_widget(cat_2)
        self.ids.create_graph.add_widget(cat_3)
        self.ids.create_graph.add_widget(cat_4)




        #making submit button --- gets text input
        submit = MDFillRoundFlatButton(text="submit",pos_hint= {"center_x":0.5,"center_y":0.5})
        submit.bind(on_press = lambda x: self.add(self.user,
                                                  cat_1.text,
                                                  int(cat_2.text),
                                                  int(cat_3.text),
                                                  int(cat_4.text)))

        #adding widget to th ecard
        self.ids.create_graph.add_widget(submit)



    #updating our graph data with user input
    def add(self,user,cat_1,cat_2,cat_3,cat_4):

        WellnessTrack(user).update_DB(cat_1,cat_2,cat_3,cat_4)
        self.ids.create_graph.clear_widgets()
        self.show_tracker(user)


class Note(Screen):
    def load_notes(self,username):
        try:
            n.notify(
                title="HEADING HERE",
                message=" DESCRIPTION HERE",

                # displaying time
                timeout=2
            )

            #load user prev notes an dshow on screen
            notes = Notes(username).load_notes()
            self.ids.user_text.text = notes
        except:
            self.ids.user_text.text = ""
            print("No notes found")





    def add_notes(self,username):
        try:
            #check if user in data
            Notes(username).update_notes(self.ids.user_text.text)
        except:
            #if not in data add them to data
            Notes(username,self.ids.user_text.text).add_notes()

class Notify(Screen):
    def choose_time(self):
        interval_amount = int(self.ids.int_set.text)
        interval_time = int(self.ids.time_set.text)
        to_secs = interval_time*60
        Clock.schedule_interval(self.reminder_set, to_secs)



    def reminder_set(self,*args):

        n.notify(
            title="HEADING HERE",
            message=" DESCRIPTION HERE",

            # displaying time
            timeout=2
        )



#for searching recipies -NOTE ADD AUTOMATIC SCROLL TO TOP -
class Search(Screen):
    def get_search(self):
        self.input = self.ids.search_input.text
        #scroll to top after new search
        self.ids.scrollview.scroll_y = 1

        if self.input != ():
            #checking to see if query is a NoneType
            try:
                #call to recpe finder class to initiate API
                data = RecipeFinder(self.input).get_info()
                self.length = len(data["MEAL_NAMES"])
                self.titles = data["MEAL_NAMES"]
                self.ingred = data["MEAL_INGREDS"]
                self.instrucs = data["MEAL_INSTRUCS"]
                self.img = data["IMAGES"]
                self.vids = data["VIDEOS"]
                self.ids.recipe_view.clear_widgets()


                #add widgets based of extracted widgets
                for add in range(self.length):
                    print("working")
                    View.source = f"{self.img[add]}"
                    View.markup = True
                    View.text = f"[size=26]{self.titles[add]}[/size]"
                    Instrucs.text = f"INSTRUCTIONS:\n{self.instrucs[add]}"
                    self.ids.recipe_view.add_widget(View())

                    self.ids.recipe_view.add_widget(MDLabel(markup=True,text=f"INGREDIENTS:\n[size=9sp]{self.ingred[add]}[/size]"))

                    self.ids.recipe_view.add_widget(MDLabel(markup=True,text=f"INSTRUCTIONS:\n[size=10sp]{self.instrucs[add]}[/size]"))

            #if query is a nonetype display error
            except:
                self.ids.recipe_view.clear_widgets()

                self.ids.recipe_view.add_widget(MDLabel(text=f"No results found for {self.input}",
                                                        pos_hint= {"center_x":0.5,"center_y":0.5}))
#other stuff
class TabManager(ScreenManager):
    pass
class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    def search(self):
        pass





class blu3whaleApp(MDApp):
    def set_screen(self,screen):
        self.root.current = screen

    def build(self):



        return Builder.load_file("GUI.kv")


blu3whaleApp().run()