import pyscreenshot as ImageGrab
import mysql.connector
from mysql.connector import errorcode, Error
from datetime import date, datetime, timedelta
from tkinter import *

DB_NAME = 'noprob01_image'

conn = mysql.connector.connect(user='noprob01_image', password='fcmvu825',
                              host='noprob01.mysql.tools',
                              database=DB_NAME)
cursor = conn.cursor()

# Die folgende Funktion soll ausgeführt werden, wenn
# der Benutzer den Button Klick me anklickt
def button_action():
    entry_email = eingabefeld_email.get()
    entry_password = eingabefeld_password.get()
    if (entry_email == "") or (entry_password == ""):
        welcome_label.config(text="Gib zuerst einen Namen ein.")
    else:

        add_user = ("INSERT INTO user "
                      "(email, password) "
                      "VALUES (%s, %s)")

        data_user = (entry_email, entry_password)

        cursor.execute(add_user, data_user)

        entry_text = "Welcome " + entry_email + "!"
        welcome_label.config(text=entry_text)

fenster = Tk()
fenster.title("Please log in.")

# Anweisungs-Label
email_label = Label(fenster, text="eMail: ")
password_label = Label(fenster, text="Password: ")
# In diesem Label wird nach dem Klick auf den Button der Benutzer
# mit seinem eingegebenen Namen begrüsst.
welcome_label = Label(fenster)


# Hier kann der Benutzer eine Eingabe machen
eingabefeld_email = Entry(fenster, bd=2, width=40)
eingabefeld_password = Entry(fenster, bd=2, width=40)

login_button = Button(fenster, text="Login", command=button_action)
exit_button = Button(fenster, text="Beenden", command=fenster.quit)


# Nun fügen wir die Komponenten unserem Fenster hinzu
email_label.grid(row = 0, column = 1, pady = 10, padx=10)
eingabefeld_email.grid(row = 0, column = 2, pady = 10, padx=10)

password_label.grid(row = 1, column = 1)
eingabefeld_password.grid(row = 1, column = 2)

login_button.grid(row = 2, column = 2, pady = 10)

mainloop()


im = ImageGrab.grab(childprocess=False)
im.save('img.png')





TABLES = {}
TABLES['users'] = (
    "CREATE TABLE `users` ("
    "  `user_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`user_no`)"
    ") ENGINE=InnoDB")

TABLES['screens'] = (
    "CREATE TABLE `screens` ("
    "  `screen_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `caption` VARCHAR(45) NOT NULL,"
    "  `img` LONGBLOB NOT NULL,"
    "  `make_date` date NOT NULL,"
    "  PRIMARY KEY (`screen_no`)"
    ") ENGINE=InnoDB")

TABLES['user'] = (
    "CREATE TABLE `user` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `email` VARCHAR(45) NOT NULL,"
    "  `password` VARCHAR(20) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    conn.database = DB_NAME
    print('Connected to DB = ' + DB_NAME)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        conn.database = DB_NAME
    else:
        print(err)
        exit(1)

for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

tomorrow = datetime.now().date() + timedelta(days=1)

add_employee = ("INSERT INTO users "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")

add_screen = ("INSERT INTO screens "
               "(caption, img, make_date) "
               "VALUES (%s, %s, %s)")

data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

filename = "img.jpg"

def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
        print("Foto OK")
    return photo

screen_data = read_file(filename)

data_img = ('First image', screen_data, tomorrow)

# Insert new employee
cursor.execute(add_employee, data_employee)
cursor.execute(add_screen, data_img)


def read_blob(filename):
    # select photo column of a specific author
    query = "SELECT img FROM screens WHERE screen_no = 8"

    try:
        # query blob data form the authors table
        cursor.execute(query)
        photo = cursor.fetchone()[0]

        # write blob data into a file
        with open(filename, 'wb') as f:
            f.write(photo)
            print("Foto saved")

    except Error as e:
        print(e)

#read_blob('picture_out.png')

emp_no = cursor.lastrowid

# Make sure data is committed to the database
conn.commit()

cursor.close()
conn.close()
