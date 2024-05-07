
from django.db.models import F, Avg, Count
from .models import PurchaseOrder
from django.utils import timezone

def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_completed_pos = completed_pos.count()
    on_time_deliveries = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count()
    
    if total_completed_pos > 0:
        return (on_time_deliveries / total_completed_pos) * 100
    else:
        return 0

def calculate_quality_rating_avg(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(quality_rating__isnull=True)
    if completed_pos.exists():
        return completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']
    else:
        return None

def calculate_average_response_time(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(acknowledgment_date__isnull=True)
    if completed_pos.exists():
        return completed_pos.aggregate(Avg(F('acknowledgment_date') - F('issue_date')))['acknowledgment_date__avg']
    else:
        return None

def calculate_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    total_pos_count = total_pos.count()
    if total_pos_count > 0:
        fulfilled_pos_count = total_pos.filter(status='completed').count()
        return (fulfilled_pos_count / total_pos_count) * 100
    else:
        return 0




def acknowledge_purchase_order(purchase_order):
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()