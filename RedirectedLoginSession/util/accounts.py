from __future__ import print_function

import sqlite3

from enum import Enum
from passlib.hash import pbkdf2_sha256


class Account(object):
    """

    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return '(username={}, password={})'.format(self.username, self.password)

    def __repr__(self):
        return str(self)


class AccountState(Enum):
    CORRECT = 0  # type: AccountState
    WRONG_USERNAME = 1  # type: AccountState
    WRONG_PASSWORD = 2  # type: AccountState


class Accounts(object):
    """

    """

    def __init__(self, path):
        self.path = path
        self._db = sqlite3.connect(path)
        self._cursor = self._db.cursor()
        self._create_table()

    def _create_table(self):
        print('creating accounts table')
        self._cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
          (username TEXT PRIMARY KEY, password TEXT)''')

    def check(self, account):
        # type: (Account) -> AccountState
        self._cursor.execute('SELECT * FROM accounts WHERE username = ?',
                             (account.username,))
        selected = self._cursor.fetchall()
        if len(selected) == 0:
            return AccountState.WRONG_USERNAME
        if pbkdf2_sha256.verify(account.password, selected[0][1]):
            return AccountState.WRONG_PASSWORD
        return AccountState.CORRECT

    def __contains__(self, account):
        # type: (Account) -> bool
        return self.check(account) == AccountState.CORRECT

    def add(self, account):
        # type: (Account) -> bool
        error = self.check(account)
        if error != AccountState.WRONG_USERNAME:
            return False
        self._cursor.execute('INSERT INTO accounts VALUES (?, ?)',
                             (account.username, pbkdf2_sha256.hash(account.password)))
        return True

    def __iadd__(self, account):
        self.add(account)
        return self

    def all_accounts(self):
        for username, password in self._cursor.execute('SELECT * FROM accounts'):
            yield Account(username, password)

    def commit(self):
        self._db.commit()

    def close(self):
        self.commit()
        self._db.close()


accounts = Accounts('../data/accounts.db')

if __name__ == '__main__':

    print(pbkdf2_sha256.hash('hello'))

    print(accounts.add(Account('hello', 'world')))
    # for i in xrange(100):
    #     for j in xrange(100):
    #         print(i, j)
    #         accounts.add(Account(str(i), str(j)))
    map(print, accounts.all_accounts())

    print(Account('hello', 'world') in accounts)

    print(type(Account))

    accounts.close()
