import mysql.connector

DB_NAME = 'noprob01_img'

def getConnection():
    connection = mysql.connector.connect(host='noprob01.mysql.tools',
                                 user='noprob01_img',
                                 password='xbjz49r8',
                                 database=DB_NAME)
    return connection