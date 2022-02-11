import smtplib
import os
import json
from email.message import*



class UserLogin:
    def __init__(self,username,password="blank",*email):
        self.email = email
        self.username = username
        self.password = password

        self.login_data = {
            'Logins': []
        }
        self.user_data = {
            "USERNAME": self.username,
            "EMAIL": self.email,
            "PASSWORD": self.password,}


        with open("C:\\Users\\rumeza\\PycharmProjects\\pythonProject\\User_Login_Data\\logins.json",'r') as read:
            self.data=json.load(read)

        #filter data
        self.filter_data =self.data['Logins']

    def sign_up(self):
        #try opening json file
        try:
            with open("C:\\Users\\rumeza\\PycharmProjects\\pythonProject\\User_Login_Data\\logins.json","r") as file:
                json_data=json.load(file)

        #if file nonexsistant, write data
        except:
            with open("C:\\Users\\rumeza\\PycharmProjects\\pythonProject\\User_Login_Data\\logins.json","w") as file:
                self.login_data['Logins'].append(self.user_data), file
                json.dump(self.login_data,file,indent=4)

        #if file exsists append new data
        else:
            json_data['Logins'].append(self.user_data)

            with open("C:\\Users\\rumeza\\PycharmProjects\\pythonProject\\User_Login_Data\\logins.json","w") as file:
                json.dump(json_data,file,indent=4)


    def sign_in(self):
        #get the password
        for i, retrieve in enumerate(self.filter_data):
            search = retrieve['USERNAME']
            # once username found, retrieve password
            if search == self.username:
                passw = "".join(retrieve['PASSWORD'])

                # if password matches return true
                if passw == self.password:
                    print("logged in")
                    return True

                else:
                    print("wrong password")
                    return False


    def change_pass(self,*newpass):
        self.newpass = newpass
        update_pass = [retrieve.update({"PASSWORD":self.newpass})
                       for i,retrieve in enumerate(self.filter_data)
                       if retrieve["USERNAME"]==self.username]

        with open("C:\\Users\\rumeza\\PycharmProjects\\pythonProject\\User_Login_Data\\logins.json","w") as file:
            json.dump(self.data,file,indent=4)



        #send email verification

        my_email = "blu3whalebusiness@gmail.com"
        my_pass =os.environ['my_pass']


        msg = EmailMessage()
        msg['Subject'] = 'Password Change Alert'
        msg['From'] = my_email
        msg['To'] = self.email

        #update w/ html and css l8ter
        msg.set_content(f"Hey {self.username},\nyour password was reset")


        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as mail:
            mail.starttls()
            mail.login(user=my_email, password=my_pass)
            mail.send_message(msg)

            return True


    def get_email(self):

        for i,read in enumerate(self.filter_data):
            search = read["USERNAME"]

            #once username found, retrieve password
            if search == self.username:
                self.email = read["EMAIL"]
                email = "".join(self.email)
                return email



UserLogin("fake_test","cats123").sign_in()

