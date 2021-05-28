from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    # blog/get_posts
    path('get_posts', views.get_posts, name='get_posts'),
    # blog/add_post&content=..&title=..
    path('add_post', views.add_post, name='add_post'),
    # blog/post/'5'/add_comment?&content=..
    path('post/<int:post_id>/add_comment', views.add_comment, name='add_comment'),
    # blog/register?username=..&email=..&password=..
    path('register', views.register, name='register'),
    # blog/login?username=..&password=..
    path('login', views.login_f, name='login'),
    # blog/users/'username'/profile
    path('users/<str:username>/profile', views.profile, name='profile'),
    # blog/about
    path('about', views.about, name=''),
]
