#!/usr/bin/python

"""
Khyber Sen
SoftDev1 pd7
HW2 -- NO-body expects the Spanish Inquisition!
2017-09-13
"""

from __future__ import print_function

import random

__author__ = 'Khyber Sen'
__date__ = '2017-09-13'

# type: dict[int, list[str]]
CLASSES = {
    7: ['Helen', 'Shakil', 'Eric', 'Jennifer Y', 'Jennifer Z', 'Arif', 'Queenie', 'Jawadul',
        'Shaina', 'Vivien', 'Brian', 'Naotaka', 'Bayan', 'Adam', 'Caleb', 'Terry', 'Jason',
        'Alessandro', 'Samantha', 'Carol', 'Joyce', 'Shannon', 'Charles', 'Taylor', 'Kelly', 'Leo',
        'Khyber', 'Ibnul', 'Eugene', 'Yuyang', 'Karina', 'Tiffany', 'Holden', 'Michael'],
    8: ['Masha', 'Adrian', 'David', 'Eric', 'Josh', 'Jerome', 'Henry', 'Jackie', 'Giorgio', 'Karen',
        'Sonal', 'Xavier', 'Bermet', 'Alex', 'Iris', 'Manahal', 'Donia', 'Md', 'Connie', 'Lisa',
        'Xing', 'Angelica', 'Angel', 'Augie', 'Dimitriy', 'Yiduo', 'Gordon', 'Tiffany', 'Clive',
        'Jonathan', 'Sasha', 'Daniel'],
    9: ['Yu Qi', 'Michela', 'Kristin', 'Fabiha', 'Maxim', 'Marcus', 'Ish', 'James', 'Ryan',
        'Edward', 'Adeeb', 'Jake', 'Cynthia', 'Kevin', 'Levi', 'Edmond', 'Kyle', 'Andrew', 'Max',
        'Jenny', 'Philip', 'Shan', 'Mansour', 'Ray', 'Jake', 'Ida', 'Kerry', 'Stanley', 'Jackie',
        'William', 'Tina', 'Michael']
}


def random_student(class_period):
    # type: (int) -> str
    if class_period not in CLASSES:
        raise ValueError('{} is not a valid class period'.format(class_period))
    return random.choice(CLASSES[class_period])


def print_random_student(class_period):
    # type: (int) -> None
    try:
        result = random_student(class_period)
    except ValueError as e:
        result = 'successfully caught the ValueError "{}"'.format(e)
    print('Pd. {}: {}'.format(class_period, result))


def test():
    # type: (None) -> None
    print('\nTest:')
    for class_period in CLASSES:
        print_random_student(class_period)
    print_random_student(1)
    print()


def main():
    # type: (None) -> None
    exit_cmd = 'exit'  # type: str
    periods = ', '.join(str(period) for period in CLASSES)  # type: str
    message = 'Choose a period ({}) or type "{}" to exit\n'.format(periods, exit_cmd)  # type: str
    while True:
        while True:
            user_input = raw_input(message)  # type: str
            if user_input == exit_cmd:
                return
            try:
                period = int(user_input)  # type: int
                break
            except ValueError:
                pass
        print_random_student(period)
        print()


if __name__ == '__main__':
    print('randomizer.py')
    test()
    main()
