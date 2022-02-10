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
        for i in range(len(self.data)):
            self.meal_ingredients = []
            self.meal_name = (self.data[i]["strMeal"])
            self.meal_instruc = (self.data[i]["strInstructions"])
            self.meal_image = (self.data[i]["strMealThumb"])
            self.meal_video = (self.data[i]["strYoutube"])
            for x in range(20):
                if x != 0:
                    self.meal_ingredient = (self.data[i][f"strIngredient{x}"])
                    self.ingredient_measure = (self.data[i][f"strMeasure{x}"])

                    if self.meal_ingredient and self.ingredient_measure != '':
                        # create a string which has the ingredient and its measurment
                        self.measure_ingredients = f"{self.meal_ingredient} - {self.ingredient_measure}"

                        # add item to list
                        self.meal_ingredients.append(self.measure_ingredients)
                        # convert measures and ingrdients to string
                        self.ingredients = "; ".join(self.meal_ingredients)

            self.visualize = f"""<!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="UTF-8">
                                        <title>Meals</title>
                                        </head>
                                        <body>
                                            <h3>{self.meal_name}</h3>
                                            <center><img src = {self.meal_image}></img></center>
                                            <p>{self.ingredients}</p>
                                            <p>{self.meal_instruc}</p>
                                            <br>
                                            <br>
                                            <a href={self.meal_video} target='_blank'>YouTube Recipe</a>

                                        </body>
                                            </html>
                                            """

            # visualize on html file
            try:
                with open("file.html", "a", encoding="utf-8") as file:
                    file.write(self.visualize)
            except:
                with open("file.html", "w", encoding="utf-8") as file:
                    file.write(self.visualize)










