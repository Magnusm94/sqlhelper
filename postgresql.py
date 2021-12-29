#!/usr/bin/env python3
import os
import psycopg2
import traceback
try:
    from sql import SQL
except ImportError:
    from sqlhelper import SQL


__all__ = ["Postgresql"]

class Postgresql(SQL):
    """Creates a connection to Postgresql using the psycopg2 library.

    :method Connect:
    """
    conn = None
    cur  = None

    def __init__(self, database: str=os.getlogin(), user: str=os.getlogin(), password: str="", host: str="localhost", port: int=5432, *args: None, **kwargs: None):
        """Saves the login information in a private variable and starts connection workflow.

        :param database: Name of database <str>. Default = os.getlogin()
        :param user: Username <str>. Default = os.getlogin()
        :param password: Password for connection <str>. Default = "" | no password.
        :param host: IP or domain to connect to <str>. Default = "localhost".
        :param port: Port for connection <int>. Default = 5432
        """
        self.__login = dict(
            database    =   database,
            user        =   user,
            password    =   password,
            host        =   host,
            port        =   port
        )
        self.Connect()

    def Connect(self):
        """Attempts to connect to database."""
        try:
            self.conn = psycopg2.connect(**self.__login)
        except Exception as e:
            self._ErrorHandler(e)
        self._IsConnected(repeated=True)

    def _IsConnected(self, repeated=False):
        """Checks if connection is active, otherwise attempts to reconnect"""
        if self.conn.closed:
            if not repeated:
                self.Connect()
                return self.IsConnected(repeated=True)
            warn("Connection to postgresql is closed.")
        return not self.conn.closed

    def _ErrorHandler(self, e: Exception):
        """Meant for internal errorhandling

        :param e: <Exception>
        """
        traceback.print_exc()

        if isinstance(e, psycopg2.errors.UndefinedTable):
            raise ValueError("Invalid query.")


        elif isinstance(e, psycopg2.OperationalError):
            exit("psycopg2.OperationalError: Cannot connect to database.")

        else:
            print(type(e))
            exit(1)


    def ListTables(self) -> list:
        """Queries for available tables.

        :returns: <list> of all public tables. 
        """
        return [i[0] for i in self.Query("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
                AND table_type='BASE TABLE';""")]

    def DescribeTable(self, tablename: str) -> list:
        """Attempts to describe values in given table.

        :param tablename: <str> of tablename you want described.
        :returns: <list> of tuples with info of each column.
        """
        print(self.Query(f"""
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{tablename}';"""))


