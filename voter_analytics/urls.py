# voter_analytics/urls.py


from django.urls import path
from . import views

from django.urls import path
from .views import VoterDetailView, VoterGraphsView, VoterListView

urlpatterns = [
    # /voter_analytics/ base URL pattern renders ListView
    path('', VoterListView.as_view(), name='voters'),
    # /voter_analytics/<int:pk> view. Displays single record
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    # /voter_analytics/graphs/ renders Graphs from the models
    path('graphs/', VoterGraphsView.as_view(), name='graphs'),
]