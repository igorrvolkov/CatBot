import requests
from loader import API_KEY

url = "https://meowfacts.p.rapidapi.com/"

querystring = {"lang": "eng"}

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "meowfacts.p.rapidapi.com"
}


def get_random_cat_fact() -> str:
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['data'][0]



