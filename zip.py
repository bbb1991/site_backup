#!/usr/bin/env python 
# -*- coding: utf-8 -*-

__author__ = 'bbb1991'

import os
import zipfile
import logging
from shutil import copyfile
from shutil import rmtree

SOURCE = ""
DESTINATION = ""

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG, filename=u'mylog.log')

# позволяет рекурсивно проитись по подпапкам
# класс был слит с ГитХаба у пользователя Daniel Dittmar
# спасибо что спас от очередного изобретения велосипеда
class RecursiveFileIterator:
    def __init__(self, *root_dirs):
        self.dirQueue = list(root_dirs)
        self.includeDirs = None
        self.fileQueue = []

    def __getitem__(self, index):
        while len(self.fileQueue) == 0:
            self.next_dir()
        result = self.fileQueue[0]
        del self.fileQueue[0]
        return result

    def next_dir(self):
        dir = self.dirQueue[0]   # fails with IndexError, which is fine
                                  # for iterator interface
        del self.dirQueue[0]
        list = os.listdir(dir)
        join = os.path.join
        isdir = os.path.isdir
        for basename in list:
            fullPath = join(dir, basename)
            if isdir(fullPath):
                self.dirQueue.append(fullPath)
                if self.includeDirs:
                    self.fileQueue.append(fullPath)
            else:
                self.fileQueue.append(fullPath)


class Compress:
    @staticmethod
    def compress_dir():
        """
        Функция для архивирования файлов
        Конечно, можно было бы написать что-то вроде:
        os.system(r'c:/"Program Files"/"winrar"/rar.exe a -r -ep1 -df '+name+' '+name+' ')
        но решил не делать этого, так как есть вероятность запуска данного скрипта в
        линуксовом сервере
        :return:
        """
        try:
            if not os.path.exists(SOURCE):
                raise FileNotFoundError(SOURCE, "Не найден!")

            logging.info("Создание архива %s.zip..." % os.path.abspath(SOURCE))
            file = zipfile.ZipFile(os.path.abspath(SOURCE)+".zip", "w")
            logging.info("Архив создан!")

            for name in RecursiveFileIterator(SOURCE):
                if os.path.isfile(name):
                    file.write(name, name, zipfile.ZIP_DEFLATED)
                    logging.info("Добавление в архив: %s" % name)

            file.close()

        except Exception as e:
            raise Exception(e)
        else:
            logging.info("Архивировние успешно завершена")

    def send_to_server(self, s_f, d):
        """
        Функция для отправки архив на бэкапный сервер
        :param s_f: файл, которую надо отправить
        :param d: КУДА отправляем
        :return:
        """
        try:
            os.chdir(d)
            copyfile(s_f, d + os.path.basename(s_f))

        except Exception as e:
            raise Exception(e)
        else:
            logging.info("Файл успешно отправлен на бэкапный сервер")

    def cleaning(self):
        rmtree(SOURCE)
        os.remove(SOURCE+".zip")
        logging.info("Временная папка очищена")
