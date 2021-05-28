import json

from django.contrib.auth import authenticate, login
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from blog.models import Post, User, Comment


def get_posts(request):
    if request.method == 'GET':
        latest_5 = Post.objects.all()[:5]
        posts = {}
        for post in latest_5:
            posts[post.id] = {
                "title": post.title,
                "author": User.objects.get(id=post.author.id).username,
                "content": post.content,
                "publish": json.dumps(post.publish, cls=DjangoJSONEncoder)
            }
        dump = {"latest_posts": posts}
        return JsonResponse(dump)
    else:
        dump = {"latest_posts": "GET method should be used to retrieve data"}
        return JsonResponse(dump)


def add_post(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            content = request.GET['content']
            title = request.GET['title']
            post = Post.objects.create(author=request.user, content=content, title=title)
            post.save()
            data = {'post': post.id, 'success': 'true'}
        else:
            data = {'error': 'no logged user'}
    else:
        data = {'error': 'for creating new post GET method should be used'}
    return JsonResponse(data, safe=False)


def register(request):
    if request.method == 'GET':
        username = request.GET['username']
        password = request.GET['password']
        email = request.GET['email']
        user = User.objects.filter(username=username).first()
        if user is not None:
            data = {'result': 'user already exists'}
        else:
            user = User.objects.create(username=username, password=password, email=email)
            user.save()
            data = {'result': 'registered'}
    else:
        data = {'result': 'for creating new user GET method should be used'}
    return JsonResponse(data)


def add_comment(request, post_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            post = Post.objects.filter(id=post_id).first()
            if post is not None:
                content = request.GET['content']
                comment = Comment.objects.create(author=request.user, post=post, content=content)
                comment.save()
                data = {'post': post.id, 'comment':comment.id, 'success': 'true'}
            else:
                data = {'error': 'post does not exist'}
        else:
            data = {'error': 'no logged user'}
    else:
        data = {'error': 'for leaving comments GET method should be used'}
    return JsonResponse(data, safe=False)


def login_f(request):
    if request.method == 'GET':
        username = request.GET['username']
        password = request.GET['password']
        user_obj = User.objects.filter(username=username).first()
        if user_obj is not None:
            user = authenticate(username=user_obj.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    data = {
                        'success': True,
                        'username': user_obj.username
                    }
                    return JsonResponse(data)
    data = {'success': False}
    return JsonResponse(data)


def profile(request, username):
    if request.method == 'GET':
        user_obj = User.objects.filter(username=username).first()
        if user_obj is not None:
            data = {
                'username': user_obj.username,
                'email': user_obj.email
            }
            return JsonResponse(data)
        else:
            data = {'error': 'User does not exists'}
    else:
        data = {'error': 'GET method should be used'}
    return JsonResponse(data)


def about(request):
    data = {
        'name': 'Simple Blog Example',
        'description': 'My first blog implemented using python/django'
    }

    return JsonResponse(data, safe=False)
