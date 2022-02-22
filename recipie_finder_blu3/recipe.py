import kivymd
import kivy
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage

from kivymd.uix.imagelist import SmartTileWithStar
import requests


class RecipeFinder:
    def __init__(self,input):
        self.input = input
        # initialize api
        self.meals_data = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={self.input}")
        self.data = self.meals_data.json()

        self.data = self.data["meals"]



    def get_info(self):
        # clear "browsing" b4 showing new browing
        file_clear = open("file.html", "w")
        file_clear.close()

        # recieve the ingredients, meal name, recipe instruction, mal ima
        self.all_ingreds = []
        self.all_names = [self.data[i]["strMeal"] for i in range(len(self.data))]
        self.all_instrucs= [self.data[i]["strInstructions"] for i in range(len(self.data))]
        self.all_images=[self.data[i]["strMealThumb"] for i in range(len(self.data))]
        self.all_videos=[self.data[i]["strYoutube"] for i in range(len(self.data))]






        for i in range(len(self.data)):
            meal_ingredients = []

            for x in range(20):
                if x != 0:
                    meal_ingredient = (self.data[i][f"strIngredient{x}"])
                    ingredient_measure = (self.data[i][f"strMeasure{x}"])


                    if meal_ingredient and ingredient_measure != '':
                    # create a string which has the ingredient and its measurment
                        measure_ingredients = f"{meal_ingredient} - {ingredient_measure}"

                    # add item to list
                        meal_ingredients.append(measure_ingredients)


        # turn the list into a string
            ingredients = "\n".join(meal_ingredients)
            self.all_ingreds.append(ingredients)

        return {
            "MEAL_NAMES":self.all_names,
            "MEAL_INSTRUCS":self.all_instrucs,
            "MEAL_INGREDS":self.all_ingreds,
            "IMAGES":self.all_images,
            "VIDEOS":self.all_videos
        }
            # title = MDLabel(
            #     text=f"{self.meal_name}",
            #     font_style = "H2",
            #     halign = "center"
            # )
            #
            # self.add_widget(title)











