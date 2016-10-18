# -*- coding: utf8 -*-
# make a very long random secret key for
# session

import string
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--length', type=int, default=32,
                    help="the secret key's length")  # 默认32位长度
args = parser.parse_args()

LENGTH = args.length


def make_secret_key():
    key = ''.join(random.choice(string.hexdigits)
                  for x in xrange(LENGTH))
    print key
    return key


if __name__ == '__main__':
    make_secret_key()
