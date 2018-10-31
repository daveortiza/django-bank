from django import forms
from django.core.validators import RegexValidator, ValidationError
from .models import Transaction, Card
from .utils import generate_pincode


class TransactionForm(forms.ModelForm):

    pin = forms.CharField(
        validators=[RegexValidator(regex='^[0-9]{4}$', message='Length has to be 4 (only digits)', code='nomatch'), ],
        max_length=4,
        required=True)

    class Meta:
        model = Transaction
        fields = ('card_from', 'card_to', 'sum', 'pin', 'operation', )

    def __init__(self, user, *args, **kwargs):
        """
        :param user:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fields['card_from'].queryset = Card.objects.filter(user=user)

    def clean_pin(self):
        """
        :return:
        """
        card_id = self.cleaned_data.get('card_from').id
        pin = self.cleaned_data.get('pin')
        pin_decode = Card.objects.values_list('pincode', flat=True).get(pk=card_id)
        pin_encode = generate_pincode(pin)

        if pin_decode != pin_encode:
            raise ValidationError('Pincode didn\'t pass validation. Please try again.')

        return True

    def clean(self):
        """
        :return:
        """
        card = self.cleaned_data.get('card_from')
        ops = self.cleaned_data.get('operation')
        cash = float(self.cleaned_data.get('sum'))

        if ops == 'minus' and card.balance < cash:
            self.add_error('sum', f"You have not necessary sum. Current balance is {card.balance:2}")
        elif ops == 'transfer':
            card_receiver = self.cleaned_data.get('card_to')
            if card.balance < cash:
                self.add_error('sum', f"You have not necessary sum. Current balance is {card.balance:2}")
            elif not card_receiver or card_receiver == card:
                self.add_error('operation', 'You must choose a card for transfer')

        return self.cleaned_data

    def save(self):
        """
        :return:
        """
        card = self.cleaned_data.get('card_from')
        ops = self.cleaned_data.get('operation')
        cash = float(self.cleaned_data.get('sum'))

        if ops == 'plus':
            card.balance = card.balance + cash
            card.save()
        elif ops == 'minus':
            card.balance = card.balance - cash
            card.save()
        elif ops == 'transfer':
            card_receiver = self.cleaned_data.get('card_to')
            card.balance = card.balance - cash
            card_receiver.balance = card_receiver.balance + cash
            card_receiver.save()
            card.save()

        self.instance.balance = card.balance

        super().save()



