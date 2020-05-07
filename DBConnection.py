import sys
from tkinter import messagebox
import pymysql
from pymysql import ProgrammingError


class DBConnection:
    def __init__(self):
        self._host_name = 'localhost'
        self._port = 3306
        self._user = 'root'
        self._password = 'root'
        self._db_name = 'vehicle_insurance'

        self._connection_object = pymysql.connect(host=self._host_name,
                                                  port=self._port,
                                                  user=self._user,
                                                  passwd=self._password,
                                                  db=self._db_name)
        self._cursor = self._connection_object.cursor()

    def get_connection_object(self):
        return self._connection_object

    def close_database(self):
        self._connection_object.commit()
        self._connection_object.close()