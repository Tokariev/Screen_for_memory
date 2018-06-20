import mysql.connector
from mysql.connector import errorcode


DB_NAME = 'noprob01_testsit'

def getConnection():
    try:
        connection = mysql.connector.connect(host='noprob01.mysql.tools',
                                             user='noprob01_testsit',
                                             password='8gs6m7fv',
                                             database=DB_NAME)
        print("Connect was created.")
        cursor = connection.cursor()

        sql = ("INSERT INTO chv_images(image_name) VALUES ('image_from_python')")

        cursor.execute(sql)

        connection.commit()
        connection.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return connection

getConnection()