from django.conf import settings
from django.shortcuts import render, redirect
import json
import urllib
import elastic_search.searchclient as elastic
import semantic_search.searchclient as semantic
import job_search.searchclient as jobsearcher

def index(request):
    context={}
    search_method = 'elastic'
    if request.method == 'POST':
        print(request.POST)
        keywords=request.POST['keywords']
        if 'searchmethod' in request.POST:
            search_method = request.POST['searchmethod']
        results = []
        if search_method == 'elastic':
            print('I love elastic search')
            index_name = 'grocery-index'
            print(f'keywords are {keywords}')
            esresults = elastic.search(index_name, keywords=keywords)
            for result in esresults['hits']:
                 results.append({'id':result['_source']['id'],
                                 'title':result['_source']['title'],
                                 'price':result['_source']['pricetext'],
                                 'packageprice':result['_source']['packageprice'],
                                 'productimage':result['_source']['productimage'],
                                 'productdetails':result['_source']['productdetails'],
                                 'url':result['_source']['url']})
            context['hits'] = results
            context['keywords'] = keywords
        elif search_method == 'semantic':
            print('yes, I\'m doing semantic search')
            seresults= semantic.search(keywords)
            for result in seresults:
                result = json.loads(result)
                results.append({'id':result['id'],
                                 'title':result['title'],
                                 'price':result['price'],
                                 'packageprice':result['package_price'],
                                 'productdetails':result['product_details'],
                                 'productimage':result['product_image'],
                                 'url':result['url']})
            context['hits'] = results
            context['keywords'] = keywords
    elif request.method == 'GET':
        # print('yes get request')
        keywords = ''
        page=1
        results = []
        if 'keywords' in request.GET:
            keywords=request.GET['keywords']
        if 'page' in request.GET:
            page=int(request.GET['page'])
        if keywords is not None and keywords != '':
                 results = []
        if 'searchmethod' in request.GET:
            search_method = request.GET['searchmethod']
        if search_method == 'elastic':
            index_name = 'grocery-index'
            esresults = elastic.search(index_name, keywords=keywords)
            for result in esresults['hits']:
                 results.append({'id':result['_source']['id'],
                                 'title':result['_source']['title'],
                                 'price':result['_source']['pricetext'],
                                 'packageprice':result['_source']['packageprice'],
                                 'productimage':result['_source']['productimage'],
                                 'productdetails':result['_source']['productdetails'],
                                 'url':result['_source']['url']})
            context['hits'] = results
            context['keywords'] = keywords
        elif search_method == 'semantic':
            print('yes, I\'m doing semantic search')
            seresults= semantic.search(keywords)
            for result in seresults:
                result = json.loads(result)
                results.append({'id':result['id'],
                                 'title':result['title'],
                                 'price':result['price'],
                                 'packageprice':result['package_price'],
                                 'productdetails':result['product_details'],
                                 'productimage':result['product_image'],
                                 'url':result['url']})
            context['hits'] = results
            context['keywords'] = keywords
    return render(request, 'search.html', context)

def jobsearch(request):
    context={}
    if request.method == 'POST':
        print(request.POST)
        keywords=request.POST['keywords']
        results = []
       
        seresults= jobsearcher.search(keywords)
        for result in seresults:
            result = json.loads(result)
            results.append({'id':result['id'],
                                'title':result['job_title'],
                                'category':result['category'],
                                # 'city':result['city'],
                                'state':result['state'],
                                'job_description':result['job_description'],
                                'date_posted':result['post_date']})
        context['hits'] = results
        context['keywords'] = keywords
    elif request.method == 'GET':
        # print('yes get request')
        keywords = ''
        page=1
        results = []
        if 'keywords' in request.GET:
            keywords=request.GET['keywords']
        if 'page' in request.GET:
            page=int(request.GET['page'])
        if keywords is not None and keywords != '':
                 results = []
        if keywords!='':
            seresults= jobsearcher.search(keywords)
            for result in seresults:
                result = json.loads(result)
                results.append({'id':result['id'],
                                    'title':result['job_title'],
                                    'category':result['category'],
                                    'city':result['city'],
                                    'state':result['state'],
                                    'job_description':result['job_description'],
                                    'date_posted':result['post_date']})
        context['hits'] = results
        context['keywords'] = keywords
    return render(request, 'jobsearch.html', context)