from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from .utils import generate_pincode, generate_credit_card_number, random_pin


class Card(models.Model):

    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    number = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(regex='^[0-9]{16}$', message='Length has to be 16', code='nomatch'),
        ],
        blank=False,
        unique=True)
    balance = models.FloatField(default=0.0)
    pincode = models.CharField(max_length=100, default=None, blank=False, editable=False)
    updated = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = ('Card')
        verbose_name_plural = ('Cards')
        ordering = ["-created"]

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

        if self.pincode is None:
            self.pin = random_pin()

    def save(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        if self.pk is None:
            self.number = generate_credit_card_number()
            self.pincode = generate_pincode(self.pin)

        super().save(*args, **kwargs)

    def check_pincode(self, pin):
        """
        :param pin:
        :return:
        """
        pincode = generate_pincode(pin)
        if pincode != self.pincode:
            return False

        return True

    def __str__(self): return self.number


class Transaction(models.Model):

    CHOICES = (('plus', 'Put money'), ('minus', 'Take money'), ('transfer', 'Transfer money'),)
    operation = models.CharField(max_length=16, choices=CHOICES, blank=False, default='plus')

    card_from = models.ForeignKey(Card, on_delete=models.PROTECT, related_name='card_from')
    card_to = models.ForeignKey(
        Card, on_delete=models.PROTECT, related_name='card_to', blank=True, default=None, null=True)

    sum = models.FloatField(default=0.0, validators=[MinValueValidator(0.1), MaxValueValidator(1000000)])
    balance = models.FloatField(default=0.0)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = ('Transaction')
        verbose_name_plural = ('Transactions')
        ordering = ["-created"]

    def __str__(self):
        return f'{self.card_from.number} at {self.created.strftime("%d.%m.%Y %H:%M")}'
