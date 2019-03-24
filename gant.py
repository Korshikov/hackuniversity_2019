import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
import pymongo

plotly.tools.set_credentials_file(username='pashaa22', api_key='xeYmeBpedvF3aitPtesI')

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.hackuniversity_2019

reservationEqCollection = db.reservation_eq

df = list(map(lambda it: dict(Task=str(it['order_id']), Start=it['start'].strftime('%Y-%m-%d %H:%M'),
                              Finish=it['finish'].strftime('%Y-%m-%d %H:%M'), Resource=str(it['equipment_id'])),
              reservationEqCollection.find()))

fig = ff.create_gantt(df)
py.iplot(fig, filename='gantt-string-variable', world_readable=True)
