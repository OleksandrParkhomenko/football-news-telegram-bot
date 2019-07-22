from bs4 import BeautifulSoup

import requests
import re


URL = 'https://isport.ua'


def findMention(word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search


def get_article_content(url):
    page = requests.get(url)
    response = BeautifulSoup(page.content, 'html.parser')
    buff = response.select('div#article_content p')[:-1]
    article = " "
    for elem in buff:
        article += elem.get_text()

    return article.replace(u'\xa0', u' ')


def parse_page(soup):
    articles = soup.select('div.article_section')
    for article in articles:
        #img = article.select('a.article__img_link img')[0]['data-src']
        href = URL + article.select('a.article__img_link')[0]['href']
        title = article.select('div.article__title')[0].get_text()
        subtitle = article.select('div.article__subtitle')[0].get_text()
        time = article.select('div.article__time')[0].get_text()

        yield {# 'img' : img,
                 'href' : href,
                 'text' : title + " " + subtitle,
                 #'subtitle' : subtitle,
                 'time' : time
                }


def get_news_about(what, time=10):
    url = URL + '/693219-news'
    for i in range(time):
        page = requests.get(url)
        response = BeautifulSoup(page.content, 'html.parser')

        for article in parse_page(response):
            if findMention(what)(article['text']):
                article['content'] = get_article_content(article['href'])
                yield article

            # if not findMention('сегодня')(article['time']) and \
            #     not findMention('вчера')(article['time']):
            #     return "Old article"


        url = URL + response.select('li.next a')[0]['href']


def get_MU_news():
    yield from get_news_about('мю')
    yield from get_news_about('манчестер юнайтед')
