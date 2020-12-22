from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd


rank = []
name = []
year = []
certificate = []
runtime = []
genre = []
rating = []
story = []
director = []
cast1 = []
cast2 = []
cast3 = []
cast4 = []
gross = []
base = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=10000'


for i in range(1, 6452, 50):
    response = requests.get(
        f'{base},&countries=us&sort=user_rating,desc&start={i}&ref_=adv_nxt')
    print(f'Scraping progress : {i} / 6452...')
    if response.status_code == 200:
        print('Response : OK')
    soup = BeautifulSoup(response.content, 'html.parser')
    full = soup.find_all(class_='mode-advanced')
    for d in full:
        rank.append(d.h3.span.get_text())
        name.append(d.h3.a.get_text())
        try:
            year.append(d.h3.select('span')[1].get_text())
        except IndexError:
            year.append('NaN')
        try:
            certificate.append(d.p.span.get_text())
        except IndexError:
            certificate.append('NaN')
        try:
            runtime.append(d.p.find(class_='runtime').get_text())
        except IndexError:
            runtime.append('NaN')
        try:
            genre.append(d.p.find(class_='genre').get_text())
        except IndexError:
            genre.append('NaN')
        rating.append(d.find(class_='ratings-bar').find('div')['data-value'])
        try:
            story.append(d.select('.text-muted')[2].get_text())
        except IndexError:
            story.append('NaN')
        director.append(d.select('p')[2].select('a')[0].get_text())
        try:
            cast1.append(d.select('p')[2].select('a')[1].get_text())
        except IndexError:
            cast1.append('NaN')
        try:
            cast2.append(d.select('p')[2].select('a')[2].get_text())
        except IndexError:
            cast2.append('NaN')
        try:
            cast3.append(d.select('p')[2].select('a')[3].get_text())
        except IndexError:
            cast3.append('NaN')
        try:
            cast4.append(d.select('p')[2].select('a')[4].get_text())
        except IndexError:
            cast4.append('NaN')
        try:
            gross.append(d.select('div')[3].select('p')[
                         3].select('span')[4].get_text())
        except IndexError:
            gross.append('NaN')
    #print('waiting 2 seconds...')
    #sleep(2)

df = pd.DataFrame({
    'rank': rank,
    'name': name,
    'year': year,
    'certificate': certificate,
    'runtime': runtime,
    'genre': genre,
    'rating': rating,
    'story': story,
    'director': director,
    'cast1': cast1,
    'cast2': cast2,
    'cast3': cast3,
    'cast4': cast4,
    'gross': gross})

df.to_csv('imdb_top_movies_12-19-20.csv', index=False)
print(df.info())
