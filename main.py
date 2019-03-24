from datetime import datetime, timedelta

import pymongo

start_date = datetime.strptime("2019-03-18", "%Y-%m-%d")

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.hackuniversity_2019

productCollection = db.product_2
equipmentCollection = db.equipment_2
orderCollection = db.order
reservationEqCollection = db.reservation_eq


# for product in productCollection.find():
#     productCollection.update_one({'_id':product['_id']},{'$set':{'equipment_class':list(map(lambda it: it.strip(" '"),product['equipment_class'][1:-1].split(",")))}})

# try to find connected component
# for equipmentClass in equipmentCollection.find().distinct("class"):
#     print("%s: %d %s" % (equipmentClass, productCollection.count_documents({'equipment_class': equipmentClass}),
#                          list(map(lambda it: it['_id'], productCollection.find({'equipment_class': equipmentClass})))))
# Oh nothing intresting

# for order in orderCollection.find():
#     orderCollection.update_one({'_id': order['_id']},
#                                {'$set': {'deadline_date': datetime.strptime(order['deadline'], "%Y-%m-%d") + timedelta(days=1)}})

def day_part(t):
    "Return timedelta between midnight and `t`."
    return t - t.replace(hour = 0, minute = 0, second = 0)

def datetime_by_adding_business_hour(from_time, add_hour):
    business_hour_to_add = timedelta(hours=add_hour)
    while(business_hour_to_add > timedelta(minutes=0)):
        if(from_time.weekday()>=5):
            from_time+= timedelta(days=2)
        if(business_hour_to_add>timedelta(days=1)):
            from_time+=timedelta(days=1)
            business_hour_to_add -= timedelta(days=1)
        else:
            from_time+=business_hour_to_add
            if (from_time.weekday() >= 5):
                from_time += timedelta(days=2)
            business_hour_to_add = timedelta(minutes=0)
    return from_time
    # return from_time + timedelta(hours=business_hour_to_add)
    # while business_days_to_add > 0:
    #     current_date += datetime.timedelta(days=1)
    #     weekday = current_date.weekday()
    #     if weekday >= 5: # sunday = 6
    #         continue
    #     business_days_to_add -= 1
    # return current_date


for order in orderCollection.find({'deadline_date': {'$gte': start_date}}, sort=[('deadline_date', 1)]):
    product = productCollection.find_one({'_id': order['product_id']})
    suitableEquipmentIdSpeedPairOrderedBy = list(map(lambda it: (it['_id'], it['speed_per_hour']),
                                                     equipmentCollection.find(
                                                         {'class': {'$in': product['equipment_class']}},
                                                         sort=[('speed_per_hour', -1)])))
    bestEquip = None
    finished_time = order['deadline']
    for suitableEquipment in suitableEquipmentIdSpeedPairOrderedBy:
        prevEquipTask = reservationEqCollection.find_one(
            {'equipment_id': suitableEquipment[0]},
            sort=[('finish', -1)])
        if prevEquipTask is None:
            startTime = start_date
        else:
            startTime = prevEquipTask['finish']
        tmp = divmod(order['amount'], suitableEquipment[1])
        countHour = tmp[0] + 1 if tmp[1] > 0 else 0
        if (datetime_by_adding_business_hour(startTime, countHour) <= order['deadline_date']):
            reservationEqCollection.insert_one(
                {'equipment_id': suitableEquipment[0], 'order_id': order['_id'], 'amount': order['amount'],
                 'start': startTime, 'finish': datetime_by_adding_business_hour(startTime, countHour)})
            break

        # count find unused
    # prevEquipTask = reservationEqCollection.find_one(
    #     {'equipment_id': {'$in': list(map(lambda it: it[0], suitableEquipmentIdSpeedPairOrderedBy))}},
    #     sort=[('finish', -1)])
    # if bestEquip is None:
    #     startTime = start_date
    #     bestEquip=suitableEquipmentIdSpeedPairOrderedBy[0]
    # else:
    #     startTime = bestEquip
    # print(suitableEquipmentIdSpeedPairOrderedBy)
