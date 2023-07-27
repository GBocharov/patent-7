import requests
from summary import sum_all_shit
from bs4 import BeautifulSoup

url = "https://patents.google.com/patent/US20170188557A1/en?oq=US20170188557A1"
def get_chapters(url):
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.find('section', itemprop = 'description')
        text = text.find('div', itemprop = 'content')
        text = text.find('ul')
    except:
        print("Неверный url ! ")
        return 0
    current_chapter = ''
    current_heading = ''
    res = []
    for i in text:
        if(i.name != 'heading'):
            current_chapter += i.text
        else:
            res.append([current_heading, current_chapter])
            current_heading = i.text
            current_chapter = i.text
    with open('final.txt', 'w', encoding='utf-8') as f:
        for i in res:
            f.write('\n----------{}-----------\n'.format(i[0]) + i[1] + '\n-------------------\n')
    sum_all_shit(res)

get_chapters(url)
