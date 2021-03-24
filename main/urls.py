from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('<slug:slug>', views.redirect_to_website, name='redirect_to_website'),
]