from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='article-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='article-detail'),
]
