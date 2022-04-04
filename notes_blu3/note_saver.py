import json

#for lettign user create notes
class Notes:
    def __init__(self,user,notes=""):
        #inital json dict
        self.user = user
        self.note_list = {"Notes":[]}
        self.notes_dict = {
            "USER": self.user,
            "NOTES": notes
        }

    #for updating the user's current notes
    def update_notes(self,new_note=""):
        with open("notes_blu3/user_notes.json", "r") as file:
            self.data = json.load(file)
        data = self.data["Notes"]

        for i, retrieve in enumerate(data):
            search = retrieve['USER']
                # once username found, retrieve notes
            if search == self.user:

                retrieve.update({"NOTES": new_note})

                with open("notes_blu3/user_notes.json", "w") as file:
                    json.dump(self.data, file, indent=4)

        raise IndexError


    #for user's that are not in the json file
    def add_notes(self):
        with open("notes_blu3/user_notes.json", "r") as file:
            self.data = json.load(file)
        self.data['Notes'].append(self.notes_dict)

        with open("notes_blu3/user_notes.json", "w") as file:
            json.dump(self.data, file, indent=4)





    #for loading the previous notes to the screen
    def load_notes(self):
        with open("notes_blu3/user_notes.json","r") as file:
            self.data = json.load(file)
        self.data = self.data["Notes"]
        for i, retrieve in enumerate(self.data):
            search = retrieve['USER']
            # once username found, retrieve notes
            if search == self.user:
                return retrieve["NOTES"]


