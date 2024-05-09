from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from datetime import timedelta



class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id','name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'avg_response_time', 'fulfillment_rate']
        read_only_fields = ['on_time_delivery_rate', 'quality_rating_avg', 'avg_response_time', 'fulfillment_rate']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']
        

  

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ['id', 'vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'avg_response_time', 'fulfillment_rate']
        read_only_fields = ['id', 'vendor']




class TimedeltaField(serializers.Field):
    def to_representation(self, value):
        # Check if the value is a timedelta object
        if isinstance(value, timedelta):
            # Convert timedelta to float representation (in seconds)
            return value.total_seconds()
        else:
            # If the value is not a timedelta object, return None
            return None

class VendorPerformanceSerializer(serializers.Serializer):
    vendor_id = serializers.IntegerField()
    on_time_delivery_rate = serializers.FloatField()
    quality_rating_avg = serializers.FloatField()
    avg_response_time = TimedeltaField()
    fulfillment_rate = serializers.FloatField()