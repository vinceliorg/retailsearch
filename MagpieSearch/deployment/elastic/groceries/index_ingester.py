from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd
import math
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import json
import hashlib
from os import listdir
from os.path import isfile, join

def encode(text):
    hash_object = hashlib.md5(text.encode('utf-8'))
    return hash_object.hexdigest()

es = Elasticsearch( 'http://localhost:9200')
encoder_endpoint = "https://api.openai.com/v1/embeddings"
INDEX_NAME = 'grocery-index'
def process_text(html):
    if html is None:
        return ''
    soup = BeautifulSoup(html, 'html.parser')
    node = soup.find("div", {"class": "sc-a2942c6c-3 dgpqzY coles-targeting-SectionHeaderDescription"})
    if node is None:
        return node
    return node.text.replace(u'\xa0', u' ')

def ingest_from_file(file_path):
    # Opening JSON file
    f = open(file_path)
    data = json.load(f)
    f.close()
    print(f'ingest from {file_path}')
    for product in data:
        prod_json = {}
        prod_json['id'] = encode(product['url'])
        prod_json['title'] = product['title']
        prod_json['source'] = 'COLES'
        prod_json['pricetext'] = product['price']
        prod_json['price'] = float(product['price'].replace('$','')) if product['price'] is not None else None
        prod_json['packageprice'] = product['package_price']
        prod_json['productimage'] = product['product_image']
        prod_json['productdetails'] = process_text(product['product_details'])
        prod_json['url'] = product['url']
        # print (prod_json)
        try :
            res = es.index(index=INDEX_NAME, id=prod_json['id'], body=prod_json)
            # print(res['result'])
        except Exception as e:
            print ('index error')
            print(str(e))
    print('index_completed')
def main():
    data_dir = '/Users/vli/Work/RetailSearch/MagpieSearch/data'
    data_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f)) and 'product' in f]
    for file_path in data_files:
        ingest_from_file(join(data_dir,file_path))
if __name__ == "__main__":
    main()