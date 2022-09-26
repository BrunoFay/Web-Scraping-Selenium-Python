from pymongo import MongoClient

def get_database():

   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&ssl=false"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client['Products']

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

   # Get the database
   db = get_database()
   sneakers_collection = db['Sneakers']
   nike_collection = db['Nike']
   clothes_collection = db['Clothes']
   adidas_collection = db['Adidas']
   vans_collection = db['Vans']
   puma_collection = db['Puma']
   skate_collection = db['Skate']
   accessories_collection = db['Accessories']
