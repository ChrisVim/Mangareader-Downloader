from bs4 import BeautifulSoup
import os
import requests
import sys

if not os.path.isfile('manga_list'):
    k = requests.get('https://www.mangareader.net/alphabetical')
    r = open('manga_list', 'w+')
    r.write(k.text)
    k.close()
    r.close()

r = open('manga_list', 'r')
soup = BeautifulSoup(r.read(), 'html.parser')
r.close()

items = soup.findAll('a')
item_dic = {}

for i in items:
    try:
        lis = [i['href'], i.text]
        item_dic[i.text] = i['href']
    except:
        pass

def search_word(keyword):
    search_list = [key for key, value in item_dic.items() if keyword.lower()
            in key.lower()]
    for i, element in enumerate(search_list, 1):
        print('. '.join((str(i).zfill(2), element)))
    print(50*'-')
    choser = int(input('select manga - '))-1
    print(50*'-')
    return item_dic[search_list[choser]]
