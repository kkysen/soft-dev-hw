from __future__ import print_function

import csv
import os
import sqlite3
from collections import Iterable


class Database(object):
    """Database wrapper."""

    def __init__(self, path, debug=False):
        # type: (str) -> None
        self.path = path
        self._db = sqlite3.connect(path)
        self.cursor = self._db.cursor()
        self.debug = debug

    @staticmethod
    def sanitize(s):
        # type: (str) -> str
        return '"{}"'.format(s.replace("'", "''").replace('"', '""'))

    @staticmethod
    def desanitize(s):
        # type: (str) -> str
        return s.replace("''", "'").replace('""', '"').strip('"')

    def table_exists(self, table_name):
        # type: (str) -> bool
        query = 'SELECT COUNT(*) FROM sqlite_master WHERE type="table" AND name=?'
        return self.cursor.execute(query, [Database.desanitize(table_name)]).fetchone()[0] > 0

    def add_csv(self, path, table_name=None, types=None):
        # type: (str, Iterable[str] | None) -> str | None
        file_name = os.path.basename(path)
        if '.' in file_name:
            file_name, ext = file_name.rsplit('.', 1)
            if ext != 'csv':
                return None
        if table_name is None:
            table_name = file_name
        table_name = Database.sanitize(table_name)

        if self.table_exists(table_name):
            return table_name

        with open(path) as csv_file:
            fields = csv.DictReader(csv_file).fieldnames
            fields = [Database.sanitize(field) for field in fields]
            reader = csv.reader(csv_file)
            num_fields = len(fields)
            if types is None or len(types) != num_fields:
                types = ['BLOB' for i in xrange(num_fields)]
            create_table_query = 'CREATE TABLE {} ({})'.format(
                table_name,
                ', '.join(field + ' ' + type for field, type in zip(fields, types))
            )
            if self.debug:
                print(create_table_query)
            self.cursor.execute(create_table_query)
            insert_query = 'INSERT INTO {} VALUES ({})'.format(
                table_name,
                ', '.join('?' for i in xrange(num_fields))
            )
            self.cursor.executemany(insert_query, [row for row in reader])
        return table_name

    def commit(self):
        # type: () -> None
        self._db.commit()

    def hard_close(self):
        # type: () -> None
        self._db.close()

    def close(self):
        # type: () -> None
        self.commit()
        self.hard_close()

    def __enter__(self):
        # type: () -> Database
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # type: () -> None
        self.close()


if __name__ == '__main__':
    with Database('test.db') as db:
        db.add_csv('students.csv', types=('TEXT', 'INT', 'INT PRIMARY KEY'))
