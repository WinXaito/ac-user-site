from time import time
from os import path as ospath
import string
import random


def uniqid():
    return hex(int(time() * 10000000))[2:]


def token_generator(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def basename(path):
    return ospath.splitext(ospath.basename(path))[0]


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False