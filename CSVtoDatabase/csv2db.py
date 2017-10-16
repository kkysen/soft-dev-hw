from __future__ import print_function

import csv
import os
import sqlite3
from collections import Iterable


class Database(object):
    """Database wrapper."""

    def __init__(self, path, debug=False):
        # type: (str) -> Database
        self.path = path
        self._db = sqlite3.connect(path)
        self._cursor = self._db.cursor()
        self.debug = debug

    @staticmethod
    def sanitize(s):
        # type: (str) -> str
        return '"{}"'.format(s.replace("'", "''").replace('"', '""'))

    def add_csv(self, path, table_name=None, types=None):
        # type: (str, Iterable[str] | None) -> bool
        file_name = os.path.basename(path)
        if '.' in file_name:
            file_name, ext = file_name.rsplit('.', 1)
            if ext != 'csv':
                return False
        if table_name is None:
            table_name = Database.sanitize(file_name)
        with open(path) as csv_file:
            fields = csv.DictReader(csv_file).fieldnames
            fields = [Database.sanitize(field) for field in fields]
            reader = csv.reader(csv_file)
            num_fields = len(fields)
            if types is None or len(types) != num_fields:
                types = ['BLOB' for i in xrange(num_fields)]
            create_table_query = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(
                table_name,
                ', '.join(field + ' ' + type for field, type in zip(fields, types))
            )
            if self.debug:
                print(create_table_query)
            self._cursor.execute(create_table_query)
            insert_query = 'INSERT INTO {} VALUES ({})'.format(
                table_name,
                ', '.join('?' for i in xrange(num_fields))
            )
            self._cursor.executemany(insert_query, [row for row in reader])
        return True

    def commit(self):
        self._db.commit()

    def hard_close(self):
        self._db.close()

    def close(self):
        self.commit()
        self.hard_close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


if __name__ == '__main__':
    with Database('test.db') as db:
        db.add_csv('peeps.csv', types=('TEXT', 'INT', 'INT PRIMARY KEY'))
