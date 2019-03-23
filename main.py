from datetime import datetime

import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.hackuniversity_2019

productCollection = db.product
orderCollection = db.order

for product in productCollection.find():
    # productCollection.update_one({'_id':product['_id']},{'$set':{'equipment_class':list(map(lambda it: it.strip(" '"),product['equipment_class'][1:-1].split(",")))}})
    bottleneck = 100000000000000000000000
    for productStageClass in product['equipment_class']:
        bottleneck = min(db.equipment.find_one({'class': productStageClass}, sort=[("speed_per_hour", 1)])[
                             'speed_per_hour'], bottleneck)
    # print(bottleneck)
for order in orderCollection.find():
    orderCollection.update_one({'_id': order['_id']},
                               {'$set': {'deadline_date': datetime.strptime(order['deadline'], "%Y-%m-%d")}})
