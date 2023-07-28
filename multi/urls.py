
from django.urls import path
from .views import *

app_name = 'multi'
urlpatterns =[
     path('multi_apply_view', multi_apply_view),
     path('multi_map_view', multi_map_view),
     path('multi_imap_view', multi_imap_view),
     path('example_multi_view',example_multi_view),
    ]