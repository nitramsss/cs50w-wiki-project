from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_page, name="createpage"),
    path("edit/<str:page>", views.edit_page, name="editpage"),
    path("random", views.random_page, name="randompage"),
    path("<str:entry>", views.entry_page, name="entrypage") 

]
