#coding=utf-8

import MySQLdb

def getDBConnect():
        conn = MySQLdb.Connect(
                                                                host = 'localhost',
                                                                port = 3306,
                                                                user = 'root',
                                                                passwd = 'root',
                                                                db = 'codeclone',
                                                                charset = 'utf8'
                                                           )
        conn.autocommit(False)
        return conn
