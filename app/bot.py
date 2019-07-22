import requests
import json
import isport
import misc


#https://api.telegram.org/<TOKEN>/<METHOD>
token = misc.token
URL = 'https://api.telegram.org/bot' + token + '/'

def get_updates():
    url = URL + 'getupdates'
    response = requests.get(url)
    return response.json()


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def deleteSetWebhook():
#https://api.telegram.org/<TOKEN>/setWebhook?url=
#https://api.telegram.org/<TOKEN>/deleteWebhook
    pass


def get_message(response):
    chat_id = response['message']['chat']['id']
    message_text = response['message']['text']

    message = { 'chat_id' : chat_id,
                    'text' : message_text }

    return message


def send_message(chat_id, text="Подожди секундочку, ищу...", what="МЮ"):
    news = isport.get_MU_news() if what == "МЮ" else isport.get_news_about(what)
    url = URL + 'sendMessage'

    requests.post(url,
            json= { 'chat_id' : chat_id,
                    'text' : text })

    for article in news:
        text = "\n" + article['content'] + "\n\n" + article['href']
        message = {'chat_id' : chat_id, 'text' : text }
        requests.post(url, json=message)

    requests.post(url,
            json= { 'chat_id' : chat_id,
                   'text' : 'Это все последние новости про {}'.format(what)})


def bot(response):
    answer = get_message(response)

    if answer != None:
        if isport.findMention('Найди про')(answer['text']) and len(answer['text']) >= 3:
            what = ' '.join(answer['text'].split()[2:])
            send_message(answer['chat_id'], what=what)
        else:
            send_message(answer['chat_id'])
