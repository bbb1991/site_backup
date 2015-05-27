#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import ftplib   # для работы с FTP
import logging  # для логирования
import os       # для работы в операционной среде

class FtpBackup:

    # Параметры логирования
    DESTINATION = ""
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                            level=logging.DEBUG, filename=u'mylog.log')


    @staticmethod
    def connect(host, login, password):

        # Создание соединения
        ftp = ftplib.FTP(host)

        # Пробуем подключиться
        try:
            logging.info("Пробуем подключиться...")
            ftp.login(login, password)
        except ftplib.error_perm as e:
            logging.error("Неправильный логин/пароль!")
            raise Exception("Не удалось подкючиться к FTP серверу! " + str(e))
        else:
            logging.info("Успешное подключение.")
        return ftp

    @staticmethod
    def download_files(path, ftp):
        """
        Главная функция, которая отвечает за загрузку
        :param path: текущая директория
        :return: None
        """
        file_list = ftp.nlst(path)  # получаем список файлов в текущем каталоге

        # Через цикл пробегаемся по списку
        for file in file_list:

            # пришлось писать индусский код, так как
            # функция os.path.isdir(file) почему-то
            # упорно возвращает False и при попытке скачать папку
            # как файл программа крашится
            try:
                ftp.cwd(file+"/")   # Пробуем переити по ссылке
                # Если перешли, значит папка, рекурсивно вызываем функцию и как аргумент
                # передаем ссылку
                FtpBackup.download_files(file, ftp)
            except ftplib.error_perm:   # Если выбросило исключение, значит файл
                local_dir = FtpBackup.DESTINATION + path    # создаем копию пути во временной директорий
                if not os.path.exists(local_dir):   # проверяем, создана ли она уже
                    os.makedirs(local_dir)
                    logging.info("%s built" % local_dir)

                os.chdir(local_dir)  # Переходим к текущей папке создаем файл и открываем для записи
                local_filename = os.path.join(local_dir, os.path.basename(file))
                local_file = open(local_filename, 'wb')
                ftp.retrbinary("RETR " + file, local_file.write)
                logging.info("%s downloaded." % file)
                local_file.close()

