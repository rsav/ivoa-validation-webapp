from django.urls import path

from .views import ServicesListView, ServicesListViewJson, ServersListView, ErrorsListView, ErrorsListViewJson, EfreqsListView


urlpatterns = [
    path('services', ServicesListView.as_view(), name='services'),
    path('services_json', ServicesListViewJson.as_view(), name='services_json'),
    path('servers', ServersListView.as_view(), name='servers'),
    path('errors', ErrorsListView.as_view(), name='errors'),
    path('efreqs', EfreqsListView.as_view(), name='efreqs'),
    path('errors_json', ErrorsListViewJson.as_view(), name='errors_json'),
    

]


