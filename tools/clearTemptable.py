#!/usr/bin/env python
# -*- coding: utf8 -*-

import MySQLdb
import time


def clear_db(interval):
    try:
        connect = MySQLdb.connect(
            '115.159.190.88', 'zhifeng', 'zhifengmysql', 'smarthome')
        connect.autocommit(True)
    except MySQLdb.Error as e:
        raise e
    else:
        print 'Connected successful...'
        cur = connect.cursor()

    RUNSATRT = True
    sql = 'TRUNCATE recvmqtt'
    while RUNSATRT:
        try:
            try:
                cur.execute(sql)
                time.sleep(interval)
            except MySQLdb.Error as e:
                raise e
        except KeyboardInterrupt:
            print 'Closed:-( '
            break


if __name__ == '__main__':
    clear_db(60)
