# blog/urls.py
# description: the app-specific URLS for the HW application


from django.urls import path
from django.conf import settings
from . import views


# create list of URLs for app:
urlpatterns = [
   
   path('', views.ArticleView.as_view(), name='random'),
   path('show_all', views.ShowAllViews.as_view(), name='show_all'),
   path('article/<int:pk>', views.ArticleView.as_view(), name='article'),
    path('article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'),
   
]
