
def imdb_scrape(x, y,  m, complete=False):
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

    for a in range(x, y):

        if complete:
            res_a = requests.get(
                f'https://www.imdb.com/search/title/?title_type=feature&year={a}-01-01,{a}-12-31&start=1&ref_=adv_nxt'
            )
            soup_a = BeautifulSoup(res_a.content, 'html.parser')
            text = soup_a.find(class_='desc').span.get_text()
            m = int(text[8:13].replace(',', ''))
        else:
            m = m

        for i in range(1, m, 50):

            response = requests.get(
                f'https://www.imdb.com/search/title/?title_type=feature&year={a}-01-01,{a}-12-31&start={i}&ref_=adv_nxt'
            )
            print(f'Scraping for year {a}')
            print(f'Scraping progress : {i} / {m}')

            if response.status_code == 200:
                print('Response : OK')
            else:
                print('Response: NOT OK')

            soup = BeautifulSoup(response.content, 'html.parser')
            full = soup.find_all(class_='mode-advanced')
            for d in full:
                rank.append(d.h3.span.get_text())
                name.append(d.h3.a.get_text())
                try:
                    year.append(d.h3.select('span')[1].get_text())
                except:
                    year.append('NaN')
                try:
                    certificate.append(d.p.span.get_text())
                except:
                    certificate.append('NaN')
                try:
                    runtime.append(d.p.find(class_='runtime').get_text())
                except:
                    runtime.append('NaN')
                try:
                    genre.append(d.p.find(class_='genre').get_text())
                except:
                    genre.append('NaN')
                try:
                    rating.append(d.find(class_='ratings-bar').find('div')['data-value'])
                except:
                    rating.append('NaN')
                try:
                    story.append(d.select('.text-muted')[2].get_text())
                except:
                    story.append('NaN')
                try:
                    director.append(d.select('p')[2].select('a')[0].get_text())
                except:
                    director.append('NaN')
                try:
                    cast1.append(d.select('p')[2].select('a')[1].get_text())
                except:
                    cast1.append('NaN')
                try:
                    cast2.append(d.select('p')[2].select('a')[2].get_text())
                except:
                    cast2.append('NaN')
                try:
                    cast3.append(d.select('p')[2].select('a')[3].get_text())
                except:
                    cast3.append('NaN')
                try:
                    cast4.append(d.select('p')[2].select('a')[4].get_text())
                except:
                    cast4.append('NaN')
                try:
                    gross.append(d.select('div')[3].select('p')[3].select('span')[4].get_text())
                except:
                    gross.append('NaN')
            print('waiting 2 seconds...')
            sleep(2)

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

    df.to_csv(f'imdb_top_movies_{x}-{y}_top{m}.csv', index=False)
    print(f" 'imdb_top_movies_{x}-{y}_top{m}.csv' file saved")
    return df.info()


#imdb_scrape(1920, 1930, full=True)
#imdb_scrape(1930, 1940)
#imdb_scrape(1940, 1950)
#imdb_scrape(1950, 1960, 10)
imdb_scrape(1950, 1970, 10)
imdb_scrape(1970, 1980,20)
imdb_scrape(1980, 1990,50)
imdb_scrape(1990, 2000,500)
imdb_scrape(2000, 2010,500)
imdb_scrape(2010, 2021,500)
