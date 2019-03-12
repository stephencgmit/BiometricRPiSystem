import pymongo
from pymongo import MongoClient
from pyfingerprint.pyfingerprint import PyFingerprint
import datetime
import tempfile
import hashlib
import example_search_wait, example_enroll_wait
import time
from tkinter import *
from tkinter import messagebox

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
        if( positionNumber == -1 ):
            print('No match found! Try again')
            login()
        else:
            result=1
            return (result)
    
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
    

login()