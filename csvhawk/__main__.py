#!/usr/bin/env python
# csvhawk - Copyright (C) 2017, Walter Doekes, OSSO B.V.
#
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#
from collections import OrderedDict
import argparse
import csv
import re
import sys


def read_stdin():
    for line in sys.stdin:
        if not line:  # stop at first EOF-sign
            break
        yield line


def csv_transform(file_, transformations):
    reader = csv.reader(file_)
    keys = next(reader)  # read next line so header will be accessed
    for row in reader:
        for transform in transformations:
            keys, row = transform(keys, row)
        yield row


class TransNormalizer(object):
    regex = re.compile(r'\s+')

    def __call__(self, keys, row):
        row = [self.regex.sub(' ', column).strip() for column in row]
        return keys, row


class TransDeleter(object):
    regex = re.compile(r'\s+')

    def __init__(self, keys_to_delete):
        self.keys_to_delete = set(keys_to_delete)


    def __call__(self, keys, row):
        # This must be cached, it is only run once.
        try:
            # Attribute lookup is supposed to be snappy.
            self._key_nums
        except AttributeError:
            self._key_nums = [
                i for i, key in enumerate(keys) if key in self.keys_to_delete]
            self._key_nums.sort(reverse=True)  # rev, to keep the order
            for key_num in self._key_nums:
                keys.pop(key_num)  # could deepcopy keys first..

        # Operate on only row now.
        for key_num in self._key_nums:
            row.pop(key_num)

        return keys, row


class TransToCsv(object):
    def __call__(self, keys, row):
        try:
            # Attribute lookup is supposed to be snappy.
            self._did_first_call
        except AttributeError:
            self._did_first_call = True
            header = (
                ','.join('"{}"'.format(key.replace('"', '""')) for key in keys) +
                '\n')
            value = (
                ','.join('"{}"'.format(col.replace('"', '""')) for col in row))
            return keys, header + value

        value = (
            ','.join('"{}"'.format(col.replace('"', '""')) for col in row))
        return keys, value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CSV stream editor.')
    parser.add_argument(
        '-w', '--normalize', action='store_true',
        help='normalize whitepace: remove non-SP and collapse spaces')
    parser.add_argument(
        '-d', '--delete', metavar='N', action='append',
        help='delete column N (by name)')
    parser.add_argument(
        'file', nargs='?', metavar='FILE', help='the file to process')
    options = parser.parse_args()

    if options.file:
        file_ = open(options.file)
    else:
        file_ = None

    transformations = []
    if options.normalize:
        transformations.append(TransNormalizer())
    if options.delete:
        transformations.append(TransDeleter(options.delete))
    transformations.append(TransToCsv())

    try:
        csv_data = csv_transform(file_ or read_stdin(), transformations)
        for row in csv_data:
            print(row)

    finally:
        if file_:
            file_.close()
