PROCESSING_ORDER = 1
ORDER_SENT_TO_CARRIER = 2
ORDER_SENT_BACKTO_SHOP = 3
DELIVERED = 4
STATUS_CHOICES = (
    (PROCESSING_ORDER, ('We got your order!')),
    (ORDER_SENT_TO_CARRIER, ('Order is sent to carrier')),
    (ORDER_SENT_BACKTO_SHOP, ('Order is sent back to shop')),
    (DELIVERED, ('Delivered')),
)