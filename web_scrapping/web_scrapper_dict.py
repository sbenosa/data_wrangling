from bs4 import BeautifulSoup
import json
import requests
import urllib
from tqdm import tqdm
import locale
import pandas as pd
import re
import time
import random
import sys

def parse_price(price):
    if not price:
        return 0
    price = price.replace(',', '')
    return locale.atoi(re.sub('[^0-9,]', "", price))

def get_movie_budget():

    movie_budget_url = 'http://www.the-numbers.com/movie/budgets/all'
    response = requests.get(movie_budget_url)
    bs = BeautifulSoup(response.text, 'lxml')
    table = bs.find('table')
    rows = [elem for elem in table.find_all('tr') if elem.get_text() != '\n']
    
    movie_budget = []
    for row in rows[1:]:
        specs = [elem.get_text() for elem in row.find_all('td')]
        movie_name = specs[2].encode('latin1').decode('utf8', 'ignore')
        movie_budget.append({'release_date': specs[1],
                             'movie_name': movie_name,
                             'production_budget': parse_price(specs[3]),
                             'domestic_gross': parse_price(specs[4]),
                             'worldwide_gross': parse_price(specs[5])})
    return movie_budget

if __name__ == '__main__':        
   movie_budget = get_movie_budget()
   #print(movie_budget)


