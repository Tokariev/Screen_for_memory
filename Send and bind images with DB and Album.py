from PIL import Image
import os, sys
import pyscreenshot as ImageGrab
import ftplib
import datetime
import mysql.connector
import socket
import time
import myconnutils



now = datetime.datetime.now()

def is_album(album_name, album_user_id):
    db_conn = myconnutils.getConnection()
    cursor = db_conn.cursor()

    select_album_name = "SELECT album_name FROM chv_albums WHERE album_user_id ='" + str(album_user_id) + "' AND album_name ='" + album_name + "'"

    cursor.execute(select_album_name)
    selected_album = cursor.fetchone()

    # Make sure data is committed to the database
    cursor.close()
    cnx.close()

    if selected_album == None:
        return False
    else:
        return True

def get_album_id(album_name):
    db_conn = myconnutils.getConnection()
    cursor = db_conn.cursor()

    select_album_id = "SELECT album_id FROM chv_albums WHERE album_name ='" + album_name + "'"

    cursor.execute(select_album_id)
    album_id = cursor.fetchone()[0]

    cursor.close()
    cnx.close()

    return album_id

def add_album_to_sql(album_name, user_id):
    db_conn = myconnutils.getConnection()
    cursor = db_conn.cursor()

    insert_into_album = ("INSERT INTO chv_albums "
                         "(album_name, album_user_id, album_date, album_date_gmt, album_creation_ip, album_image_count) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")

    #album_name = "%d.%02d.%d" % (now.year, now.month, now.day)
    album_user_id = user_id
    album_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    album_date_gmt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    album_creation_ip = socket.gethostbyname(socket.gethostname())
    album_image_count = 0

    data_album = (album_name, album_user_id, album_date, album_date_gmt, album_creation_ip, album_image_count)

    # Insert into chv_albums
    cursor.execute(insert_into_album, data_album)
    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()


def add_img_to_sql(imGrab, image_name, user_id, album_id):

    image_extension = image_name.split(".")[-1]
    image_size = os.stat(image_name).st_size
    image_width, image_height = imGrab.size
    image_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_date_gmt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    image_title = datetime.datetime.now().strftime("%H:%M:%S")
    image_user_id = user_id
    image_album_id = album_id
    image_uploader_ip = socket.gethostbyname(socket.gethostname())
    image_original_filename = image_name
    image_medium_size = os.stat(image_name.split(".")[0] + '.md.jpg').st_size

    cnx = mysql.connector.connect(host='noprob01.mysql.tools', database=DB_NAME, user='noprob01_img',
                                  password='xbjz49r8')
    cursor = cnx.cursor()

    insert_into_images = ("INSERT INTO chv_images(image_name, image_extension, image_size, image_width, image_height, image_date, image_date_gmt, image_title, image_user_id, image_album_id, image_uploader_ip, image_original_filename, image_medium_size) "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    data_img = (image_name.split(".")[0], image_extension, image_size, image_width, image_height, image_date, image_date_gmt, image_title, image_user_id, image_album_id, image_uploader_ip, image_original_filename, image_medium_size)

    cursor.execute(insert_into_images, data_img)

    cnx.commit()
    cursor.close()
    cnx.close()

def get_id(email):
    cnx = mysql.connector.connect(host='noprob01.mysql.tools', database=DB_NAME, user='noprob01_img',
                                  password='xbjz49r8')
    cursor = cnx.cursor()

    select_id = "SELECT user_id FROM chv_users WHERE user_email ='" + email + "'"

    cursor.execute(select_id)
    user_id = cursor.fetchone()[0]

    cursor.close()
    cnx.close()
    return user_id

def make_screen():
    im = ImageGrab.grab(childprocess=False)
    im_medium = ImageGrab.grab(childprocess=False)
    user_id = get_id("sumytoxa@ukr.net")
    img_name = str(user_id) + "_{:02d}_{:02d}".format(now.hour, now.minute)
    img_big_name = img_name + '.jpg'

    im.save(img_big_name)
    upload(img_big_name)

    album_name = datetime.datetime.now().strftime("%Y-%m-%d")

    if is_album(album_name, user_id):
        print("Album %s exist" % album_name )
    else:
        add_album_to_sql(album_name, user_id)

    album_id = get_album_id(album_name)



    try:
        size = 500, 333
        im_medium.thumbnail(size, Image.ANTIALIAS)
        img_medium_name = img_name + '.md.jpg'
        im_medium.save(img_medium_name)
        upload(img_medium_name)
    except IOError:
        print ("Cannot create small image")

    add_img_to_sql(im, img_big_name, user_id, album_id)

    os.remove(img_medium_name)
    os.remove(img_big_name)

    print("Added fotos to MySQL")

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


#make_screen()
#add_album_in_sql("sdsds", 1)

i = 1
while True:
    make_screen()
    print(i)
    time.sleep(30)  # Delay for 1 minute (60 seconds).
    i += 1
