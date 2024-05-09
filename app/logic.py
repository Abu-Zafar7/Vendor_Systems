
from django.db.models import F, Avg, Count
from .models import PurchaseOrder
from django.utils import timezone





def acknowledge_purchase_order(pk):
    try:
        purchase_order = PurchaseOrder.objects.get(id=pk)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
    except PurchaseOrder.DoesNotExist:
        return "Purchase Order does not exist"







