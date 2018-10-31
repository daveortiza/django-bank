from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from project.apps.banking.models import Card, Transaction


class BankingTestCase(TestCase):

    def setUp(self):
        """
        :return:
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')