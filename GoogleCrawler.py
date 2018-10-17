import re
import pandas as pd
import json
import requests_cache
import requests
from bs4 import BeautifulSoup

requests_cache.install_cache('google')

BASE_URL = 'https://www.google.com/search?tbm=shop&q='

COLORS = ['red', 'yellow', 'green', 'orange', 'white', 'blue', 'brown', 'black', 'grey']
CLOTHES = ['Blouse',
           'Cardigan',
           'Dress',
           'Jacket',
           'Joggers',
           'Kimono',
           'Leggings',
           'Shorts',
           'Skirt',
           'Sweater',
           'Tank',
           'Tee',
           'Top']

'''
@param string searchTerm
@param string site
@param boolean useLiteral
'''


def createSearchQuery(search_term):
    literal_str = "%22"
    parsed_search_term = search_term.split()
    concatenated = ""
    for term in parsed_search_term:
        concatenated += term + "+"

    query = literal_str + concatenated + literal_str
    return query


'''
@param string searchTerm
'''


def getGoogleResponses(search_term):
    query = createSearchQuery(search_term)
    result = requests.get(BASE_URL + query)
    return result


'''
@param request result
@returns list l
'''


def parseResult(result):
    soup = BeautifulSoup(result.text)
    clothes_divs = soup.findAll("div", {"class": "g"})
    df = pd.DataFrame()

    # add all the <p> into a list
    for tile_index in range(len(clothes_divs)):
        image_html_div = soup.findAll('div', attrs={'class': 'psliimg'})[tile_index]
        alt_tag = str(image_html_div).split('<')[3].split('src')
        image_link = alt_tag[1][1:-2]
        source = soup.findAll('div', attrs={'class': '_AT'})[tile_index]
        source_div = str(source).split('href')[1].split('"')
        source_link = source_div[1].replace('"', '')
        image_title = clean_html(source_div[2])[1:]
        row = {'image_title': image_title, 'image_link': image_link, 'source_link': source_link}
        df = df.append(row, ignore_index=True)

    return df


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', raw_html)
    return clean_text


def generate_clothes_colors_combination():
    df = pd.DataFrame()
    for color in COLORS:
        for clothe in CLOTHES:
            string = color + ' ' + clothe
            print(string)
            df = df.append(run(string), ignore_index=True)

    return df

def df_to_sql(df):
    return


def run(search_term):
    search_results = getGoogleResponses(search_term)
    clothes = parseResult(search_results)
    return clothes


print("I love you so much babe, thank you for working on this project with me")
print("I know that no matter what, we'll have a lovey result")

out_df = (generate_clothes_colors_combination())
out_df.to_csv('out-2.csv')
print(out_df)

#print(run('red Blouse'))
