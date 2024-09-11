from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListCreateView.as_view(), name='product_list'),
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('<int:pk>/', views.ArticleUpdateDeleteView.as_view(), name='update'),
]
