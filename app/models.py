from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .logic import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, calculate_fulfillment_rate


class Vendor(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    avg_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.name



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=[
        ('pending','Pending'),
        ('completed','Completed'),
        ('canceled','Canceled')
    ])
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor} - {self.status}"
    


 

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default= timezone.now)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    vendor.quality_rating_avg = calculate_quality_rating_avg(vendor)
    vendor.average_response_time = calculate_average_response_time(vendor)
    vendor.fulfillment_rate = calculate_fulfillment_rate(vendor)
    vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def handle_purchase_order_save(sender, instance, **kwargs):
    update_vendor_performance_metrics(instance.vendor)
