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
from datetime import datetime

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
    input_file = open(input_file_path)
    data = json.load(input_file)
    input_file.close()
    print(f'ingest from {input_file_path}')
    embeddings_file = open(embedding_file_path,'wb')
    vectors = []

    for product in data:
        # print(product)
        title = ''
        company = ''
        location = ''
        post_date = ''
        if 'job_title' in product:
            title = product['job_title']
        if 'company_name' in product:
            company = product['company_name']
        if 'state' in product:
            location = product['state']
            if 'city' in product:
                location = location +' '+ product['city']
        if 'post_date' in product:
            post_date = product['post_date']
            post_date_object = datetime.strptime(post_date , '%Y-%m-%d')
            extract_date = datetime.strptime('2021-03-30' , '%Y-%m-%d')
            delta = extract_date  - post_date_object
            post_date = f'{delta} ago'

        job_text ='role: '+ title+' company: '+company+ ' location: '+location+' posted: '+ post_date
        vector = vectorize(job_text)
        id = encode(product['uniq_id'])
        vectors.append([index,id, vector])
    pickle.dump(vectors,  embeddings_file)
    embeddings_file.close()

def main():
    data_dir = '/Users/vli/Work/RetailSearch/MagpieSearch/data/'
    embedding_dir =  join(data_dir,'embeddings/')
    embedding_file_name = 'job_title_embedding'

    file_name = 'marketing_sample_for_seek_au-seek_au_job__20210101_20210331__30k_data.ldjson'
    file_path = join(data_dir,file_name)
    
    chunk_size = 1000
    output_dir = join(data_dir,'jobs/')
    output_file_name = 'seek'
    split_file( file_path, chunk_size, output_dir, output_file_name)

    data_files = [f for f in listdir(output_dir) if isfile(join(output_dir, f)) and 'seek' in f and '.json' in f]
    arguments = []
    for file_path in data_files:
        embedding_file_path = embedding_file_name+'-'+file_path.replace('.json','')+'.bin'
        arguments.append([join(output_dir,file_path), 
            join(data_dir,embedding_file_path)])
    with Pool(8) as p:
        # The arguments are passed as tuples
        p.starmap(ingest_from_file, arguments)

    print('Done', flush=True)

if __name__ == "__main__":
    main()

       