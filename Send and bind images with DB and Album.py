from PIL import Image
import os
import pyscreenshot as ImageGrab
import datetime
import socket
import myconnutils
import ftp_module

now = datetime.datetime.now()


def is_album(album_name, album_user_id):
    cursor = db_connection.cursor()
    select_album_name = "SELECT album_name FROM chv_albums WHERE album_user_id ='" + str(album_user_id) + "' AND album_name ='" + album_name + "'"
    cursor.execute(select_album_name)
    selected_album = cursor.fetchone()

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
    db_conn.close()
    return album_id

def add_album_to_sql(album_name, user_id):
    db_connection = myconnutils.getConnection()
    cursor = db_connection.cursor()
    insert_into_album = ("INSERT INTO chv_albums "
                         "(album_name, album_user_id, album_date, album_date_gmt, album_creation_ip) "
                         "VALUES (%s, %s, %s, %s, %s)")

    select_album_count = ("SELECT user_album_count FROM chv_users WHERE user_id = " + str(user_id))

    cursor.execute(select_album_count)
    album_count = cursor.fetchone()[0]

    print("Album_count = ", album_count)

    update_chv_user = ("UPDATE chv_users SET user_album_count = " + str(album_count + 1) +
                       " WHERE user_id = " + str(user_id))

    print(update_chv_user)

    album_user_id = user_id
    album_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    album_date_gmt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    album_creation_ip = socket.gethostbyname(socket.gethostname())
    #album_image_count = 0

    data_album = (album_name, album_user_id, album_date, album_date_gmt, album_creation_ip)


    # Insert into chv_albums
    cursor.execute(insert_into_album, data_album)

    cursor.execute(update_chv_user)
    # Make sure data is committed to the database
    db_connection.commit()

def add_img_to_sql(imGrab, image_name, user_id, album_id):

    image_extension = image_name.split(".")[-1]

    print("Image extension = " + image_extension)

    image_size = os.stat(image_name).st_size

    print("Image size = " + str(image_size))

    image_width, image_height = imGrab.size

    print("Image_width = " + str(image_width))

    image_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Image_date = " + str(image_date))

    image_date_gmt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    print("Image_date_gmt = " + str(image_date_gmt))

    image_title = datetime.datetime.now().strftime("%H:%M:%S")
    image_user_id = user_id
    image_album_id = album_id
    image_uploader_ip = socket.gethostbyname(socket.gethostname())
    image_original_filename = image_name
    image_medium_size = os.stat(image_name.split(".")[0] + '.md.jpg').st_size

    print("Image_medium_size = " + str(image_medium_size))

    #db_connection = myconnutils.getConnection()
    cursor = db_connection.cursor()

    insert_into_images = ("INSERT INTO chv_images(image_name, image_extension, image_size, image_width, image_height, image_date, image_date_gmt, image_title, image_user_id, image_album_id, image_uploader_ip, image_original_filename, image_medium_size) "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    data_img = (image_name.split(".")[0], image_extension, image_size, image_width, image_height, image_date, image_date_gmt, image_title, image_user_id, image_album_id, image_uploader_ip, image_original_filename, image_medium_size)

    cursor.execute(insert_into_images, data_img)

    select_album_image_count = ("SELECT album_image_count FROM chv_albums WHERE album_id = " + str(album_id))

    cursor.execute(select_album_image_count)
    album_image_count = cursor.fetchone()[0]

    print("Album_image_count = ", album_image_count)

    update_chv_albums = ("UPDATE chv_albums SET album_image_count = " + str(album_image_count + 1) +
                         " WHERE album_id = " + str(album_id))

    cursor.execute(update_chv_albums)

    select_image_count = ("SELECT user_image_count FROM chv_users WHERE user_id = " + str(user_id))
    cursor.execute(select_image_count)
    image_count = cursor.fetchone()[0]

    update_chv_albums = ("UPDATE chv_users SET user_image_count = " + str(image_count + 1) +
                         " WHERE user_id = " + str(user_id))
    cursor.execute(update_chv_albums)

    db_connection.commit()


def get_id(email):
    #db_conn = myconnutils.getConnection()
    cursor = db_connection.cursor()

    select_id = "SELECT user_id FROM chv_users WHERE user_email ='" + email + "'"

    cursor.execute(select_id)
    user_id = cursor.fetchone()[0]
    #db_conn.close()
    return user_id

def make_screen():
    im = ImageGrab.grab(childprocess=False)
    im_medium = ImageGrab.grab(childprocess=False)
    user_id = get_id("sumytoxa@ukr.net")

    print("User ID = " + str(user_id))

    img_name = str(user_id) + "_{:02d}_{:02d}".format(now.hour, now.minute)
    img_big_name = img_name + '.jpg'

    print(img_big_name)

    im.save(img_big_name)
    upload(img_big_name)

    album_name = datetime.datetime.now().strftime("%Y-%m-%d")

    if is_album(album_name, user_id):
        print("Album %s exist" % album_name )
    else:
        add_album_to_sql(album_name, user_id)
        print("Created new album %s " % album_name)

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
    ftp = ftp_module.getFtpConnection()

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

db_connection = myconnutils.getConnection()
make_screen()
db_connection.close()