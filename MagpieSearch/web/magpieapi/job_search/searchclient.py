import faiss                   # make faiss available
import numpy as np
from os import listdir
from os.path import isfile, join
import pickle
import json
import hashlib
import pandas as pd
import sys
sys.path.insert(1, '../../utils/')
from embeddings import vectorize
from text_utils import encode
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis_docs = redis.Redis(connection_pool=pool)

# TO DO: upload to cloud
d = 1536  
project_root = '/Users/vli/Work/RetailSearch/'
faiss_index_path = 'MagpieSearch/deployment/faiss/index/seek_jobs.fi'
faiss_index_path = join(project_root,faiss_index_path)
search_index = faiss.read_index(faiss_index_path)

doc_id_path = 'MagpieSearch//deployment/faiss/index/seek_jobs.id'
doc_id_path  = join(project_root,doc_id_path )
doc_idx = pickle.load(open(doc_id_path, "rb"))

def search(text):
    encode = vectorize(text)
    D, I = search_index.search(np.array([encode]), 20)
    result_ids = doc_idx[I[0]]
    results = redis_docs.mget(result_ids)
    return results
