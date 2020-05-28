from django.views.generic import View
from django.shortcuts import render
import json
import requests

SEARCH_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId=1002196771843734307'


def get_data(title):
    params = {
        'title': title
    }

    api = requests.get(SEARCH_URL, params=params).text
    result = json.loads(api)

    book_data = []
    for i in result['Items']:
        item = i['Item']
        title = item['title']
        image = item['largeImageUrl']
        query = {
            'title': title,
            'image': image
        }
        book_data.append(query)
    return book_data


class IndexView(View):
    def get(self, request, *args, **kwargs):
        book_data = []

        return render(request, 'app/index.html', {
            'book_data': book_data
        })

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search')

        book_data = get_data(search)

        return render(request, 'app/index.html', {
            'book_data': book_data
        })
