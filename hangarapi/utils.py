import time
import random


def get_date():
    sec_diff = random.randint(0, 1728000)
    return time.time() - sec_diff
