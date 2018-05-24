from encodings.punycode import selective_find

import pyscreenshot as ImageGrab
import mysql.connector
from mysql.connector import errorcode, Error
from datetime import date, datetime, timedelta
from tkinter import *
import datetime
import socket
now = datetime.datetime.now()


album_name = "%d.%02d.%d" % (now.year, now.month, now.day)
album_user_id = 1
album_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
album_date_gmt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
album_creation_ip = socket.gethostbyname(socket.gethostname())
album_image_count = 1


print( type(album_name) )
print( type(album_user_id) )
print( type(album_date) )
print( type(album_date_gmt) )
print( type(album_creation_ip) )
print( type(album_image_count) )
