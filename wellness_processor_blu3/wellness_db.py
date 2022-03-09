import matplotlib.pyplot as plt
import nltk
from matplotlib import pyplot as pi
import sqlite3 as sql
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime



class WellnessTrack:
    def __init__(self,username):
        self.username = username
        self.seven_day = 0


    def create_DB(self,*categories):
        con = sql.connect(f"wellness_processor_blu3\\User_Wellness_Data\\{self.username}_data.db")
        self.categories = list(categories)
        self.categ = ["date","mood"]

        self.categ.extend(self.categories)
        self.categ = tuple(self.categ)
        cur = con.cursor()
        # Create table
        cur.execute(f'''CREATE TABLE wellness_data
                       {self.categ}''')

        # Save changes
        con.commit()
       # secure connection
        con.close()

    def update_DB(self,sentiment,*input):
        self.input = input
        self.input = list(self.input)


        for i,v in enumerate(self.input):
            if v=="yes":
                self.input[i]=1
            elif v=="no":
                self.input[i] = 0
            else:
                self.input[i] = int(v)

        self.date = datetime.now().date()
        self.seven_day +=1
        self.sentiment = sentiment


        #sentiment analysis
        self.classify = SentimentIntensityAnalyzer()
        self.eval = self.classify.polarity_scores(self.sentiment)
        self.mood = self.eval["compound"]

        con = sql.connect(f"wellness_processor_blu3\\User_Wellness_Data\\{self.username}_data.db")
        cur = con.cursor()
        # Create table
        data = [self.date,self.mood]
        data.extend(self.input)

        # Create table
        cur.execute(f"INSERT INTO wellness_data VALUES (?,?,?,?,?)", data)

        # save changes
        con.commit()

        # close db
        con.close()
    def retrieve_DB(self):
        con = sql.connect(f"wellness_processor_blu3\\User_Wellness_Data\\{self.username}_data.db")
        cur = con.cursor()

        # select the table
        query = '''SELECT * FROM wellness_data'''
        cur.execute(query)
        db_data=cur.fetchall()

        # extract db data values
        dates = [dates[0] for dates in db_data ]

        mood_status = [float(mood[1]) for mood in db_data if float(mood[1])!=0]


        cat_1 = [cat_1[2] for cat_1 in db_data]
        cat_2 = [cat_2[3] for cat_2 in db_data]
        cat_3 = [cat_3[4] for cat_3 in db_data]
        try:
            avg_mood = sum(mood_status) / len(mood_status)
        except:
            avg_mood = 0
        avg_mood = round(avg_mood,4)*100

        mood_total = 100 - abs(avg_mood)

        return dates, mood_total, sum(cat_1), sum(cat_2),sum(cat_3)

    def create_visual(self):
        # fetching the headers
        con = sql.connect(f"wellness_processor_blu3\\User_Wellness_Data\\{self.username}_data.db")
        cursor = con.cursor()

        cursor.execute('''Select * from wellness_data''')



        #retrives the db categories
        headers = [i[0] for i in cursor.description if i != 'date']

        #use this data for 7 day achievements ?? -- ended up nto doing 7 day achievmets - maybe in a future update
        headers.remove('date')

        #try fetching data if user has data
        try:
            categories = list(self.retrieve_DB())

            #puts user data in an array
            data_set = [categories[i] for i in range(len(categories)) if i>0]
            achievement = max(data_set)
            work = min(data_set)

            #returns ur area of growth
            achieve = [headers[i] for i,v in enumerate(data_set) if v==achievement]
            work_on = [headers[i] for i,v in enumerate(data_set) if v==work]


            return data_set, headers,achieve[0],work_on[0]

        #if not, get the headers
        except:
            return headers





