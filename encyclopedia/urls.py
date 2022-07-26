from django.urls import path

from . import views

app_name = "WIKI"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:prefix>", views.title, name="title"),
    path("find/wiki/", views.search, name="search"),
    path("new/wiki", views.create_entry, name="create_entry"),
    path("random/wiki/", views.random_entry, name="random"),
    path("edits/wiki/<str:prefix>", views.edit_entry, name="edit")
]
