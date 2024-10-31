# blog/urls.py
# description: the app-specific URLS for the HW application


from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

# create list of URLs for app:
urlpatterns = [
   
   path('', views.ArticleView.as_view(), name='random'),
   path('show_all', views.ShowAllView.as_view(), name='show_all'),
   path('article/<int:pk>', views.ArticleView.as_view(), name='article'),
    path('article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'),
        path('article/<int:pk>/create_article', views.CreateCommentView.as_view(), name='create_article'),
   
   
   # authentication related URLS:
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), ## NEW
    path('register/', views.RegistrationView.as_view(), name='register')
]
