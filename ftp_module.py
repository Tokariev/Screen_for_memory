import ftplib


def getFtpConnection():
    ftp = ftplib.FTP('noprob01.ftp.tools', 'noprob01_ftp', 'wzWKWr5e')
    ftp.cwd("/testsiteua.site/www/images/")
    return ftp