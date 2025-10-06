from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>/edit", views.edit_product, name="edit_product"),
]