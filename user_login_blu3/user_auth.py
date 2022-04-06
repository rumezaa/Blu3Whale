import json



#app login system
class UserLogin:
    def __init__(self,username,password="blank",*email):
        self.email = email
        self.username = username
        self.password = password


        with open("user_login_blu3/User_Login_Data/logins.json", mode="r") as read:
            self.data=json.load(read)

        #filter data
        self.filter_data =self.data['Logins']

    #for signing up users
    def sign_up(self):
        li = []
        for i, retrieve in enumerate(self.filter_data):
            search = retrieve['USERNAME']
            li.append(search)

        self.login_data = {
            'Logins': []
        }

        if self.username not in li:
            self.user_data = {
                "USERNAME": self.username,
                "EMAIL": self.email,
                "PASSWORD": self.password,
                "GRAPH": False}
            #try opening json file
            try:
                with open("user_login_blu3/User_Login_Data/logins.json","r") as file:
                    json_data=json.load(file)

        #if file nonexsistant, write data
            except:
                with open("user_login_blu3/User_Login_Data/logins.json","w") as file:
                    self.login_data['Logins'].append(self.user_data), file
                    json.dump(self.login_data,file,indent=4)

        #if file exsists append new data
            else:

                json_data['Logins'].append(self.user_data)

                with open("user_login_blu3/User_Login_Data/logins.json","w") as file:
                    json.dump(json_data,file,indent=4)
                return True
        else:
            return False

    #for signing in
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

    #for changing the password
    def change_pass(self,*newpass):
        self.newpass = newpass
        update_pass = [retrieve.update({"PASSWORD":self.newpass})
                       for i,retrieve in enumerate(self.filter_data)
                       if retrieve["USERNAME"]==self.username]

        with open("user_login_blu3/User_Login_Data/logins.json","w") as file:
            json.dump(self.data,file,indent=4)


        return True

    #getting the email
    def get_email(self):

        for i,read in enumerate(self.filter_data):
            search = read["USERNAME"]

            #once username found, retrieve password
            if search == self.username:
                self.email = read["EMAIL"]
                email = "".join(self.email)
                return email

    #for seeing whether has a graph established
    def get_newusers(self):
        bool_graph = [retrieve["GRAPH"] for i,retrieve in enumerate(self.filter_data)
                       if retrieve["USERNAME"]==self.username]
        return bool_graph

    #updating whether the user has a graph established
    def change_newusers(self):
        update_pass = [retrieve.update({"GRAPH": True})
                       for i, retrieve in enumerate(self.filter_data)
                       if retrieve["USERNAME"] == self.username]

        with open("user_login_blu3/User_Login_Data/logins.json", "w") as file:
            json.dump(self.data, file, indent=4)






