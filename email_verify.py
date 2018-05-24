from encodings.punycode import selective_find

import pyscreenshot as ImageGrab
import mysql.connector
from mysql.connector import errorcode, Error
from datetime import date, datetime, timedelta
from tkinter import *
import datetime
import socket

now = datetime.datetime.now()
DB_NAME = 'noprob01_boxbe'

def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='noprob01.mysql.tools',database=DB_NAME,user='noprob01_boxbe',password='vdq2h5s7')

        if conn.is_connected():
            print('Connected to MySQL database')

        ### Check eMail ###
        is_email(conn, "mlangust@gmail.com")
        create_album(conn, 3)

    except Error as e:
        print(e)

    finally:
        conn.close()
        print('Connected was closed')


def is_email(conn, email):
    cursor = conn.cursor()

    params = {'value': email}
    query = "SELECT user_email FROM chv_users WHERE user_email = %(value)s"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    if not rows:
        print("Nothing im DB")
        return False
    else:
        for row in rows:
            print(row)
        return True

def create_album(cnx, user_id):


    cursor = cnx.cursor()

    add_album = ("INSERT INTO chv_albums "
                 "(album_name, album_user_id, album_date, album_date_gmt, album_creation_ip, album_image_count) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")

    album_name = "%d.%02d.%d" % (now.year, now.month, now.day)
    album_user_id = user_id
    album_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    album_date_gmt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    album_creation_ip = socket.gethostbyname(socket.gethostname())
    album_image_count = 1

    data_album = (album_name, album_user_id, album_date, album_date_gmt, album_creation_ip, album_image_count)

    # Insert new employee
    cursor.execute(add_album, data_album)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

if __name__ == '__main__':
    connect()