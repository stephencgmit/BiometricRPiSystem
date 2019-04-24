import pymongo
from pymongo import MongoClient
from pyfingerprint.pyfingerprint import PyFingerprint
import datetime
import tempfile
import hashlib
import time

client = MongoClient("mongodb://fpDBuser:project2019@fingerprintproject-shard-00-00-2ee1v.mongodb."
                     "net:27017,fingerprintproject-shard-00-01-2ee1v.mongodb.net:27017,"
                     "fingerprintproject-shard-00-02-2ee1v.mongodb.net:27017/test?ssl=true&replicaSet="
                     "FingerprintProject-shard-0&authSource=admin&retryWrites=true")

mydb = client['fingerprint_project']
coll = mydb['students']

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
            time.sleep(0.5)
            #login()
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            #return 0
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
    
    if ( positionNumber == -1 ):
        print('No match found! Try again')
        time.sleep(0.5)
        login()
    else:
        result= 10
        return(result)

def reg(username):
    uname = username

    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        register()
        exit(1)

    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    while ( f.readImage() == False ):
        pass

        ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)
        ## Checks if finger is already enrolled
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        exit(0)

    print('Remove finger...')
    time.sleep(0.1)


        ## Wait that finger is read again
    while ( f.readImage() == False ):
        pass

        ## Converts read image to characteristics and stores it in charbuffer 2
    f.convertImage(0x02)
        ## Compares the charbuffers
    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')
        ## Creates a template
    #temp = f.createTemplate()
    ## Creates a template
    f.createTemplate()

    ## Saves template at new position number
    positionNumber = f.storeTemplate()
    temp=[]
    temp=f.downloadCharacteristics(0x01)
    x = []
    x = coll.find_one(sort=[("uid", -1)])
    print(x)
    if x is None:
        new_user = {}
        new_user["uid"] = 0
        new_user["image_template"] = temp
        new_user["username"] = uname
        #new_user = {"uid": next_user, "image_template": last_template, "user_name": uname}
        coll.insert_one(new_user)
    else:
        last_user = x['uid']
        print("last user" + str(last_user))
        next_user = last_user + 1
        new_user = {}
        new_user["uid"] = next_user
        new_user["image_template"] = temp
        new_user["username"] = uname
        #new_user = {"uid": next_user, "image_template": last_template, "user_name": uname}
        coll.insert_one(new_user)
        
    return 1

def mongo_tests():
    #mydict = {"name": "Stephen"}
    for x in connect_to_collection.find():
        print(x)
    

#mongo_tests()
#login() 