from django.urls import path
from . import views

app_name='gallery'
urlpatterns=[
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:id>/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
]