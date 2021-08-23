import os
import requests
import json

AccessToken = os.environ.get('AccessToken')
IntercomUrl = 'https://api.intercom.io/articles'
headers = {
    'Authorization': 'Bearer ' + AccessToken,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def delete_all_articles():
    article_ids = list_all_articles()
    for article_id in article_ids:
        r = requests.delete(IntercomUrl + '/' + article_id, headers=headers)
        print(str(id))
        print(r.status_code)
        print(r.text)
        print(r.headers)
    print('Complete')


def list_all_articles():
    r = requests.get(IntercomUrl, headers=headers)
    articles_json = json.loads(r.text)
    number_of_pages = articles_json['pages']['total_pages']

    if number_of_pages > 1:
        print('More than one page')
        article_ids = multiple_pages_of_articles(articles_json)
    else:
        print('One page or less')
        article_ids = one_page_of_articles(articles_json)

    return article_ids


def get_article_ids(article_json):
    article_ids = []
    articles = article_json['data']

    for article in articles:
        current_id = article['id']
        article_ids.append(current_id)
    return article_ids


def one_page_of_articles(article_json):
    article_ids = []
    current_ids = get_article_ids(article_json)
    article_ids += current_ids
    return article_ids


def multiple_pages_of_articles(articles_json):
    article_ids = []
    current_ids = get_article_ids(articles_json)
    article_ids += current_ids

    number_of_pages = articles_json['pages']['total_pages']
    print(str(number_of_pages) + ' pages of contacts')
    print('Page 1 ids gathered')

    for request in range(1, number_of_pages):
        next_page_url = articles_json['pages']['next']
        print(next_page_url)
        r = requests.get(next_page_url, headers=headers)
        articles_json = json.loads(r.text)
        current_ids = get_article_ids(articles_json)
        article_ids += current_ids

        if 'next' in articles_json['pages']:
            new_page_url = articles_json['pages']['next']
            next_page_url.replace(articles_json['pages']['next'], new_page_url)
            print('Page ' + str(request + 1) + ' ids gathered')
        else:
            print('Page ' + str(request + 1) + ' ids gathered')
    return article_ids


if __name__ == '__main__':
    delete_all_articles()
