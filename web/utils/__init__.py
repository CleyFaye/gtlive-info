from random import random
from datetime import (datetime,
                      timezone)


def generate_random_tag(length):
    """Generate a random alphanumeric tag of specified length.

    Parameters
    ----------
    length : int
        The length of the tag, in characters


    Returns
    -------
    str
        An alphanumeric tag of specified length.


    Notes
    -----
    The generated tag will not use possibly ambiguous characters from this set:
     - '0' and '1'
     - 'i' and 'I'
     - 'l' and 'L'
     - 'o' and 'O'
    """
    characters_set = ('23456789'
                      + 'abcdefghjkmnpqrstuvwxyz'
                      + 'ABCDEFGHJKMNPQRSTUVWXYZ')
    return ''.join([characters_set[int(random() * len(characters_set))]
                    for _ in range(length)])


def get_now():
    """Return the current UTC time"""
    return datetime.utcnow().replace(tzinfo=timezone.utc)
