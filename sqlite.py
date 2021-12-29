#!/usr/bin/env python
import sqlite3
try:
    from sql import SQL
except ImportError:
    from sqlhelper import SQL


class Sqlite(SQL):
    conn = None
    cur  = None

    def __init__(self, filename: str = ":memory:"):
        """

        :param filename: <str> of path to sqlite3 database. If none is given, defaults to RAM.
        """
        self.Connect(filename)

    def Connect(self, filename):
        try:
            self.conn = sqlite3.connect(filename)
            self.cur = self.conn.cursor()
        except Exception as e:
            self._ErrorHandler(e)

    def _IsConnected(self, repeated=False) -> bool:
        # TODO: Make this function work and document it.
        print(dir(self.cur))
        print(self.cur.description)

