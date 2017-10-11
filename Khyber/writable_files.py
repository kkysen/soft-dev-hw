from __future__ import print_function

from collections import Counter

def filter_me(fn):
    # type: (str) -> None
    s = ''.join(line.strip('.') for line in open(fn) if 'khyber' not in line and 'sen' not in line)
    with open(fn) as f:
        f.write(s)


def count_users(fn):
    # type: (str) -> Counter
    return Counter(line.split('/')[4] for line in open(fn) if '/home/students' in line)


def find_users(fn):
    # type: (str) -> list[str]
    return sorted(count_users(fn).viewkeys())


def print_user_counts(fn):
    # type: (str) -> None
    for user, n in sorted(count_users(fn).viewitems(), key=lambda x: x[1]):
        print('{}: {}'.format(user, n))


if __name__ == '__main__':
    print_user_counts('C:/Users/kkyse/Desktop/writable_files.txt')