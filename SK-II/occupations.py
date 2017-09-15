#!/usr/bin/python

"""
Khyber Sen, Shannon Lau
SoftDev1 pd7
HW3 -- StI/O: Divine your Destiny!
2017-09-13
"""

from __future__ import print_function

import random

from collections import Counter

__authors__ = ['Khyber Sen', 'Shannon Lau']
__date__ = '2017-09-14'


def _percentages(self):
    # type: () -> dict[any, float]
    length = float(sum(count for count in self.viewvalues()))
    return {value: self[value] / length for value in self}


Counter.percentages = _percentages


class Occupations(object):
    """
    :cvar DEFAULT_SAMPLE_SIZE: int
    :cvar UNITED_STATES_FILE: str

    :ivar occupations: list[tuple[str, float]]
    :ivar total_percent: float
    """

    DEFAULT_SAMPLE_SIZE = 1000000

    UNITED_STATES_FILE = 'occupations.csv'

    @staticmethod
    def parse_line(line):
        # type (str) -> tuple[str, float]
        occupation, percent = line.rsplit(',', 1)
        return occupation.strip('"'), float(percent)

    def __init__(self, file_name):
        # type: (str) -> Occupations
        self.occupations = [Occupations.parse_line(line) for line in
                            open(file_name).read().splitlines()[1:]]
        self.total_percent = sum(occupation[1] for occupation in self.occupations)

    def random_occupation(self):
        # type: () -> str
        random_percent = random.uniform(0, self.total_percent)  # type: float
        for occupation, percent in self.occupations:
            if random_percent < percent:
                return occupation
            random_percent -= percent

    def random_occupations(self, num_occupations):
        # type: (int) -> Counter
        return Counter(self.random_occupation() for i in xrange(num_occupations))

    def is_randomly_weighted(self, sample_size=DEFAULT_SAMPLE_SIZE, debug=False):
        # type: (int, bool) -> bool
        count = self.random_occupations(sample_size)
        delta = 0  # type: float
        percents = count.percentages()  # type: dict[str, float]
        for occupation, percent in self.occupations:
            delta += abs(percent - percents.get(occupation, 0) * self.total_percent)
        if debug:
            print('\n'.join('{}: {} vs. {}'.format(occupation, percent,
                                                   percents[occupation] * self.total_percent)
                            for occupation, percent in self.occupations))
        estimate = 867.238 / sample_size ** (0.561231 * .95)
        accepted = 2 * estimate
        print('sample size: {:<8}: delta: {} < {}'.format(sample_size, delta, accepted))
        return delta < accepted

    @staticmethod
    def in_united_states():
        # type: () -> Occupations
        return Occupations(Occupations.UNITED_STATES_FILE)

    @staticmethod
    def test(sample_size=DEFAULT_SAMPLE_SIZE, debug=True):
        # type: (int, bool) -> None
        error_msg = 'random weighted selection of occupations found in {}' \
                    ' is not working for a sample size of {}' \
            .format(Occupations.UNITED_STATES_FILE, sample_size)
        assert Occupations.in_united_states().is_randomly_weighted(sample_size, debug), error_msg


def test(sample_size=Occupations.DEFAULT_SAMPLE_SIZE, debug=True):
    # type: (int, bool) -> None
    Occupations.test(sample_size, debug)


if __name__ == '__main__':
    million = True
    while True:
        for i in xrange(2, (6 if million else 5) + 1):
            test(debug=False, sample_size=10 ** i)
        print()
