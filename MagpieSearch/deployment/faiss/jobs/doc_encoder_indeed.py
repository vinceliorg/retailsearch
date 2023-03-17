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
sys.path.insert(1, '../../../utils/')
from embeddings import vectorize
from text_utils import encode
from os import makedirs, mkdir

index = 0
encodes = []

def split_file(input_file_path, chunk_size, output_dir, output_file_name):
    print(f'split {input_file_path} to {chunk_size} files')
    data = []
    # Opening JSON file
    with open(input_file_path) as f:
        for line in f:
            try:
                job = json.loads(line)
                data.append(job)
            except:
                continue
    chunk_flag = 1
    try:
        makedirs(output_dir, exist_ok = True)
        print("Directory '%s' created successfully" % output_dir)
    except OSError as error:
        print("Directory '%s' can not be created" % output_dir)
        mkdir(output_dir, mode = 777, dir_fd = None)

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        with open(join(output_dir,f'{output_file_name}-{chunk_flag}.json'), 'w') as f:
            json.dump(chunk, f)
        chunk_flag = chunk_flag+1

    print(f'split done.')


    

def ingest_from_file(input_file_path, embedding_file_path):
    # Opening JSON file
    data = pd.read_csv(input_file_path)
 
    print(f'ingest from {input_file_path}')
    embeddings_file = open(embedding_file_path,'wb')
    vectors = []

    for i,product in data.iterrows(): 
        vector = vectorize(product.Title)
        id = product.id
        vectors.append([index, id, vector])
    pickle.dump(vectors,  embeddings_file)
    embeddings_file.close()

def main():
    data_dir = '/Users/vli/Work/RetailSearch/MagpieSearch/data/jobs'
    embedding_dir =  join(data_dir,'embeddings/')
    embedding_file_name = 'indeed_job_title_embedding'

    file_name = 'indeed_jobs_march_2023.csv'
    file_path = join(data_dir,file_name)

    embedding_file_path = embedding_file_name+'-'+file_name.replace('.csv','')+'.bin'
    ingest_from_file(file_path,embedding_file_path)

    print('Done', flush=True)

if __name__ == "__main__":
    main()

       