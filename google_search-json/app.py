#-- Google search results
from bs4 import BeautifulSoup
import requests
import json

words = input('Enter search keywords: ')
words = words.replace(' ','+')

url = 'https://www.google.com/search?q=' + words
html_doc = requests.get(url)
obj = BeautifulSoup(html_doc.text,'html.parser')
h3s = obj.find_all('h3')
with open('search_results.json','w',encoding='UTF-8') as file:
    data = {}
    for h3 in h3s:
        if(h3.parent.name == 'a'):
            website = h3.parent['href'].split('?q=')[1]
            description = h3.string
            data[website] = description
    json.dump(data,file,indent=2,ensure_ascii=False)