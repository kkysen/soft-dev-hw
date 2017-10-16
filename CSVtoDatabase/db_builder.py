#!/usr/bin/python

"""
Khyber Sen
SoftDev1 pd7
HW9 -- No Treble
2017-10-15
"""

__author__ = 'Khyber Sen'
__date__ = '2017-10-15'

import os

from csv2db import Database

if __name__ == '__main__':
    with Database('test.db', debug=True) as db:
        db.add_csv('peeps.csv', types=('TEXT', 'INT', 'INT PRIMARY KEY'))

        db.add_csv('courses.csv', types=('TEXT', 'INT', 'INT'))

        dir_path = 'baseball/'
        for csv in os.listdir(dir_path):
            db.add_csv(dir_path + csv)
