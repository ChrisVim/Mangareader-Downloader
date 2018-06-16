from bs4 import BeautifulSoup
import Grab_Index_List
import os
import requests

def fetch_chapter_names(mname):
    home = 'https://www.mangareader.net'
    r = requests.get(''.join((home, mname)))
    soup = BeautifulSoup(r.text, 'html.parser')
    ctable = soup.find('div',{'id':'chapterlist'}).table
    nctable = (ctable.findAll('td'))
    chapter_list = [table.text.strip() for table in nctable]
    del chapter_list[1::2]
    return chapter_list

def fetch_page_links(mname, vol):
    # returns the links of the pages
    home = 'https://www.mangareader.net'
    r = requests.get(''.join((home,mname,'/',str(vol))))
    soup = BeautifulSoup(r.text, 'html.parser')
    chapters = [''.join((home, chapter['value'])) for chapter in soup.div.findAll('option')]
    return chapters

def fetch_img_links(page_links):
    img_links = []
    clen = len(page_links)
    for i,link in enumerate(page_links, 1):
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        img_links.append(soup.find('div', id='imgholder').a.img['src'])
        print(' / '.join(('fetching',str(i).zfill(2),str(clen).zfill(2))), end='\r'),
    return img_links

def down_imgs(img_links, manga_name, chapter_name):
    print('')
    dlen = len(img_links)
    path = '/'.join((manga_name,chapter_name))
    create_folder(path)
    for i, link in enumerate(img_links, 1):
        r = requests.get(link)
        with open(''.join((path,'/',str(i).zfill(2),'.jpg')), 'wb') as f:
            f.write(r.content)
        print(' / '.join(('downloading',str(i).zfill(2), str(dlen))), end='\r')
    print(50*'-')
    print('finished')

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    manga = input('which manga - ')
    print(50*'-')
    chosen = Grab_Index_List.search_word(manga)
    svol = int(input('which start chapter - '))
    evol = int(input('which end chapter - '))
    clen = [i for i in range(svol,evol+1)]
    chapter_names = fetch_chapter_names(chosen)

    for i in clen:
        print(50*'-')
        print(chapter_names[i-1])
        print(50*'-')
        links= fetch_page_links(chosen, i)
        img_links = fetch_img_links(links)
        down_imgs(img_links, manga ,chapter_names[i-1])
    print(50*'-')
