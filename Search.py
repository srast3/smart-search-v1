import os
import fastapi
import re
 
from fastapi import FastAPI
from CosmosServiceClient import *
from AzureOpenAIClient import *
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
 
 
load_dotenv()
 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
 
@app.get("/")
def home():
    return {"use": "call /search to search for products"}
 
@app.get("/search")
def search(query: str):
    response = []
    print("Searching for: " + query)
    results = vector_search(query, 5)
    for res in results:
        data = { 'id': res['document']['id'],
                'name': res['document']['name'],
                'price': res['document']['price'],
                'storage': res['document']['specification']['storage'],
                'modelName': res['document']['specification']['modelName'],
                'battery': res['document']['specification']['battery']['power'],
                'cameraResolution': res['document']['specification']['camera']['backCamera'],  
                'lowLightCapability': res['document']['specification']['camera']['lowLightCapability'],
                'similarityScore': res['similarityScore']}
        response.append(data);
    return response
 
def vector_search(query, num_results):
    client = AzureOpenAIClient()
    query_vector = client.generate_embeddings(os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"), query)
    db = CosmosServiceClient()
    query = getPriceFilters(query)
    results = db.get_vector_search(os.getenv("COSMOS_DB_COLLECTION_NAME"), query_vector, num_results, query)
    return results
 
def getPriceFilters(t):
    if "price" in t and "less than" in t:
        m = re.search('(?<=price less than )(.*)', t)
        if m:
            return {"price": {"$lt": int(m.group(1))}}
    elif "under" in t:
        m = re.search('(?<=under )(.*)', t)
        if m:
            return {"price": {"$lt": int(m.group(1))}}
    elif "price" in t and "greater than equal to" in t:
        m = re.search('(?<=greater than equal to )(.*)', t)
        if m:
            return {"price": {"$gte": int(m.group(1))}}
    elif "price" in t and "more than" in t:
        m = re.search('(?<=more than )(.*)', t)
        if m:
            return {"price": {"$gt": int(m.group(1))}}
    elif "price" in t and "greater than" in t:
        m = re.search('(?<=price greater than )(.*)', t)
        if m:
            return {"price": {"$gt": int(m.group(1))}}
    return {"price": {"$nin": [0]}}