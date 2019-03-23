import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.hackuniversity_2019

# productCollection = db.product
#
# for product in productCollection.find():
#     productCollection.update_one({'_id':product['_id']},{'$set':{'equipment_class':list(map(lambda it: it.strip(" '"),product['equipment_class'][1:-1].split(",")))}})