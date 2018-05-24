import ftplib


session = ftplib.FTP('noprob01.ftp.tools','noprob01_ftp','wzWKWr5e')

session.cwd("/noproblema.kiev.ua/www")
session.mkd('mydir')
#1
file = open('img.jpg','rb')                     # file to send
session.storbinary('STOR kitten.jpg', file)     # send the file
file.close()                                    # close file and FTP

session.quit()


#2
filename = "img.jpg"
ftp = ftplib.FTP('noprob01.ftp.tools')
ftp.login("noprob01_ftp", "wzWKWr5e")
ftp.cwd("/noproblema.kiev.ua/www")

ftp.storbinary("STOR " + filename, open(filename, 'rb'))


