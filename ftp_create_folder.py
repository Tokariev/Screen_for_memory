import ftplib
import datetime

now = datetime.datetime.now()

ftp = ftplib.FTP('noprob01.ftp.tools', 'noprob01_ftp', 'wzWKWr5e')

ftp.cwd("/noproblema.kiev.ua/www/images/")

def change_ftp_directory(ftp_conn, path):
    ftp_conn.cwd(path)
    return ftp_conn

def create_ftp_directory(ftp_conn, path):
    ftp_conn.mkd(path)


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





print(ftp.pwd())




