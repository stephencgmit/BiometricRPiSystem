import json
from pymongo import MongoClient
import time
from pyfingerprint import *
import pycode 


client = MongoClient("mongodb://fpDBuser:project2019@fingerprintproject-shard-00-00-2ee1v.mongodb."
                     "net:27017,fingerprintproject-shard-00-01-2ee1v.mongodb.net:27017,"
                     "fingerprintproject-shard-00-02-2ee1v.mongodb.net:27017/test?ssl=true&replicaSet="
                     "FingerprintProject-shard-0&authSource=admin&retryWrites=true")

mydb = client['fingerprint_project']
connect_to_collection = mydb['students']

mydict = {"name": "Eddy", "college": "gmit"}
x=connect_to_collection.insert_one(mydict)