from django.urls import path

from . import views

urlpatterns = [
    path("settings", views.site_settings, name="site_settings"),
    path("products", views.manage_products, name="manage_products"),
]