from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

# class CreateVendorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = ['name', 'contact_details', 'address','vendor_code']


# class CreatePurchaseOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PurchaseOrder
#         fields = ['po_number', 'vendor', 'order_date', 'delivery_date', 'status', 'items', 'quantity', 'quality_rating', 'issue_date', 'acknowledgment_date']

# class PurcharseOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PurchaseOrder
#         fields = ['po_number', 'vendor', 'order_date', 'delivery_date', 'status', 'items', 'quantity', 'quality_rating', 'issue_date', 'acknowledgment_date' ]   


# class HistoricalPerformanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HistoricalPerformance
#         fields = "__all__"
# vendors/serializers.py


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        read_only_fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']
        read_only_fields = ['status']

    def validate(self, data):
        # Perform custom validation if needed
        return data

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ['id', 'vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        read_only_fields = ['id', 'vendor']


class VendorPerformanceSerializer(serializers.Serializer):
    vendor_id = serializers.IntegerField()
    on_time_delivery_rate = serializers.FloatField()
    quality_rating_avg = serializers.FloatField()
    average_response_time = serializers.FloatField()
    fulfillment_rate = serializers.FloatField()