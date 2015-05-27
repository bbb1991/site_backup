#!/usr/bin/env python 
# -*- coding: utf-8 -*-

__author__ = 'bbb1991'


import mysql.connector
import os
import logging

"""
Класс для бэкапирования мускула

"""


class MysqlDownload:
    DESTINATION = ""
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                            level=logging.DEBUG, filename=u'mylog.log')

    @staticmethod
    def backup(host, user, password, db):
        """
        Функция для бэкапа бд
        :param host: ХОСТ
        :param user: ПОЛЬЗОВАТЕЛЬ
        :param password: ПАРОЛЬ
        :param db: БАЗА ДАННЫХ
        :return:
        """
        conn = mysql.connector.connect()    # получаем соединение
        try:
            logging.info("Пытаемся соедениться с сервером...")
            #  попытка соединения
            conn = mysql.connector.connect(host=host,
                                           database=db,
                                           user=user,
                                           password=password)
            if conn.is_connected():
                logging.info("Соединение установлена")

            # попытка бэкапирования
            try:
                logging.info("Попытка бэкапирования базы данных...")
                db = conn.database
                command = "mysqldump -u " + user + " -h " + host + " -p" + password + \
                          " " + db + " > " + MysqlDownload.DESTINATION + "/" + db + ".sql"
                os.system(command)

            except Exception as e:
                logging.error("Ошибка бэкапирования базы " + db + "!")
                logging.error(e)
                conn.close()
                raise Exception("Ошибка : " + str(e))
            else:
                logging.info("%s.sql успешна загружена!" % db)

        except Exception as e:
            logging.error(e)
            raise Exception(e)

        finally:
            conn.close()
            logging.info("Соединения закрыта")
