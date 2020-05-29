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
        isbn = item['isbn']
        query = {
            'title': title,
            'image': image,
            'isbn': isbn
        }
        book_data.append(query)
    return book_data


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/index.html')

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search')

        book_data = get_data(search)

        return render(request, 'app/index.html', {
            'book_data': book_data
        })


class DetailView(View):
    def get(self, request, *args, **kwargs):
        isbn = self.kwargs['isbn']

        params = {
            'isbn': isbn
        }

        api = requests.get(SEARCH_URL, params=params).text
        result = json.loads(api)

        book_data = []
        for i in result['Items']:
            item = i['Item']
            title = item['title']
            image = item['largeImageUrl']
            author = item['author']
            itemPrice = item['itemPrice']
            salesDate = item['salesDate']
            publisherName = item['publisherName']
            size = item['size']
            isbn = item['isbn']
            itemCaption = item['itemCaption']
            itemUrl = item['itemUrl']
            reviewAverage = item['reviewAverage']
            reviewCount = item['reviewCount']

            query = {
                'title': title,
                'image': image,
                'author': author,
                'itemPrice': itemPrice,
                'salesDate': salesDate,
                'publisherName': publisherName,
                'size': size,
                'isbn': isbn,
                'itemCaption': itemCaption,
                'itemUrl': itemUrl,
                'reviewAverage': reviewAverage,
                'reviewCount': reviewCount,
                'average': float(reviewAverage) * 20,
            }
            book_data.append(query)

        return render(request, 'app/detail.html', {
            'book_data': book_data[0]
        })
