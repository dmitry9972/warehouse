from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from datetime import datetime
from tasks import CDEK_task



class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')


    class Meta(AbstractUser.Meta):
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'



class Order(models.Model):

    order_date = models.DateTimeField(default=datetime.now)

    PROCESSING_ORDER = 1
    SHIPPED = 2
    DELIVERED = 3
    STATUS_CHOICES = (
        (PROCESSING_ORDER, ('We got your order!')),
        (SHIPPED, ('We have packaged your items and have handed your package to our trusted carriers. ')),
        (DELIVERED, ('Delivered')),
    )

    order_info =  models.CharField(max_length=10000, db_index=True,
                            verbose_name='Инфа о заказе')

    order_number = models.IntegerField(default=0, unique=True, verbose_name='Номер заказа')

    order_client = models.CharField(default='', max_length=100, db_index=True,
                            verbose_name='Заказчик')

    cdek_uuid = models.CharField(default='', max_length=100, db_index=True,
                            verbose_name='CDEK UUID')

    def __str__(self):
        return 'Номер заказа: %s' % (self.order_number)

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'
        ordering = ['order_date']



@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender = Order)
def push_order_to_celery(sender, instance=None, created=True, **kwargs):
    if created:

        order = instance

        transfer_data = {}
        transfer_data['order_client'] = order.order_client
        transfer_data['order_pk'] = order.pk
        transfer_data['order_date'] = order.order_date
        transfer_data['order_info'] = order.order_info
        # instanceCDEK = CDEK( 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI',
        #                              'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG' )

        CDEK_task.send_order_to_cdec(transfer_data, order.pk)