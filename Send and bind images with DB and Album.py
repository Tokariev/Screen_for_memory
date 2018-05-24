from PIL import Image
import os, sys
import pyscreenshot as ImageGrab
import ftplib
import datetime
import mysql.connector
import socket

DB_NAME = 'noprob01_img'
now = datetime.datetime.now()

def is_album(album_name, album_user_id):
    cnx = mysql.connector.connect(host='noprob01.mysql.tools', database=DB_NAME, user='noprob01_img',
                                  password='y9wf4j2v')
    cursor = cnx.cursor()

    select_album_name = "SELECT album_name FROM chv_albums WHERE album_user_id ='" + str(album_user_id) + "' AND album_name ='" + album_name + "'"

    cursor.execute(select_album_name)
    selected_album = cursor.fetchone()

    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()

    if selected_album == None:
        return False
    else:
        return True

def add_record_in_sql_chv_albums(album_name, user_id):

    cnx = mysql.connector.connect(host='noprob01.mysql.tools', database=DB_NAME, user='noprob01_img',
                                  password='y9wf4j2v')
    cursor = cnx.cursor()
    insert_into_album = ("INSERT INTO chv_albums "
                         "(album_name, album_user_id, album_date, album_date_gmt, album_creation_ip, album_image_count) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")

    album_name = "%d.%02d.%d" % (now.year, now.month, now.day)
    album_user_id = user_id
    album_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    album_date_gmt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    album_creation_ip = socket.gethostbyname(socket.gethostname())
    album_image_count = 1

    data_album = (album_name, album_user_id, album_date, album_date_gmt, album_creation_ip, album_image_count)

    # Insert into chv_albums
    cursor.execute(insert_into_album, data_album)
    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()

def get_id(email):
    cnx = mysql.connector.connect(host='noprob01.mysql.tools', database=DB_NAME, user='noprob01_img',
                                  password='y9wf4j2v')
    cursor = cnx.cursor()

    select_id = "SELECT user_id FROM chv_users WHERE user_email ='" + email + "'"

    cursor.execute(select_id)
    user_id = cursor.fetchone()[0]

    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()
    return user_id

def make_screen():
    im = ImageGrab.grab(childprocess=False)
    user_id = get_id("sumytoxa@ukr.net")
    name = str(user_id) + "_{:02d}_{:02d}".format(now.hour, now.minute)
    im.save(name + '.jpeg')

    upload(name + '.jpeg')
    os.remove(name + '.jpeg')

    try:
        size = 500, 333
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(name + '.md.jpeg')

        upload(name + '.md.jpeg')
        os.remove(name + '.md.jpeg')


    except IOError:
        print ("Cannot create small image")

def change_ftp_directory(ftp_conn, path):
    ftp_conn.cwd(path)
    return ftp_conn

def create_ftp_directory(ftp_conn, path):
    ftp_conn.mkd(path)


def upload(filetoupload):
    ftp = ftplib.FTP('noprob01.ftp.tools', 'noprob01_ftp', 'wzWKWr5e')

    ftp.cwd("/noproblema.kiev.ua/www/images/")

    if str(now.year) in ftp.nlst():  # check if '2018' exist inside 'images'
        ftp = change_ftp_directory(ftp, str(now.year))
    else:
        create_ftp_directory(ftp, str(now.year))
        ftp = change_ftp_directory(ftp, str(now.year))
    if "%02d" % (now.month) in ftp.nlst():
        ftp = change_ftp_directory(ftp, "%02d" % now.month)
    else:
        create_ftp_directory(ftp, "%02d" % now.month)
        ftp = change_ftp_directory(ftp, "%02d" % now.month)
    if "%02d" % (now.day) in ftp.nlst():
        ftp = change_ftp_directory(ftp, "%02d" % (now.day))
    else:
        create_ftp_directory(ftp, "%02d" % now.day)
        ftp = change_ftp_directory(ftp, "%02d" % now.day)

    f = open(filetoupload,'rb')
    ftp.storbinary(('STOR '+filetoupload),f)
    f.close()
    ftp.quit()


make_screen()
#is_album("1234", 1)
