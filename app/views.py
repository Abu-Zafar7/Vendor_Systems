from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from .logic import acknowledge_purchase_order
from django.db.models import F, Avg, Count,ExpressionWrapper, fields
class VendorListCreateAPIView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorRetrieveUpdateDeleteAPIView(APIView):
    def get(self, request, pk):
        try:
            vendor = Vendor.objects.get(id=pk)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = Vendor.objects.get(id=pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = Vendor.objects.get(id = pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderListCreateAPIView(APIView):
    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderRetrieveUpdateDeleteAPIView(APIView):
    def get(self, request, pk):
        purchase_order = PurchaseOrder.objects.get(id=pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, pk):
        purchase_order = PurchaseOrder.objects.get(id=pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        purchase_order = PurchaseOrder.objects.get(id=pk)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class VendorPerformanceAPIView(APIView):
    def get(self, request, pk):
        try:
            vendor = Vendor.objects.get(id=pk)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        performance_metrics = self.calculate_performance_metrics(vendor)  # Call the method
        data = {
            "vendor_id": pk,
            **performance_metrics
        }

        serializer = VendorPerformanceSerializer(data)
        return Response(serializer.data)

    def calculate_on_time_delivery_rate(self, vendor):
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_pos = completed_pos.count()
        on_time_deliveries = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count()
        
        if total_completed_pos > 0:
            return (on_time_deliveries / total_completed_pos) * 100
        else:
            return 0

    def calculate_quality_rating_avg(self, vendor):
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(quality_rating__isnull=True)
        if completed_pos.exists():
            return completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']
        else:
            return None

    def calculate_average_response_time(self, vendor):
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(acknowledgment_date__isnull=True)
        if completed_pos.exists():
           
            avg_response_time_expr = ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=fields.DurationField()
            )
            return completed_pos.aggregate(avg_response_time=Avg(avg_response_time_expr))['avg_response_time']
        else:
            return None

    def calculate_fulfillment_rate(self, vendor):
        total_pos = PurchaseOrder.objects.filter(vendor=vendor)
        total_pos_count = total_pos.count()
        if total_pos_count > 0:
            fulfilled_pos_count = total_pos.filter(status='completed').count()
            return (fulfilled_pos_count / total_pos_count) * 100
        else:
            return 0

    def calculate_performance_metrics(self, vendor):
        
        on_time_delivery_rate = self.calculate_on_time_delivery_rate(vendor)
        quality_rating_avg = self.calculate_quality_rating_avg(vendor)
        avg_response_time = self.calculate_average_response_time(vendor)
        fulfillment_rate = self.calculate_fulfillment_rate(vendor)

        return {
            "on_time_delivery_rate": on_time_delivery_rate,
            "quality_rating_avg": quality_rating_avg,
            "avg_response_time": avg_response_time,
            "fulfillment_rate": fulfillment_rate
        }


    
class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, pk):
        acknowledge_purchase_order(pk)
        return Response({"message": "Purchase Order acknowledged successfully"}, status=status.HTTP_200_OK)