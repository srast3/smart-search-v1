import os
import openai
from openai import AzureOpenAI
from dotenv import load_dotenv

class AzureOpenAIClient:
    def __init__(self):
        load_dotenv()
        self.client = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),
            api_version = os.getenv("OPENAI_API_VERSION"),
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    def generate_embeddings(self, embedding_deployment_name, data):
        try:
            response = self.client.embeddings.create(
                model = embedding_deployment_name, input = data)
            embeddings = response.data[0].embedding
            return embeddings
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
