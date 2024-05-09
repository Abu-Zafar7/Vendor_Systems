from django.urls import path
from .views import *


urlpatterns = [
    
    path('api/vendors',VendorListCreateAPIView.as_view(), name='vendors'),
    path('api/vendors/<str:pk>', VendorRetrieveUpdateDeleteAPIView.as_view(),name='update_get_delete_vendor'),
    path('api/purchase_orders', PurchaseOrderListCreateAPIView.as_view(), name='create_get_purchase_order'),
    path('api/purchase_orders/<str:pk>',PurchaseOrderRetrieveUpdateDeleteAPIView.as_view(), name='get_update_delete_purchase_orders'),
    path('api/vendors/<str:pk>/performance',VendorPerformanceAPIView.as_view(), name='retrieve_vendor_details'),
    path('api/purchase_orders/<str:pk>/acknowledge', AcknowledgePurchaseOrderAPIView.as_view(), name="acknowledge")
]