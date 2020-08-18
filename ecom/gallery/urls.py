from django.urls import path
from . import views

app_name='gallery'
urlpatterns=[
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:id>/add/', views.add_to_cart, name='add_to_cart'),
    path('<int:id>/remove/', views.remove_item, name='remove_item'),
    path('cart/', views.view_cart, name='view_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('sellerlist/', views.sellerList, name='sellerList'),
    path('<int:id>/delete/', views.delete_listing, name='delete_listing'),
]