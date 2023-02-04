# ingredient_scraper.py
import requests
import bs4
from urllib.parse import urlencode
BASE_URL = 'https://www.allrecipes.com/search?'

def url_to_soup(url: str) -> bs4.BeautifulSoup:
    result = requests.get(url)
    return bs4.BeautifulSoup(result.text, 'lxml')

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

def url_to_recipies(url: str) -> list[tuple[str,str]]:
    """
    Given a url, it will return a list of recipies with these properties...
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
    


if __name__ == "__main__":
    ingredients = {
    'Carrots':['1/30/2023',20,'Counter'],
    'Chicken':['1/31/2023',50,'Fridge']
    }   
    url = ingredients_to_url(ingredients)
    for recipe in url_to_recipies(url):
        print(recipe)