from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd
import math
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import json

end_point = 'http://localhost:9200'
es = Elasticsearch(end_point)

mapping_path = 'mapping.json'
def main():
    # Opening JSON file
    f = open(mapping_path)
    mapping= json.load(f)
    f.close()
    INDEX_NAME = 'grocery-index'
    es.indices.create(index=INDEX_NAME, ignore=400, body=mapping)
    print(f'index {INDEX_NAME} created')
if __name__ == "__main__":
    main()
