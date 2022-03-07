import json

#for letting the user make goals
class Goals:
    #initiate json dict
    def __init__(self,user,goals=""):
        self.user = user
        self.goals = goals
        self.goals_li = {"Goals":[]}
        self.goals_dict = {
            "USER":self.user,
            "GOALS": [self.goals]
        }

    #for updating the current goal list
    def update_goals(self):
        with open("user_goals_blu3/User_Goals/user_goals.json", "r") as file:
            self.data = json.load(file)
        data = self.data["Goals"]

        for i, retrieve in enumerate(data):
            search = retrieve['USER']
                # once username found, retrieve notes
            if search == self.user:

                retrieve["GOALS"].append(self.goals)

                with open("user_goals_blu3/User_Goals/user_goals.json", "w") as file:
                    json.dump(self.data, file, indent=4)

    #for loading the previous goals
    def load_goals(self):
        with open("user_goals_blu3/User_Goals/user_goals.json","r") as file:
            self.data = json.load(file)
        self.data = self.data["Goals"]
        for i, retrieve in enumerate(self.data):
            search = retrieve['USER']
            # once username found, retrieve notes
            if search == self.user:
                return retrieve["GOALS"]

    #for adding new users to the json
    def add_goals(self):
        with open("user_goals_blu3/User_Goals/user_goals.json", "r") as file:
            self.data = json.load(file)
        self.data['Goals'].append(self.goals_dict)

        with open("user_goals_blu3/User_Goals/user_goals.json", "w") as file:
            json.dump(self.data, file, indent=4)

    #for deleting goals
    def remove_goals(self,goal):
        with open("user_goals_blu3/User_Goals/user_goals.json", "r") as file:
            data = json.load(file)
        self.data = data["Goals"]

        for i, retrieve in enumerate(self.data):
            search = retrieve['USER']
            # once username found, retrieve goals
            if search == self.user:
                retrieve["GOALS"].remove(goal)
                retrieve.update({"GOALS":retrieve["GOALS"]})

        with open("user_goals_blu3/User_Goals/user_goals.json", "w") as file:
            json.dump(data, file, indent=4)



