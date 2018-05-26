import pymysql.cursors

DB_NAME = 'noprob01_img'

def getConnection():
    connection = pymysql.connect(host='noprob01.mysql.tools',
                                 user='noprob01_img',
                                 password='xbjz49r8',
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection