from datetime import datetime
import pandas as pd
import math
import requests
import json
from os import listdir
from os.path import isfile, join
import pickle
from multiprocessing import Process
from multiprocessing import Pool
import sys
sys.path.insert(1, '../utils/')
from embeddings import vectorize
from text_utils import encode

index = 0
encodes = []

def ingest_from_file(input_file_path, embedding_file_path):
    # Opening JSON file
    input_file = open(input_file_path)
    data = json.load(input_file)
    input_file.close()
    print(f'ingest from {input_file_path}')

    embeddings_file = open(embedding_file_path,'wb')
    vectors = []
    for product in data: 
        vector = vectorize(product['title'])
        id = encode(product['url'])
        vectors.append([index,id, vector])
    pickle.dump(vectors,  embeddings_file)
    embeddings_file.close()

def main():
    data_dir = '/Users/vli/Work/RetailSearch/RetailSearch/data'
    embedding_file_name = 'embedding'
    data_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f)) and 'product' in f and '.json' in f]
    arguments = []
    for file_path in data_files:
        mbedding_file_path = embedding_file_name+'-'+file_path.replace('.json','')+'.bin'
        arguments.append([join(data_dir,file_path), 
            join(data_dir,mbedding_file_path)])
    with Pool(8) as p:
        # The arguments are passed as tuples
        p.starmap(ingest_from_file, arguments)

    print('Done', flush=True)

if __name__ == "__main__":
    main()

       