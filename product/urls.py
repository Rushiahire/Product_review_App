from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductInfo.as_view(),name='productinfo'),
    path('new_product/',views.NewProduct.as_view(),name='newproduct'),
    path('review/',views.NewReview.as_view(),name="newreview")
]
