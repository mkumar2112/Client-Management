from django.urls import path
from .views import *

urlpatterns = [
    # path('', home, name='home'),
    path('clients/', client_list, name='client-list'),
    path('clients/<id>/view', client_detail, name='client-detail'),
    path('clients/create/', create_client, name='create-client'),
    path('clients/<str:id>/update/', update_client, name='update-client'),
    path('clients/<str:id>/delete/', delete_client, name='delete-client'),
    path('save-pdf/<str:id>/', save_as_pdf, name='save-pdf'),

]

