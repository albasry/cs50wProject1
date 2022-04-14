from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
    path('wiki/create/', views.create_entry, name='create-entry'),
    path('wiki/<str:title>/edit/', views.edit_entry, name='edit-entry'),
    path('wiki/random/', views.random_entry, name='random'),
    path('wiki/<str:title>/', views.single_entry, name='single-entry'),
    path("", views.index, name="index"),
]
