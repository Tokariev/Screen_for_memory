import mysql.connector
from mysql.connector import errorcode


DB_NAME = 'noprob01_screen'

def getConnection():
    try:
        connection = mysql.connector.connect(host='noprob01.mysql.tools',
                                             user='noprob01_screen',
                                             password='tcdsbdhf',
                                             database=DB_NAME)
        print("Connect was created.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return connection

