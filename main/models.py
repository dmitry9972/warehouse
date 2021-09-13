from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from datetime import datetime
from tasks import push_order_to_carrier
import main.const

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')

    class Meta(AbstractUser.Meta):
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'


class Order(models.Model):
    status = models.PositiveSmallIntegerField(choices=main.const.STATUS_CHOICES, default=main.const.PROCESSING_ORDER,
                                              verbose_name='Статус')

    order_date = models.DateTimeField(default=datetime.now)

    order_info = models.CharField(max_length=10000, db_index=True,
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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#
# @receiver(post_save, sender=Order)
# def push_order_to_celery(sender, instance=None, created=True, **kwargs):
#     if created:
#         order = instance
#
#         transfer_data = {}
#         transfer_data['order_client'] = order.order_client
#         transfer_data['order_pk'] = order.pk
#         transfer_data['order_date'] = order.order_date
#         transfer_data['order_info'] = order.order_info
#
#         push_order_to_carrier.delay(transfer_data, order.pk)
