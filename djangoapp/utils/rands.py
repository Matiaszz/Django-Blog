import string
from random import SystemRandom
from django.utils.text import slugify


def random_letters(length: int) -> str:
    return ''.join(SystemRandom().choices(string.ascii_letters + string.digits,
                                          k=length))


def new_slugfy(text: str, k: int) -> str:
    return slugify(text) + random_letters(k)
