import nltk
import csv
import pandas
from matplotlib import pyplot as pi
import sqlite3 as sql
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import numpy as np

class WellnessTrack:
    def __init__(self,username):
        self.username = username



    def create_DB(self):
        con = sql.connect(f"C:\\Users\\rumeza\\PycharmProjects\\pythonProject\\User_Wellness_Data\\{self.username}_data.db")
        cur = con.cursor()
        # Create table
        cur.execute('''CREATE TABLE wellness_data
                       (date text, water_drank text, active bool, mood text)''')

        # Save changes
        con.commit()
       # secure connection
        con.close()
    def update_DB(self,water_intake,active,sentiment):
        self.h2o = water_intake
        self.activity = active
        self.date = datetime.now().date()
        self.sentiment = sentiment

        #sentiment analysis
        self.classify = SentimentIntensityAnalyzer()
        self.eval = self.classify.polarity_scores(self.sentiment)
        self.mood = self.eval["compound"]

        con = sql.connect(f"C:\\Users\\rumeza\\PycharmProjects\\pythonProject\\User_Wellness_Data\\{self.username}_data.db")
        cur = con.cursor()
        # Create table
        data = (self.date, self.h2o, self.activity, self.mood)
        # Create table
        cur.execute("INSERT INTO wellness_data VALUES(?,?,?,?)", data)

        # save changes
        con.commit()

        # close db
        con.close()
    def retrieve_DB(self):
        con = sql.connect(f"C:\\Users\\rumeza\\PycharmProjects\\pythonProject\\User_Wellness_Data\\{self.username}_data.db")
        cur = con.cursor()

        # select the table
        query = '''SELECT * FROM wellness_data'''
        cur.execute(query)
        db_data=cur.fetchall()

        # extract db data values
        dates =[dates[0] for dates in db_data ]
        water_intake =  [water[1] for water in db_data]
        activity = [active[2] for active in db_data]
        mood_status = [float(mood[3]) for mood in db_data if float(mood[3])>=0]
        avg_mood = sum(mood_status) / len(mood_status)

        return dates, water_intake, activity, round(avg_mood,4)




print(WellnessTrack("testuser").retrieve_DB())


