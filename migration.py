
URL = 'mongodb://localhost:27017/'
DBNAME = 'maestro-client'




from pymongo import MongoClient
from pymongo import InsertOne, UpdateOne
from bson.objectid import ObjectId

client = MongoClient(URL)
db = client[DBNAME]

apps = db.applications
servers = db.servers


for app in apps.find({ 'servers': { '$exists': True} }):
    if 'servers' in app and app['servers']:
        if len(app['servers']) > 0:
            napp = app.copy()
            del napp['servers']
            del napp['updated_at']

            result = db.applications.update_one({'_id': app['_id']}, {'$unset': { 'servers': True }, '$currentDate': { 'updated_at': True }})
            print('app -> ', app['_id'], result.raw_result)

            tmp_app = {k: napp.get(k, None) for k in ('_id', 'name', 'family')}

            for server in app['servers']:
                result = db.servers.update_one({'_id': server}, {'$set': {'applications': [tmp_app]}})
                print('server -> ', server, result.raw_result)
                print(server)




