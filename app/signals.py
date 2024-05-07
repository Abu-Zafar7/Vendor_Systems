
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from .logic import update_vendor_performance_metrics

@receiver(post_save, sender=PurchaseOrder)
def handle_purchase_order_save(sender, instance, **kwargs):
    update_vendor_performance_metrics(instance.vendor)