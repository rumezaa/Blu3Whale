import firebase_admin
import json
import requests
from firebase import firebase

#startig a chat firebase
class Chat_Data:
	def __init__(self):
		#get firebase ulr
		self.url = "https://blu3whalechat-default-rtdb.firebaseio.com/"
		self.app = firebase.FirebaseApplication(self.url)


	#post new texts to the data base
	def adding_to_db(self,text):
		result = self.app.post(self.url, {'CHAT': text})

	#load the previous texts from the firebase
	def load_db(self):
		result = self.app.get(self.url,None)
		values = result.values()

		chats = [list(i.values())[0] for i in values]

		return chats




