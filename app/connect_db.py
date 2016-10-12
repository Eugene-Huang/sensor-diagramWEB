# -*- coding: UTF-8 -*-

import MySQLdb

HOSTNAME = 'localhost'
USER = 'root'
PASSWORD = '123456'
DBNAME = 'smarthome'


class db():
    # connect database, create cursor

    def __init__(self):
        try:
            self.conn = MySQLdb.connect(HOSTNAME, USER, PASSWORD,
                                        DBNAME)
            self.conn.autocommit(True)  # 事务自动提交
        except MySQLdb.Error as e:
            raise e
        else:
            print 'Database connected successful...\n'
            self.cur = self.conn.cursor()

    # close database
    def close_db(self):
        try:
            self.conn.close()
        except MySQLdb.Error as e:
            raise e
        else:
            print 'Database closed\n'

    # execute sql
    def execute_db(self, sql):
        try:
            self.cur.execute(sql)
        except MySQLdb.Error as e:
            raise e

# 创建新的实例
db = db()
