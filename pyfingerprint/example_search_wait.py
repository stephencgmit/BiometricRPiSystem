#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

import sqlite3
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from tkinter import *
from tkinter import messagebox

conn = sqlite3.connect('student.db')
c = conn.cursor()


## Search for a finger
##
def run():
## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to search the finger and calculate hash
    try:
        msg=messagebox.showinfo("Enroll", "Press OK when Finger Ready")

        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]
        temp = positionNumber
        if ( positionNumber == -1 ):
            print('No match found! Try again')
            run()
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            c.execute("SELECT firstname, lastname FROM students WHERE templateid = ?", str(temp) )
            result = c.fetchall()
            for row in result:
                fn = row[0]
                ln = row[1]
                print("Name = %s %s", fn, ln)
            #for row in c:
            #    print(row)
            #print(c)
            print("User logged in")

        ## OPTIONAL stuff
        ##

        ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        ## Hashes characteristics of template
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

#run()
