#!/usr/bin/env python

__all__ = ["SQL", "Sqlite", "Postgresql"]


if __name__ == "__main__":
    from sql import SQL
    from sqlite import Sqlite
    from postgresql import Postgresql

else:
    from sqlhelper.sql import SQL
    from sqlhelper.sqlite import Sqlite
    from sqlhelper.postgresql import Postgresql


