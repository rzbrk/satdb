import mysql.connector
from datetime import datetime

NULL = "NULL"

#------------------------------------------------------------------------------
# Class for database connection instance and functions
class Dbase:
    def __init__(self, configdata):
        self.config = configdata

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.config.host, port=self.config.port, user=self.config.user, password=self.config.password, database=self.config.database)
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            exit()

        self.cursor = self.connection.cursor()

    def fetchone(self, sql, arguments=None):
        self.cursor.execute(sql, arguments)
        data = self.cursor.fetchone()
        self.connection.commit()
        return data

    def fetchall(self, sql, arguments=None):
        self.cursor.execute(sql, arguments)
        data = self.cursor.fetchall()
        self.connection.commit()
        return data

    def write(self, sql, arguments=None):
        self.cursor.execute(sql, arguments)
        self.connection.commit()

    def disconnect(self):
        self.connection.close()

