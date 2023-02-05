# ingredient_scraper.py
import requests
import bs4
from urllib.parse import urlencode
import json
BASE_URL = 'https://www.allrecipes.com/search?'
RECIPES_PER_PAGE = 24

def url_to_soup(url: str) -> bs4.BeautifulSoup:
    result = requests.get(url)
    return bs4.BeautifulSoup(result.text, 'lxml')

def is_url_empty(url: str) -> bool:
    """
    Returns whether or not the page has no recipes or not
    """
    ret = []
    soup = url_to_soup(url)
    recipes = soup.select('.comp.mntl-card-list-items.mntl-document-card.mntl-card.card.card--no-image')
    return len(recipes) == 0


def ingredients_to_url(ingredients: dict, offset = 0) -> str:
    """
    Given a dictionary of ingredients, returns a url
    string to so that we can strape this bad baby 

    The offset is just so we can change pagination
    """

    """
    Just to note the format of the ingredients:
    ingredients: key = ingredient name
                 value = [date_bought: str, days_until_expiration: int, location: str]
    """
    ingredients_str = ""
    for ingredient_name, data in ingredients.items():
        ingredients_str += ingredient_name + ' '
    url_str = BASE_URL + urlencode({'q': ingredients_str, 'offset': offset})
    return url_str

def url_to_recipes(url: str) -> list[tuple[str,str]]:
    """
    Given a url, it will return a list of recipes with these properties...
    1) The first index of the tuple will be the name of the recipie
    2) The second index of the tuple will be another url to that specific recipe
    """
    ret = []
    soup = url_to_soup(url)
    recipes = soup.select('.comp.mntl-card-list-items.mntl-document-card.mntl-card.card.card--no-image')
    for recipe in recipes:
        recipe_url = recipe['href']
        recipe_text = recipe.select('.card__title-text ')[0].get_text()
        ret.append((recipe_text,recipe_url))
    
    return ret


def get_recipes(ingredients: dict, n: int) -> list[tuple[str,str]]:
    """
    Gets n recipes in the same format as url_to_recipes
    """
    ret = []
    offset = 0
    while True:
        url = ingredients_to_url(ingredients)
        if is_url_empty(url):
            # Just stop if there are no ingredients left...
            break
        ret.extend(url_to_recipes(ingredients_to_url(ingredients, offset)))
        offset += RECIPES_PER_PAGE

        # Filter out the dodo ones
        def is_recipe(x):
            url = x[1]
            return '/recipe/' in url

        ret = list(filter(is_recipe , ret))

        if len(ret) >= n:
            # We reached our amount
            break

    return ret[:n]
        

def url_to_recipe(url: str) -> dict:
    """
    Given the url to a valid recipe, makes a recipe object thingy
    """
    # recipe object [title, prep time, cook time, additional time, total time, portions, ingredients, directions, notes, nutrition faces]

    soup = url_to_soup(url)
    title = soup.select('#article-heading_2-0')[0].get_text()

    # Getting the title
    title = title[1::] # GET RID OF THAT STUPID NEWLINE CHARACTER AT THE BEGINNING LIKE WHY DO YOU EXIST GET OUT OF MY FACE
    
    # Getting prep time, cook time, additional time, total time, and portions
    cooking_info = soup.select('.mntl-recipe-details__content')[0]
    cooking_info = list(zip( cooking_info.select('.mntl-recipe-details__label'), cooking_info.select('.mntl-recipe-details__value')))
    
    prep_time, cook_time, additional_time, total_time, servings = (None, None, None, None, None)
    for label, value in cooking_info:
        label_text = label.get_text().lower()
        value_text = value.get_text()
        if label_text == "prep time:":
            prep_time = value_text
        elif label_text == "cook time:":
            cook_time = value_text
        elif label_text == "total time:":
            total_time = value_text
        elif label_text == "servings:" or label == 'yield:':
            servings = value_text
        elif label_text == "additional time:":
            additional_time = value_text
    
    # GRAB THOSE INGREDIENTS
    ingredient_list = soup.select('.mntl-structured-ingredients__list')[0]
    ingredient_list = ingredient_list.select('.mntl-structured-ingredients__list-item ')
    ingredients = ""
    for ingredient in ingredient_list:
        ingredients += ingredient.get_text().strip() + '\n'
    
    # GET DA DIRECTIONS
    directions_str = ""
    directions = soup.select('.comp.recipe__steps.mntl-block')[0]
    directions = directions.select('.comp.mntl-sc-block.mntl-sc-block-html')
    for step_number, direction in enumerate(directions):
        directions_str += f'Step {step_number + 1}\n'
        directions_str += direction.get_text().strip() + '\n'
        
    # NUT(rition)
    nutrition_facts = soup.select('.mntl-nutrition-facts-summary__table-row')
    nutrition_str = ""
    for fact in nutrition_facts:
        nutrition_str += fact.get_text()

        


    ret = dict()

    ret["title"] = title
    ret["prep_time"] = prep_time
    ret["cook_time"] = cook_time
    ret["additional_time"] = additional_time
    ret["total_time"] = total_time
    ret["portions"] = servings
    ret["ingredients"] = ingredients
    ret["directions"] = directions_str
    ret["nutrition_facts"] = nutrition_str
    ret["notes"] = None

    return ret

def ingredients_to_recipe_dict(ingredients: dict, n: int) -> dict:
    """
    Given the ingredients and the amount of recipes we want, returns a dict of all the recipes
    """
    return [url_to_recipe(recipe[1]) for recipe in get_recipes(ingredients,n)]

def ingredients_to_recipe_json(ingredients: dict, n: int) -> dict:
    """
    Given the ingredients and the amount of recipes we want, returns a json of all the recipes
    """
    return json.dumps(ingredients_to_recipe_dict(ingredients,n))

if __name__ == "__main__":
    ingredients = {
    'Flour':['1/30/2023',20,'Counter'],
    'Baking Soda':['1/31/2023',50,'Fridge'],
    }   
    print(ingredients_to_recipe_dict(ingredients, 10))
