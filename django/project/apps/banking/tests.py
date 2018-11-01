from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from project.apps.banking.models import Card, Transaction
from project.apps.banking.forms import TransactionForm


class BankingTestCase(TestCase):

    def setUp(self):
        """
        :return:
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.card = Card.objects.create(user=self.user)

    def test_auth_home_path(self):
        """
        :return:
        """
        print('\nRunning test [test_home_path_return_200]')

        self.response = self.client.get('/banking/')
        print('Response status code:', self.response.status_code)

        self.assertEqual(self.response.status_code, 200)

    def test_modal_create_credit_card(self):
        """
        :return:
        """
        print('\nRunning test [test_create_credit_card]')

        cards_count_before = Card.objects.count()
        print(f'Cards count before: {cards_count_before}')

        card_create_request_url = '/banking/create/'
        print('Card request AJAX URL:', card_create_request_url)

        result = self.client.post(card_create_request_url, {
            'user': self.user,
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        print(result)

        cards_count_after = Card.objects.count()
        print(f'Cards count after: {cards_count_after}')

        self.assertEqual(result.status_code, 200)
        self.assertGreater(cards_count_after, cards_count_before)

    def test_put_money_to_card(self):
        """
        :return:
        """
        print('\nRunning test [test_put_money_to_card]')

        print(f'\nBalance before transaction: {self.card.balance}')

        form_data = {
            'card_from': self.card.id,
            'card_to': None,
            'sum': 100,
            'pin': self.card.pin,
            'operation': 'plus'
        }

        form = TransactionForm(self.user.id, form_data)
        self.assertTrue(form.is_valid())
        form.save()

        self.card.refresh_from_db()
        print(f'\nBalance after transaction: {self.card.balance}')
        self.assertGreater(self.card.balance, 0)

    def test_take_money_from_card(self):
        """
        :return:
        """
        print('\nRunning test [test_take_money_from_card]')

        form_data = {
            'card_from': self.card.id,
            'card_to': None,
            'sum': 200,
            'pin': self.card.pin,
            'operation': 'minus'
        }

        form = TransactionForm(self.user.id, form_data)
        self.assertFalse(form.is_valid())

    def test_transfer_money_to_card(self):
        """
        :return:
        """
        print('\nRunning test [test_transfer_money_to_card]')

        form_data = {
            'card_from': self.card.id,
            'card_to': None,
            'sum': 100,
            'pin': self.card.pin,
            'operation': 'plus'
        }

        form = TransactionForm(self.user.id, form_data)
        self.assertTrue(form.is_valid())
        form.save()

        card_receiver = Card.objects.create(user=self.user)

        print(f'\nBalance before transaction: {card_receiver.balance}')

        form_data = {
            'card_from': self.card.id,
            'card_to': card_receiver.id,
            'sum': 10,
            'pin': self.card.pin,
            'operation': 'transfer'
        }

        form = TransactionForm(self.user.id, form_data)
        self.assertTrue(form.is_valid())
        form.save()

        card_receiver.refresh_from_db()
        print(f'\nBalance after transaction: {card_receiver.balance}')
        self.assertGreater(card_receiver.balance, 0)
