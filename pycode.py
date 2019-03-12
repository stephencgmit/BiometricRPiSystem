import pymongo
from pymongo import MongoClient
from pyfingerprint.pyfingerprint import PyFingerprint
import datetime
import tempfile
import hashlib
import time
from tkinter import *
from tkinter import messagebox


client = MongoClient("mongodb://fpDBuser:project2019@fingerprintproject-shard-00-00-2ee1v.mongodb."
                     "net:27017,fingerprintproject-shard-00-01-2ee1v.mongodb.net:27017,"
                     "fingerprintproject-shard-00-02-2ee1v.mongodb.net:27017/test?ssl=true&replicaSet="
                     "FingerprintProject-shard-0&authSource=admin&retryWrites=true")

mydb = client['fingerprint_project']
connect_to_collection = mydb['students']

def login():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    time.sleep(1)
    try:
        while ( f.readImage() == False ):
            pass
        f.convertImage(0x01)
        result = f.searchTemplate() ## Searchs template
        positionNumber = result[0]
        accuracyScore = result[1]
        temp = positionNumber
        if ( positionNumber == -1 ):
            print('No match found! Try again')
            login()
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
        f.loadTemplate(positionNumber, 0x01)
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
    
    if ( positionNumber == -1 ):
        print('No match found! Try again')
        login()
    else:
        result= 10
        return(result)


#login()
def mongo_tests():
    #mydict = {"name": "Stephen"}
    for x in connect_to_collection.find():
        print(x)
    

#mongo_tests()
    