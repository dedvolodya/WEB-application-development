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


def doc(request):
    return render(request, 'doc.html')

def openapi(request):
    data = {
        "swagger": "2.0",
        "title": "Simple Blog",
        "info": {
            "title": "Simple Blog",
            "description": "My first python/django blog.",
            "contact": {
                "name": "Volodymyr Kravchuk",
                "github": "https://github.com/ded_volodya"
            }
        },
        "basePath": "/",
        "paths": {
            "/blog/about": {
                "get": {
                    "tags": [
                        "/blog/about"
                    ],
                    "summary": "Get app description",
                    "description": "",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "app_name": {
                                        "type": "string"
                                    },
                                    "about": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/blog/register": {
                "get": {
                    "tags": [
                        "/blog/register"
                    ],
                    "summary": "Register new user",
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "username",
                            "in": "path",
                            "description": "",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "password",
                            "in": "path",
                            "description": "",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "email",
                            "in": "path",
                            "description": "",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "json",
                                "properties": {
                                    "result": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/blog/login": {
                "get": {
                    "tags": [
                        "/blog/login"
                    ],
                    "summary": "Log in user",
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "password",
                            "in": "path",
                            "description": "",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "username",
                            "in": "path",
                            "description": "",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "result": {
                                        "type": "string"
                                    },
                                    "username": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/blog/users/{username}/profile": {
                "get": {
                    "tags": [
                        "/blog/users/{username}/profile"
                    ],
                    "summary": "Return user profile information",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "username": {
                                        "type": "string"
                                    },
                                    "email": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/blog/get_posts": {
                "get": {
                    "tags": [
                        "/blog/get_posts"
                    ],
                    "summary": "List of latest posts",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "array",
                                "properties": {
                                    "title": {
                                        "type": "string"
                                    },
                                    "author": {
                                        "type": "string"
                                    },
                                    "content": {
                                        "type": "string"
                                    },
                                    "publish": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/blog/post/{postId}/add_comment": {
                "get": {
                    "tags": [
                        "/blog/post/{postId}/add_comment"
                    ],
                    "summary": "Leave comment for post",
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "content",
                            "in": "path",
                            "description": "",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "post_id": {
                                        "type": "integer",
                                        "format": "int64"
                                    },
                                    "comment_id": {
                                        "type": "integer",
                                        "format": "int64"
                                    },
                                    "result": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/blog/add_post": {
                "get": {
                    "tags": [
                        "/blog/add_post"
                    ],
                    "summary": "Add new post",
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "title",
                            "in": "path",
                            "description": "",
                            "required": False,
                            "type": "string"
                        },
                        {
                            "name": "content",
                            "in": "path",
                            "description": "",
                            "required": False,
                            "type": "int"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "post_id": {
                                        "type": "integer",
                                        "format": "int64"
                                    },
                                    "result": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "securityDefinitions": {
            "api_key": {
                "type": "apiKey",
                "name": "api_key",
                "in": "header"
            }
        }
    }
    return JsonResponse(data, safe=False)