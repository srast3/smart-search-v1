import os
import pymongo
from dotenv import load_dotenv

class CosmosServiceClient:
    def __init__(self):
      load_dotenv()
      self.mongo_conn = os.getenv("COSMOS_DB_CONNECTION_STRING")
      self.mongo_client = pymongo.MongoClient(self.mongo_conn)
      self.db = self.mongo_client[os.getenv("COSMOS_DB_DATABASE_NAME")]

    def create_collection(self, collection_name):
      self.db.drop_collection(collection_name)
      self.db.create_collection(collection_name)

    def create_index(self, collection, index_name, index_type, vector_property_name):
      self.db.command({
      'createIndexes': collection,
      'indexes': [
          {
            'name': index_name,
            'key': {
              'contentVector': "cosmosSearch"
            },
            'cosmosSearchOptions': {
              'kind': index_type,
              'numLists': 1,
              'similarity': 'COS', # other options are 'L2' or 'IP'
              'dimensions': 1536
          }
          }
        ]
      });
    
    def create_filter_index(self, collection, filter_index_name, filter_vector_property_name):
      self.db.command({ 
     "createIndexes": collection,
     "indexes": [ {
        "key": { 
            filter_vector_property_name: 1 
               }, 
        "name": filter_index_name 
        } ] 
     });
    
    def create_filter_index(self, collection, filter_index_name, filter_vector_property_name):
      self.db.command({ 
     "createIndexes": collection,
     "indexes": [ {
        "key": { 
            filter_vector_property_name: 1 
               }, 
        "name": filter_index_name 
        } ] 
     });

    def insert_data(self, collection, data):
      return self.db[collection].insert_one(data)

    def get_vector_search(self, collection_name, query_vector, num_results, query):
      collection = self.db[collection_name]
      pipeline = [
            {
                '$search': {
                    "cosmosSearch": {
                      "vector": query_vector,
                      "numLists": 1,
                      "path": "contentVector",
                      "k": num_results,
                      "filter": query
                    },
                    "returnStoredSource": True }},
            {'$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document' : '$$ROOT' } }
      ]
      return collection.aggregate(pipeline)
