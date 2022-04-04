
import json
import requests


#startig a chat firebase
class Chat_Data:
	def __init__(self):
		#get firebase ulr
		self.url = "https://blu3whalechat-default-rtdb.firebaseio.com/.json"


	#post new texts to the data base
	def adding_to_db(self,text):
		result = requests.post(url = self.url, json = {'CHAT': text})

	#load the previous texts from the firebase
	def load_db(self):
		result = requests.get(self.url)
		values = result.json().values()

		chats = [list(i.values())[0] for i in values]

		return chats




