import insert



connection = insert.getConnection()
cursor = connection.cursor()

sql = ("INSERT INTO chv_images(image_name) VALUES ('image_from_python2')")

cursor.execute(sql)

connection.commit()
connection.close()