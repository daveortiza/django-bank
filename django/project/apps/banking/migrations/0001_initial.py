# Generated by Django 2.1.2 on 2018-10-30 11:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.TextField(unique=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 16', regex='^[0-9]{16}$')])),
                ('balance', models.FloatField(default=0.0)),
                ('pincode', models.CharField(editable=False, max_length=100)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Card',
                'verbose_name_plural': 'Cards',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.1)])),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('card_from', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='card_from', to='banking.Card')),
                ('card_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='card_to', to='banking.Card')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-created'],
            },
        ),
    ]
