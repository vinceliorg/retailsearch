import redis
import sys
sys.path.insert(1, '../../utils/')
from text_utils import encode
import numpy as np
from os import listdir
from os.path import isfile, join
import json
import pickle

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis_docs = redis.Redis(connection_pool=pool)

pool = redis.ConnectionPool(host='localhost', port=6400, db=0)
redis_embedding = redis.Redis(connection_pool=pool)

embedding_dir = '/Users/vli/Work/RetailSearch/RetailSearch/data/embeddings'
embedding_files = [f for f in listdir(embedding_dir) if isfile(join(embedding_dir, f)) and '.bin' in f]

data = []
for file in embedding_files:
    f = open(join(embedding_dir, file),'rb')
    data.append(pickle.load(f))
    # close the file
    f.close()
embeddings = {}

for dt in data:
    for record in dt:
        embeddings[record[1]] = record[2]


data_dir = '/Users/vli/Work/RetailSearch/RetailSearch/data/'
data_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f)) and '.json' in f]
for data_file in data_files:
    input_file_path = join(data_dir,data_file)
    print(input_file_path)
    input_file = open(input_file_path)
    products = json.load(input_file)
    for product in products:
        id = encode(product['url'])
        embedding = embeddings[id]
        product['id'] = id
        # product=embeddings[id]
        redis_docs.set(id, json.dumps(product))
        redis_embedding.set(id, json.dumps({"vector": embedding}))
    input_file.close()

