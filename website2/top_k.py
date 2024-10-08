import sys
import json
import pymongo
from scipy import spatial
import numpy as np
import certifi
from pymongo.mongo_client import MongoClient

# Read the input from stdin
data_input = sys.stdin.read()
user_data = json.loads(data_input)
vector_array = user_data['vector']#get the vector from the array
query_embedding = vector_array

from typing import List, Optional
from scipy import spatial

def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
import certifi
import os


cluster = MongoClient("mongodb+srv://Nate:admin@dormie.0whqn7z.mongodb.net/?retryWrites=true&w=majority&appName=Dormie", tlsCAFile=certifi.where())
database = cluster['Dormie']
collection = database['user_data4']

import re
#use this for search
if user_data.get('search_array'):
    query = {}
    for item in user_data['search_array']:
        query[item['search_term']] = { '$in': [re.compile(q, re.IGNORECASE) for q in item['query']]}
    user_array = collection.find(query)
else:
    user_array = collection.find()  # #get every user's embedding (including the user we're using to query)


docs_array = []
embeddings = []
for doc in user_array:
    embeddings.append(doc["vector"])
    docs_array.append({k: v for k, v in doc.items() if k != '_id'})

distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine") #calculate the distances
import numpy as np

def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
    return np.argsort(distances)

indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances) #get the indices of the nearest neighbors

print(json.dumps([docs_array[x] for x in indices_of_nearest_neighbors]), flush=True)
