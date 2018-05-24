import mysql.connector

DB_NAME = 'noprob01_img'
cnx = mysql.connector.connect(host='noprob01.mysql.tools',database=DB_NAME,user='noprob01_img',password='y9wf4j2v')
cursor = cnx.cursor()

email = "sumytoxa@ukr.net"

select_id = "SELECT user_id FROM chv_users WHERE user_email ='" + email + "'"

cursor.execute(select_id, email)
id = cursor.fetchone()[0]

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()

print(id)
