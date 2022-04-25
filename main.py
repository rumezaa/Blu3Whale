#mainimports
import os
import json
import kivy
import kivymd
import plyer
import requests
from kivy import utils




#utils
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from garden_matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt


#widgets
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, CheckboxLeftWidget
from kivymd.uix.list import IconRightWidget
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage,Image
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextFieldRound
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.uix.banner import MDBanner

#backend
from plyer import notification as n
from chat_blu3.chat import Chat_Data
from user_goals_blu3.goals import Goals
from notes_blu3.note_saver import Notes
from wellness_processor_blu3.wellness_db import WellnessTrack
from user_login_blu3.user_auth import UserLogin
from recipie_finder_blu3.recipe import RecipeFinder
import numpy as np

import certifi

os.environ['SSL_CERT_FILE'] = certifi.where()

#setting our window size
Window.size = (380,580)




#widgets
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


            info = signup_info.sign_up()

            if info==True:
                # switch to login screen
                submit = MDFillRoundFlatButton(text="login", pos_hint={"center_x": 0.5, "center_y": 0.5})
                submit.bind(on_press=lambda x: self.go_to_login() )
                d = MDDialog(title="Account Created!",text="please login to your account", buttons=[submit])
                d.open()
                self.ids.add_email.text = ""
                self.ids.add_username.text= ""
                self.ids.add_user_password.text= ""


            if info==False:
                self.ids.add_username.hint_text = "username is in use!"
    #for seeing and unseeing password
    def see_pass(self):
        if self.ids.add_user_password.password == True:
            self.ids.add_user_password.password = False
            self.ids.show_pass.icon = "eye"

        else:
            self.ids.add_user_password.password = True
            self.ids.show_pass.icon = "eye-off"

    def go_to_login(self):
        self.parent.current= "Login"

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
            with open("session.json", "r") as file:
                data = json.load(file)

            self.sesh = {"USER": self.username,
                         "PASSW": password}
            data["UserSession"].append(self.sesh)

            with open("session.json", "w") as wfile:
                json.dump(data, wfile)

            self.parent.current="Home"
            self.ids.user_password.text = ""

        elif signed_in==False:
            p = MDDialog(title="Parameter Error", text="the password/username you entered is incorrect")
            p.open()

    #for seeing and unseeing password
    def see_pass(self):
        if self.ids.user_password.password == True:
            self.ids.user_password.password = False
            self.ids.show_pass.icon = "eye"

        else:
            self.ids.user_password.password = True
            self.ids.show_pass.icon = "eye-off"


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
            self.manager.get_screen("Login").ids.username.text = self.ids._username.text
            self.ids._username.text = ""
            self.ids.new_password.text = ""

        #go to homescreen
            self.parent.current = "Home"
        except:
            print("username incorrect")
    #for seeing and unseeing password
    def see_pass(self):
        if self.ids.new_password.password == True:
            self.ids.new_password.password = False
            self.ids.show_pass.icon = "eye"

        else:
            self.ids.new_password.password = True
            self.ids.show_pass.icon = "eye-off"


#carries our basic graph funcs
class HomeScreen(Screen):
    #info screen
    def info(self):
        triggers = MDFloatingActionButton(
                        icon= "alert-decagram-outline",
                        md_bg_color= utils.get_color_from_hex("#ffffa1"))
        community = MDFloatingActionButton(
                        icon= "account-heart",
                        md_bg_color= utils.get_color_from_hex("#efc5b1"),
                        )

        whale = MDFloatingActionButton(
                        icon= "human-male-child",
                        md_bg_color= utils.get_color_from_hex("#BABAFF"))

        triggers.bind(on_press=lambda x: self.trigs())
        community.bind(on_press = lambda x: self.community())
        whale.bind(on_press = lambda x: self.whale())


        d = MDDialog(title="Library",buttons=[triggers,community,whale])

        d.open()

    #checks whether the user is new
    def customize(self,user):
        self.user = user


        if UserLogin(self.user, "").get_newusers() == [True]:

            self.show_tracker(self.user)

        elif UserLogin(user, "").get_newusers() == [False]:

            self.create_tracker(self.user)

    #for past users
    def show_tracker(self,user):

        try:
            self.username = user

            #get the previous data
            graph_data = list(WellnessTrack(self.user).create_visual())


            self.ids.flat.clear_widgets()
            #getting the categories and the data set
            data_set = graph_data[0]
            headers = graph_data[1]

            #getting the user's area of growth and expetise
            achievement = graph_data[2]
            work_on = graph_data[3]

            color_theme = ("#ffb3ba","#ffffba","#baffc9","#bae1ff")

            fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(aspect="equal"))

            #meta data
            wedges, texts  = ax.pie(data_set,textprops=dict(color="w"),colors=color_theme)

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

            #add our growth widget
            banner = MDLabel(pos_hint={"center_x": .65, "center_y": .25},markup= True)
            banner.text = f"Hey {self.user}!\n[size=12]you've been growing in {achievement}\nwe see your growth in {work_on}, keep going![/size]"

            self.ids.flat.clear_widgets()
            self.ids.flat.add_widget(banner)

            #for updating the graph
            b = MDIconButton(icon="plus-circle-outline")
            b.bind(on_press=lambda x: self.update_tracker(self.user, headers, banner))
            self.ids.create_graph.add_widget(b)



        except:
            self.ids.flat.clear_widgets()
            self.ids.create_graph.clear_widgets()
            self.ids.create_graph.add_widget(MDLabel(text="There was an Error :("))


    #for new users
    def create_tracker(self, user):
        self.ids.flat.clear_widgets()
        self.ids.create_graph.clear_widgets()
        self.ids.create_graph.add_widget(MDLabel(text="No graph found, try adding some data!"))
        new_graph = MDIconButton(icon="plus-circle-outline")
        new_graph.bind(on_press=lambda x: self.new_track())
        self.ids.create_graph.add_widget(new_graph)

        #for selecting the tracking categories

    #swithing to creation
    def new_track(self):
        self.parent.current = "makeTracker"

    #for updating the user's graph
    def update_tracker(self,user,categories,instance=None):
        try:
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
                                                  cat_2.text,
                                                  cat_3.text,
                                                  cat_4.text))

            #adding widget to the card
            self.ids.create_graph.add_widget(submit)
            self.ids.flat.remove_widget(instance)

        except:
            self.ids.create_graph.clear_widgets()
            self.show_tracker(user)

    # updating our graph data with user input
    def add(self,user,cat_1,cat_2,cat_3,cat_4):
        try:
            WellnessTrack(user).update_DB(cat_1,cat_2,cat_3,cat_4)
        except:
            d = MDDialog(title="invalid data inputted", text="please enter your data as a number or yes/no (excluding the mood)")
            d.open()
        self.ids.create_graph.clear_widgets()
        self.show_tracker(user)

    #info on ED triggers
    def trigs(self):
        b = MDRaisedButton(text="close",md_bg_color= utils.get_color_from_hex("#ffffa1"))
        b.bind(on_press=lambda x: self.close(d))
        d = MDDialog(title="Take a 3 step approach in learning about your triggers:", text="1.IDENTIFY\nIdentify your "
                                                                                           "triggers and the adverse "
                                                                                           "affects\n'What happens "
                                                                                           "that makes me "
                                                                                           "____'\n\n2.REASON\nHow "
                                                                                           "would you come about "
                                                                                           "these situations if they "
                                                                                           "were not "
                                                                                           "triggers?\n\n3.APPLY"
                                                                                           "\nStarting small, "
                                                                                           "but building up to "
                                                                                           "overcoming triggers. Use "
                                                                                           "resources such as our "
                                                                                           "built in tracker to track "
                                                                                           "your progressive response "
                                                                                           "to triggers\n you CAN do "
                                                                                           "this!",
                     buttons=[b], radius=[20, 7, 20, 7])


        d.open()

    #info on building a community for a support
    def community(self):
        b = MDRaisedButton(text="close",md_bg_color= utils.get_color_from_hex("#efc5b1"))
        b.bind(on_press=lambda x: self.close(d))
        d = MDDialog(title="Find People Who Support You",
                     text="Depending on your preference, you may find ease and motivation in your journey with the "
                          "help of others acting as your support. It's important to surround yourself with individuals "
                          "who brig positivity and support towards you.\n\nYour ED does not define your "
                          "capabilities\n\nOnline support groups, or social media are a great way to find people who "
                          "have\\are experiencing the same thing as you\n\n Alternatively, we have provided you with a "
                          "community feature in the app, where you may be able to create connections with others",
                     buttons=[b], radius=[20, 7, 20, 7])
        d.open()

    #info on our role
    def whale(self):
        b = MDRaisedButton(text="close",md_bg_color= utils.get_color_from_hex("#BABAFF"))
        b.bind(on_press=lambda x: self.close(d))
        r = MDRaisedButton(text="give feedback",md_bg_color= utils.get_color_from_hex("#BABAFF"))
        r.bind(on_press=lambda x: self.feedback(), on_release= lambda x: self.close(d))

        d = MDDialog(title="What We Can Do",
                     text="Your wellness and overall experience is the most important factor. By sharing your "
                          "experience with us, we can not only to create a better and more "
                          "inclusive app, but rather improve your journey with the app as well "
                          "\n\nBy understanding that every journey is unique, "
                          "you can customize and put your needs first in your road to recovery\n\nAdditionally, "
                          "you may provide us with feedback to better our application!",
                     buttons=[b,r], radius=[20, 7, 20, 7])
        d.open()

    #switch to feedback screen
    def feedback(self):
        self.parent.current = "feedback"

    def close(self,button):
        button.dismiss()

#screen for creating a new tracker for new users
class Make_Tracker(Screen):
    # for built in categories
    def user_submit(self,user):
        #all the built in categories
        check_list = { self.ids.check_11 : self.ids.check_1,
                       self.ids.check_22: self.ids.check_2,
                       self.ids.check_33: self.ids.check_3,
                       self.ids.check_44: self.ids.check_4,
                       self.ids.check_55:self.ids.check_5}

        #compile all the chosen categories
        li = [v.text for v in check_list if check_list[v].active==True]


        try:
            #get the three categories
            cat_1 = li[0]
            cat_2 = li[1]
            cat_3 = li[2]


            #make the user's data base
            WellnessTrack(user).create_DB(cat_1,cat_2,cat_3)

            try:
                UserLogin(user, "").change_newusers()
                self.parent.current = "Home"
            except:
                print("errors")
        except:
            print("errors")


    #for custom user categories
    def submit(self,user):
        #get the innput text
        cat_1= self.ids.cust_1.text
        cat_2= self.ids.cust_2.text
        cat_3= self.ids.cust_3.text

        #create the data base
        WellnessTrack(user).create_DB(cat_1,cat_2,cat_3)
        try:
            UserLogin(user, "").change_newusers()
            self.parent.current = "Home"
        except:
            print("errors")

#screen for giving feedback
class FeedBack(Screen):
    def feedback(self):

        try:
            #email response
            msg_stuff = self.ids.feedback.text
            url = "https://blu3whalefeedback-5d325-default-rtdb.firebaseio.com/.json"

            #sending the feedback
            requests.post(url = url, json = {'user':msg_stuff})

            self.ids.feedback.text=""
            d = MDDialog(title="Feedback sent!", text="please contact blu3whalebusiness@gmail.com\nfor any pressing concerns")
            d.open()

        except:
            b = MDDialog(title = "There was an Error Processing Your Request")
            b.open()

#for letting user create personal notes
class Note(Screen):
    def load_notes(self,username):
        try:
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
            print("error")

#for setting timers for meal time
class Notify(Screen):
    def choose_time(self):

        interval_time = int(self.ids.time_set.text)

        b = MDRaisedButton(text="close")
        notice = MDDialog(title="Reminder set!",text=f"please keep the application open in your tabs. You will be reminded every {interval_time} hour(s)", buttons=[b])

        b.bind(on_press=lambda x: notice.dismiss())
        notice.open()
        to_secs = interval_time*60*60
        Clock.schedule_interval(self.reminder_set, to_secs)



    def reminder_set(self,*args):

        n.notify(
            title="Hey? What's cooking?",
            message="dear user this is your gentle reminder for meal time\nwe are so proud of you!",

            # displaying time
            timeout=2
        )

#for settig goals
class Goal(Screen):
    def load_goals(self,user):
        try:
            self.ids.layout.clear_widgets()
            self.ids.list.clear_widgets()
            #retrieve the user's goals if they have any
            goals = Goals(user).load_goals()


            #iterate over list and make goals appear as list ites
            for i,v in enumerate(goals):
                remover = IconLeftWidget(icon="check-bold")


                #for removing goals
                remover.bind(on_press= lambda x: Goals(user).remove_goals(item.text))
                item = OneLineIconListItem(text=v)
                item.add_widget(remover)
                self.ids.list.add_widget(item)

            b = MDIconButton(icon="plus-circle-outline")
            b.bind(on_press = lambda x: self.update_goals(user))
            self.ids.layout.add_widget(b)

        except:
            d=MDDialog(text="No Goals Found, try adding!")
            d.open()
            b = MDIconButton(icon="plus-circle-outline")
            b.bind(on_press=lambda x: self.add_goals(user))
            self.ids.layout.add_widget(b)

    #NEW USER'S
    def add_goals(self,user):
        #for adding goals
        content = Content()
        new_goal = MDTextField(hint_text="enter a your new goal",multiline=True)

        content.add_widget(new_goal)

        b = MDRaisedButton(text="add")
        b.bind(on_press=lambda x: Goals(user, new_goal.text).add_goals(), on_release=lambda x: dialog.dismiss())

        dialog = MDDialog(type="custom", content_cls=content, buttons=[
            b
        ])
        dialog.open()


    #FOR ADDING goals for PAST USERS
    def update_goals(self,user):
        content = Content()
        new_goal = MDTextField(hint_text="enter a your new goal",multiline=True)
        content.add_widget(new_goal)

        b = MDRaisedButton(text="add")
        close = MDRaisedButton(text="close")
        close.bind(on_press= lambda x: dialog.dismiss())


        b.bind(on_press=lambda x: Goals(user,new_goal.text).update_goals(), on_release=lambda x: dialog.dismiss())

        dialog = MDDialog(title="Add a new goal", type="custom", content_cls = content, buttons=[
            b,close
        ])

        dialog.open()


#chat screen
class Chat(Screen):

    def new_text(self,user):
        #let user send a new text and save to firebase
        self.user = user
        user = self.user.capitalize()

        self.ids.scroll.scroll_y = 0
        self.ids.chatroom.text += f"{user}: {self.ids.chat_text.text}\n"
        Chat_Data().adding_to_db(f"{user}: {self.ids.chat_text.text}\n")
        self.ids.chat_text.text = ""

    #for loadinng past texts from firebase
    def load_text(self):

        try:
            self.ids.chatroom.text=""
            data=Chat_Data().load_db()
            for i in data:
                self.ids.chatroom.text += f"\n{i}"
        except:
            pass

#for searching recipies -NOTE ADD AUTOMATIC SCROLL TO TOP -done
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




#run the app

class blu3whaleApp(MDApp):
    def set_screen(self,screen):
        self.root.current = screen

    def build(self):
        self.file = Builder.load_file("gui/GUI.kv")
        return self.file

    def on_start(self):
        #for automatically logging in the user
        try:
            with open("session.json","r") as file:
                data = json.load(file)

            d = len(data["UserSession"])
            last_sesh = data["UserSession"][d-1]

            self.file.get_screen('Login').ids.username.text = last_sesh["USER"]
            self.file.get_screen('Login').ids.user_password.text = last_sesh["PASSW"]

            self.set_screen('Home')
        except:
            pass


blu3whaleApp().run()
