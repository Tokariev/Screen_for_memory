from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

import datetime


now = datetime.datetime.now()
DB_NAME = 'noprob01_boxbe'

cnx = mysql.connector.connect(host='noprob01.mysql.tools',database=DB_NAME,user='noprob01_boxbe',password='vdq2h5s7')
cursor = cnx.cursor()



add_album = ("INSERT INTO chv_albums "
               "(album_name, album_user_id, album_date) "
               "VALUES (%s, %s, %s)")


a = "%d.%02d.%d" % (now.year, now.month, now.day)
b = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

data_employee = (a, 1, b)

# Insert new employee
cursor.execute(add_album, data_employee)


# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()