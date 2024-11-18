import os

from dotenv import load_dotenv
from AzureOpenAIClient import *
from CosmosServiceClient import *
from Utilities import *

class LoadProductData:
    def __init__(self):
        load_dotenv()
        self.client = AzureOpenAIClient()
        self.utilities = Utilities()
        self.db = CosmosServiceClient()
    
    def insert_product_data(self, data):
      try:
          data[os.getenv("COSMOS_DB_VECTOR_PROPERTY_NAME")] = self.client.generate_embeddings(os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"), json.dumps(data))
          result = self.db.insert_data(os.getenv("COSMOS_DB_COLLECTION_NAME"), data)
          return result
      except Exception as e:
          print(f"An error occurred: {e}")
          return None

    def load_product_data_into_cosmos_db(self):
      self.db.create_collection(os.getenv("COSMOS_DB_COLLECTION_NAME"))
      self.db.create_index(os.getenv("COSMOS_DB_COLLECTION_NAME"), os.getenv("COSMOS_DB_VECTOR_PROPERTY_INDEX_NAME"), os.getenv("COSMOS_DB_VECTOR_PROPERTY_INDEX_TYPE"), os.getenv("COSMOS_DB_VECTOR_PROPERTY_NAME"))
      self.db.create_filter_index(os.getenv("COSMOS_DB_COLLECTION_NAME"), os.getenv("COSMOS_DB_VECTOR_PROPERTY_FILTER_INDEX_NAME"), os.getenv("COSMOS_DB_VECTOR_FILTER_PROPERTY_NAME"))
      jsonData =self.utilities.getJsonDataFromFile(os.getenv("DATASET_FILE_NAME_WITH_PATH")) 
      for obj in jsonData:
        self.insert_product_data(obj)
      print("\nAll Products inserted to Cosmos DB for Mongo DB vCore successfully.\n")
