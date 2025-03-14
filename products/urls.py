from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test_view, name='test'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
] 