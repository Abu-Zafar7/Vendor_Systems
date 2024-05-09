
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from .views import VendorPerformanceAPIView

@receiver(post_save, sender=PurchaseOrder)
def handle_purchase_order_save(sender, instance, **kwargs):
  
    vendor_performance_view = VendorPerformanceAPIView()
    vendor_performance_view.calculate_performance_metrics(instance.vendor)