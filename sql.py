#!/usr/bin/env python3
from abc import ABC, abstractmethod
import traceback


class SQL(ABC):

    @property
    def conn(self):
        raise NotImplementedError

    @property
    def cur(self):
        raise NotImplementedError

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def Connect(self):
        pass

    @abstractmethod
    def _IsConnected(self, r: bool) -> bool:
        pass

    def _ErrorHandler(self, e: Exception):
        traceback.print_exc()
        exit(1)

    def IsConnected(self) -> bool:
        """Checks if connection is still active

        :returns: Connection still active: <bool>
        """
        return self._IsConnected(repeated=True)

    def Query(self, query: str) -> list or None:
        """Sends a query to database.

        "SELECT" statements gets data returned as a list.
        "INSERT" statements automatically commits the changes.

        :param query: SQL query to execute <str>.
        :returns: list or None based on the type of query.
        """
        if "select" in query.lower():
            fetch = True
        else: fetch = False

        response = None
        cur = self.conn.cursor()

        try: cur.execute(query)

        except Exception as e:
            self._ErrorHandler(e)

        if fetch: return cur.fetchall()
        self.conn.commit()

    def PrettyPrint(self, query: str):
        """Queries the database and prints each row on a new line.

        :param query: SQL query to execute <str>.
        """
        try:
            for i in self.Query(query):
                print(i)
        except Exception as e:
            self._ErrorHandler(e)


