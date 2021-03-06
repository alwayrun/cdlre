#!/usr/bin/env python3

"""
Converts the union of several unicode categories to a single bitmask encoded as
a JS string.
"""

import collections
import os
from subprocess import Popen

TARGET_CATEGORIES = ['Mn', 'Mc', 'Nd', 'Pc', 'Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl']

# Each index in the bitmap corresponds to a uint16,
# because that's the best we can encode in a unicode character.
bitmap = collections.defaultdict(int)
with open(os.path.join('metadata', 'unicode_categories.txt')) as file:
    for line in file:
        hexcode, category, *rest = line.split()
        if category not in TARGET_CATEGORIES:
            continue
        dec = int(hexcode, 16)
        index, bit = divmod(dec, 16)
        assert bitmap[index] & (1 << bit) == 0
        bitmap[index] = 1 << bit

print('"', end='')
for i in range(max(bitmap.keys()) + 1):
    item = bitmap[i]
    assert item & 0xffff == item
    print(r'\u%04x' % item, end='')
print('"')
