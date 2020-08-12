from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.randpage, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("add", views.add, name="add"),
    path("edit/<str:title>", views.edit, name="edit"),
]
