"""
Created on May 20, 2018
@author: Sherwin Benosa
"""

from bs4 import BeautifulSoup
import json
import requests
import urllib
import locale
import pandas as pd
import re
import random
import sys
import csv

csv_file = open('movies_income.csv','w',newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Release_Date','Movie','Production_Budget','Domestic_Gross','Worldwide_Gross'])

def parse_price(price):
    if not price:
        return 0
    price = price.replace(',', '')
    return locale.atoi(re.sub('[^0-9,]', "", price))

def main():

    movie_budget_url = 'http://www.the-numbers.com/movie/budgets/all'
    response = requests.get(movie_budget_url)
    bs = BeautifulSoup(response.text, 'lxml')
    table = bs.find('table')
    rows = [elem for elem in table.find_all('tr') if elem.get_text() != '\n']
    
    for row in rows[1:]:
        specs = [elem.get_text() for elem in row.find_all('td')]
        movie_name = specs[2].encode('latin1').decode('utf8', 'ignore')

        release_date = specs[1]
        movie_name   = movie_name
        production_budget = parse_price(specs[3])
        domestic_gross = parse_price(specs[4])
        worldwide_gross = parse_price(specs[5])

        csv_writer.writerow([release_date,movie_name, production_budget, domestic_gross, worldwide_gross])       
    csv_file.close()

if __name__ == '__main__':
    main()