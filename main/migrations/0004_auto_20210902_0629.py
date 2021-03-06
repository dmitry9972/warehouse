# Generated by Django 3.2.6 on 2021-09-02 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_order_order_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['order_date'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AddField(
            model_name='order',
            name='order_client',
            field=models.CharField(db_index=True, default='', max_length=100, verbose_name='Заказчик'),
        ),
    ]
