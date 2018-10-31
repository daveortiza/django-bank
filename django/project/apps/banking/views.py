from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import Http404
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .models import Card, Transaction
from .forms import TransactionForm


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@login_required
def home(request):
    """
    :param request:
    :return:
    """
    #if 'cards' in cache:
    #    cards = cache.get('cards')
    #else:
    cards = Card.objects.filter(user=request.user)
    #cache.set('cards', cards, timeout=CACHE_TTL)

    return render(request, 'banking/home.html', {
        'cards': cards
    })


@csrf_exempt
def card_modal(request):
    """
    :param request:
    :return:
    """
    modal = render_to_string('banking/modals/card.html')
    return JsonResponse({'modal': modal})


@csrf_exempt
def create(request):
    if request.user.is_authenticated:
        try:
            credit_card = Card(user=request.user)
            credit_card.save()
        except ValidationError:
            return JsonResponse({'_status': '500'})
        else:
            return JsonResponse({
                '_status': '200',
                'card': credit_card.number,
                'pincode': credit_card.pin
            })
    else:
        return JsonResponse({'_status': '403'})


@csrf_exempt
def transaction_form(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = TransactionForm(request.user.id, request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'_status': '201'})
    else:
        form = TransactionForm(request.user)

    context = {'form': form}
    modal = render_to_string('banking/modals/transaction.html', context, request=request, )
    return JsonResponse({
        '_status': '200',
        'modal': modal,
    })


@login_required
def card(request, card_number):
    """
    :param request:
    :param card_number:
    :param page:
    :return:
    """
    page = request.GET.get('page', 1)
    transaction_list = Transaction.objects.all()
    paginator = Paginator(transaction_list, 20)

    try:
        credit_card = Card.objects.get(number=card_number)
    except Card.DoesNotExist:
        raise Http404("Credit card does not exist")

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return render(request, 'banking/card.html', {
        'card': credit_card,
        'transactions': transactions,
    })
