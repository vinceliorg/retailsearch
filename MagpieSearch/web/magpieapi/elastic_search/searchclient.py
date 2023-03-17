from elasticsearch import Elasticsearch
import math
import ast
import pystache
import json
es = Elasticsearch( 'http://localhost:9200/')

# TODO: configure this as static file or read from a sever
query_template_path = '/Users/vli/Work/RetailSearch/MagpieSearch/web/magpieapi/elastic_search/configure/query_template.js'
index_name = 'grocery-index'

with open(query_template_path , 'r') as f:
    query_template = json.load(f)
    
def search(index_name, keywords,retrieval_boolean_operator='or', page=1, page_size=20):
    elastic_query = pystache.render(json.dumps(query_template), {'query': keywords, 'retrieval_boolean_operator':retrieval_boolean_operator })
    res = es.search(index=index_name, 
                    query=json.loads(elastic_query)['query'],from_ = page_size*(page-1),size = page_size)
    return res['hits']