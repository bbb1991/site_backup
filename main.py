#!/usr/bin/env python 
# -*- coding: utf-8 -*-

__author__ = 'bbb1991'

from time import strftime
from mysql import MysqlDownload
import ftp
import zip
from sys import exit
import os
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG, filename=u'mylog.log')

# КУДА будем складывать все. Создается папка с текущей даты. Пример: 20150522
TEMP = "/home/Lucifer/Temp/" + strftime("%Y%m%d")
BACKUP_DESTINATION = "/home/Lucifer/Backups/"
MAX_ARCHIVE = 4

# FTP
FTP_HOST = "666.666.666.666"    # ХОСТ куда подключаемся
FTP_USER = "Lucifer"       # ЛОГИН для подключения
FTP_PASSWORD = "HeLL1$C0M1nG"   # ПАРОЛЬ для подключения
FTP_SOURCE = ["/list/sinners", "/list/bieber_fans"]  # ОТКУДА будем скачивать
ftp.DESTINATION = TEMP
ftp_backup = ftp.FtpBackup()

# MySQL
DB_HOST = "616.616.616.616"    # Адрес хоста баз данных
DATABASES = ["db_all_list", "db_bieber_fans"]
DB_USER = "Devil"
DB_PASSWORD = "tHeD@yEnD$"
MysqlDownload.DESTINATION = TEMP
my_db = MysqlDownload()

# Zip
zip.SOURCE = TEMP
zip.DESTINATION = BACKUP_DESTINATION
compress = zip.Compress()

# Создаем временную папку
if not os.path.exists(TEMP):
    logging.info("Создаем временную папку...")
    os.makedirs(TEMP)

try:
    # MySQL backup
    # Поочередно бэкапируем базу данных
    for db in DATABASES:
        my_db.backup(DB_HOST, DB_USER, DB_PASSWORD, db)

    # FTP backup
    for s in FTP_SOURCE:
        ftp_connect = ftp_backup.connect(FTP_HOST, FTP_USER, FTP_PASSWORD)
        try:
            ftp_backup.download_files(s, ftp_connect)
        except Exception as e:
            logging.error(e)
            raise Exception(e)
        finally:
            logging.info("Закрытие соединения...")
            ftp_connect.quit()
    # Zipping
    compress.compress_dir()
    compress.send_to_server(os.path.abspath(TEMP+".zip"), BACKUP_DESTINATION)

    os.chdir(BACKUP_DESTINATION)
    if len([name for name in os.listdir('.') if os.path.isfile(name)]) >= MAX_ARCHIVE:
        logging.info("В бэкапном сервере обнаружена больше файлов, чем", MAX_ARCHIVE)
        onlyfiles = [f for f in os.listdir(BACKUP_DESTINATION) if os.path.isfile(os.path.join(BACKUP_DESTINATION, f))]
        onlyfiles.sort()
        os.remove(onlyfiles[0])
        logging.info(onlyfiles[0], " удалена.")

except Exception as e:
    logging.error(e)
    exit(e)
else:
    logging.info("Бэкапирование завершена, ошибок не обнаружено.")
