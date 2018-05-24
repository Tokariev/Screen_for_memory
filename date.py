import datetime
import time

now = datetime.datetime.now()





print ("Current year: %d.%02d.%d" % (now.year, now.month, now.day))

print ("Current date and time: " , datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))


a = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

#cursor.execute('INSERT INTO myTable (Date) VALUES(%s)', (a.strftime('%Y-%m-%d %H:%M:%S'),)

a = datetime.datetime.now()

print("%d.%02d.%d" % (now.year, now.month, now.day))