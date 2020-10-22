from django.urls import path
from django.conf.urls import url
from receiving import views

app_name = 'receiving'
urlpatterns = [
    path('receivingpage/', views.receiving_page, name='receiving_page'),
]