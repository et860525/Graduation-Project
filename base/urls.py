from django.urls import path
from base import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'result/<str:stockname>', views.search_result, name='stock_result')
]