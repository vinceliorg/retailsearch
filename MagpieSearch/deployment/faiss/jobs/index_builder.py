import faiss                   # make faiss available
import numpy as np
from os import listdir
from os.path import isfile, join
import pickle
import json
import hashlib
import pandas as pd
# TO DO: add to configuration file

def ingest_from_file(data_dir,embedding_size, index_path, doc_index_path):
    data_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f)) and '.bin' in f]

    data = []
    for file in data_files:
        f = open(join(data_dir, file),'rb')
        data.append(pickle.load(f))
        # close the file
        f.close()

    embeddings = []
    ids = []
    for dt in data:
        for record in dt:
            embeddings.append(record[2])
            ids.append(record[1])
    embeddings = np.array(embeddings)
    ids = np.array(ids)
    n_bits = 2 * embedding_size
    lsh = faiss.IndexLSH (embedding_size, n_bits)
    lsh.train (embeddings)
    lsh.add (embeddings)
    
    faiss.write_index(lsh, index_path)
    print(f'faiss index write to {index_path}')
    f = open(doc_index_path, 'wb')
    pickle.dump(ids, f)
    f.close()
    print(f'doc index write to {doc_index_path}')
def main():
    d = 1536
    data_dir = '/Users/vli/Work/RetailSearch/MagpieSearch/data/embeddings/jobs'
    # fi -> faiss index
    index_path = '/Users/vli/Work/RetailSearch/MagpieSearch/deployment/faiss/index/seek_jobs.fi'
    #id -> doc id map
    doc_index_path = '/Users/vli/Work/RetailSearch/MagpieSearch/deployment/faiss/index/seek_jobs.id'
    ingest_from_file(data_dir,d, index_path, doc_index_path)
if __name__ == "__main__":
    main()