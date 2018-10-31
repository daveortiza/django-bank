from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def color_operation(operation_type: str):
    """
    View Helper
    :param operation_type:str
    :return:
    """
    if operation_type == 'plus':
        return '#1dd000'
    elif operation_type == 'minus':
        return '#ff0000'
    elif operation_type == 'transfer':
        return '#0004ef'


@register.filter()
@stringfilter
def amazing_number(card_number: str):
    """
    View Helper
    :param card_number:str
    :return:
    """
    card = []
    for index, number in enumerate(card_number):
        card.append(number)
        odd = (index + 1) % 4
        if odd == 0:
            card.append('&nbsp;&nbsp;&nbsp;')

    return ''.join(card)
