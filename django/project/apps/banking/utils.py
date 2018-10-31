import hashlib
from random import SystemRandom, randint
from string import digits
from django.apps import apps


def generate_credit_card_number(length=16):
    """
    :return string:
    """
    card_model = apps.get_model('banking', 'Card')
    card_number = True

    while card_number:
        number = ''.join(SystemRandom().choice(digits) for _ in range(length))
        card_number = card_model.objects.filter(number=number).exists()
        if not card_number:
            return number


def generate_pincode(pin):
    """
    :param pin:
    :return:
    """
    code = hashlib.md5(str(pin).encode('utf-8'))
    return code.hexdigest()


def random_pin(length=4):
    """
    :param length: pincode length
    :return:
    """
    range_start = 10**(length-1)
    range_end = (10**length)-1
    return randint(range_start, range_end)
