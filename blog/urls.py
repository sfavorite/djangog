from django.urls import path 
from . import views
urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('login/', views.user_login, name='user_login'),
	path('logout/', views.user_logout, name='user_logout'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
	path('newuser', views.new_user),
]