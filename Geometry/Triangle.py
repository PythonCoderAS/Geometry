from typing import Union


def find_measure(side1: int, side2: int) -> int:
    return 180 - (side1 + side2)


def find_inequality(side1: Union[int, float], side2: Union[int, float], side3: Union[int, float]):
    vals = [side1, side2, side3]
    vals.sort()
    s = ''
    for i in vals:
        s += '%s>' % i
    return s.rstrip('>')
