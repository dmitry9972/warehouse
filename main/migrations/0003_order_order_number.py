# Generated by Django 3.2.6 on 2021-09-02 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(default=0, unique=True, verbose_name='Номер заказа'),
        ),
    ]
