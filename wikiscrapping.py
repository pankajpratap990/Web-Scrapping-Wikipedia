"""
    In this script, we are scraping the information various proxy wars between U.S and Soviet Union
    happened during the period of cold war using wikipedia as source.
    Final result is saved csv file
"""

import requests
from bs4 import BeautifulSoup
import wikipedia
import pandas as pd
import time

"""
    First we pull the Html from the https://en.wikipedia.org/wiki/List_of_proxy_wars using requests module
"""
r = requests.get('https://en.wikipedia.org/wiki/List_of_proxy_wars')

"""
    Turning html acquired using request to Html object
"""
source = BeautifulSoup(r.text,'lxml')

"""
    Extracting cold war table from html
"""
body = source.find('span', id='Cold_War_proxy_wars').parent.find_next_sibling('table')
table = body.tbody

"""
  links list to store wikipedia link of respective war
  titles list to store title of respective war
  years list to store period of the respective war
  summary list to store summary of respective war
"""

links = []
titles = []
years = []
summary = []

"""
    Inserting information from the table to the links,titles,years lists
"""
for row in table.find_all('tr'):
    if row.find('td') == None:
        continue
    else:
        link = row.find('a', href=True)
        links.append('https://en.wikipedia.org'+link['href'])
        title = row.find('a', title=True)
        titles.append(title['title'])
        data = row.td.find_next_sibling('td')
        data = str(data.next_element)
        if data[-1] == '\n':
            data = data[:-1]
        years.append(data)


"""
    Correcting discrepancy in the scraped data of year.
    Discrepancy is caused due to dissimilar cell on row 26
"""
years[25] = "1961–1974 and 1974–1991"

"""
    Inserting summary to summary list using wikipedia api
"""

i = 0
for title in titles:
    text = wikipedia.WikipediaPage(title=title).summary
    print(i)
    summary.append(text)
    time.sleep(1)
    i += 1

"""
    Using Dataframe to store acquired lists into csv file
"""
df = pd.DataFrame(titles, columns=['Wars'])
df['Year'] = years
df['Summary'] = summary
df['Resource Link'] = links
cold_war_csv = df.to_csv(r'cold-war.csv',index=False)
print(df)