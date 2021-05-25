from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('search', views.SearchView.as_view(), name='search'),
    path('available/<slug:url>/',views.BedroomDetailView.as_view(),name='available'),

]
