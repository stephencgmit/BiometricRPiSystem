#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""
import sqlite3
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from tkinter import *
from tkinter import messagebox


global idnum
idnum = 0
#top = Tk()
## Enrolls new finger
##
conn = sqlite3.connect('student.db')
c = conn.cursor()

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

    ## Tries to enroll new finger
    try:
        msg=messagebox.showinfo("Enroll", "Press OK when Finger Ready")
        print('Waiting for finger...')

        ## Wait that finger is read
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
        time.sleep(1)

        msg=messagebox.showinfo("Enroll", "Press OK when Finger Ready")
        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')
            run()

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        #print(positionNumber)
        idnum = positionNumber
        
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        idnum = positionNumber
        #template = result[0]
        firstname = input("Enter your first name: ")
        lastname = input("Enter your last name: ")
        c.execute("INSERT INTO students VALUES(?, ?, ?, ?, ?, ?);", (idnum, firstname, lastname, 'NULL', 'NULL', 'NULL'))
        conn.commit()
        #conn.close()
        f = open("idtemplate.txt", "w")
        f.write(str(idnum))
        f.close
        #exit(1)

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

#run()
#top.mainloop()