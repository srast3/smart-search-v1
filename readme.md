Smart Search & Product Recommendation: Personalized E-commerce Experience

Prerequisite:

Python 3.9.10 
pip install fastapi -> Framework/plugin on which API to search products is created
pip install uvicorn -> To run the API created using FASTAPI as a server
pip install -r requirements.txt


Run:

python Main.py -> To laod the products to Cosmos DB for MongoDB vCore
uvicorn Search:app --reload -> To start the search API

API Links:

http://127.0.0.1:8000/search?query=cheap%20mobile
http://127.0.0.1:8000/docs

Steps:

1. Create Collection “Product” in Cosmos DB
2. Create Index for the property “contentVector” in the above created collection (“Product”)
3. Create vector embeddings for all products using text-embedding-ada-002 model 
4. Store each product data (product data + Vector Embedding together) in to Cosmos DB for Mongo DB vCore. With this step we have added all product data. Example product data in the Cosmos DB
	{
        "productId": 8,
        "productName": "Huawei P60 Pro",
        .
		.
		.
		"contentVector": Vector Embedding created using text-embedding-ada-002 model
    }
5. When user search for a query (EG. phone with low light camera), create Vector Embedding for the query using text-embedding-ada-002 model  
6. Call the Cosmos DB - Vector Search method by passing the above created user query Vector Embedding.
7. Above step will return the semantic search results with product details, display these resulted products in the Frontend UI application.                  
