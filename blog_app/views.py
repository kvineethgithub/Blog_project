from django.shortcuts import render, redirect
from .models import Post, Like, Dislike, Comment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q


def user_register(request):
    """ this function is used for registering into the application"""
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if password == confirm_password:
            if User.objects.filter(username=user_name):
                messages.success(request, "User name already exists...!!")
                return redirect(user_register)
            elif User.objects.filter(email=email):
                messages.success(request, "Email already exists...!!")
                return redirect(user_register)
            else:
                User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=user_name,
                                         password=password)
                messages.success(request, "User registered successfully...!!!")
                return redirect(user_login)
        else:
            messages.success(request, "Passwords not matching...!!!")
            return redirect(user_register)

    else:
        return render(request, 'auth/register.html', {})


def user_login(request):
    """ this function is used for login into the application"""
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In successfully...!!!")
            return redirect(home_page)
        else:
            messages.success(request, "Invalid credentials..!!!")
            return redirect(user_login)
    return render(request, 'auth/login.html', {})


@login_required
def user_logout(request):
    """ this function is used for logout from application"""
    logout(request)
    messages.success(request, "Logout successfully..!!!")
    return redirect(user_login)


@login_required
def user_profile(request):
    """ this function is used for getting the current user profile"""
    user = User.objects.get(username=request.user)
    return render(request, 'blog/profile.html', {'user': user})


@login_required
def home_page(request):
    """ this function is used for getting all the blogs with most liked and most commented"""
    posts = Post.objects.order_by('-no_of_likes') & Post.objects.order_by('-no_of_comments')
    return render(request, 'blog/home.html', {'posts': posts})


@login_required
def uploaded_blogs(request):
    """ this function is used for getting all the blogs uploaded by current user"""
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/upload_blogs.html', {'posts': posts})


@login_required
def blog_create(request):
    """ this function is used for create new blog"""
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if Post.objects.filter(title=title):
            messages.success(request, "blog with {} already existed..".format(title))
            return render(request, 'blog/blog_create.html', {})
        else:
            Post.objects.create(title=title, content=content, author=request.user)
            messages.success(request, "New blog created successfully..!!")
            return redirect(home_page)
    return render(request, 'blog/blog_create.html', {})


@login_required
def detail_blog_view(request, id=None):
    """ this function is used for particular blog """
    each_post = Post.objects.get(id=id)
    return render(request, 'blog/detail_blog.html', {'each_post': each_post})


@login_required
def delete_blog(request, id=None):
    """ this function is used for deleting the particular blog"""
    each_post = Post.objects.get(id=id)
    each_post.delete()
    messages.success(request, "Blog deleted successfully..!!")
    return redirect(uploaded_blogs)


@login_required
def edit_blog(request, id=None):
    """ this function is used for updating particular blog"""
    each_post = Post.objects.get(id=id)
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.filter(id=id).update(title=title, content=content, pub_date=timezone.now())
        return redirect(uploaded_blogs)
    return render(request, 'blog/blog_edit.html', {'each_post': each_post})


@login_required
def likes_view(request, id=None):
    """ this function used for liking the blog"""
    post = Post.objects.get(id=id)
    if Like.objects.filter(Q(post_id=id) & Q(user=request.user)):
        return redirect(home_page)
    else:
        disliked_users = Dislike.objects.filter(Q(post_id=id) & Q(user=request.user))
        if disliked_users:
            likes = post.no_of_likes
            dislikes = post.no_of_dislikes
            dislikes = dislikes - 1
            likes = likes + 1
            Post.objects.filter(id=id).update(no_of_likes=likes, no_of_dislikes=dislikes)
            Like.objects.create(post_id=id, user=request.user)
            disliked_users.delete()
            return redirect(home_page)
        else:
            likes = post.no_of_likes
            likes = likes + 1
            Post.objects.filter(id=id).update(no_of_likes=likes)
            Like.objects.create(post_id=post.id, user=request.user)
            return redirect(home_page)


@login_required
def liked_users(request, id=None):
    """ this function is used for getting all liked users """
    users = Like.objects.filter(post_id=id)
    each_post = Post.objects.get(id=id)
    return render(request, 'blog/detail_blog.html', {'each_post': each_post, 'users': users})


@login_required
def dislikes_view(request, id=None):
    """ this function is used for disliking the blog """
    post = Post.objects.get(id=id)
    if Dislike.objects.filter(Q(post_id=id) & Q(user=request.user)):
        return redirect(home_page)
    else:
        liked_users = Like.objects.filter(Q(post_id=id) & Q(user=request.user))
        if liked_users:
            likes = post.no_of_likes
            dislikes = post.no_of_dislikes
            dislikes = dislikes + 1
            likes = likes - 1
            Post.objects.filter(id=id).update(no_of_likes=likes, no_of_dislikes=dislikes)
            Dislike.objects.create(post_id=post.id, user=request.user)
            liked_users.delete()
            return redirect(home_page)
        else:
            dislikes = post.no_of_dislikes
            dislikes = dislikes + 1
            Post.objects.filter(id=id).update(no_of_dislikes=dislikes)
            Dislike.objects.create(post_id=post.id, user=request.user)
            return redirect(home_page)


@login_required
def disliked_users(request, id=None):
    """ this function is used for getting all disliked users"""
    users = Dislike.objects.filter(post_id=id)
    each_post = Post.objects.get(id=id)
    return render(request, 'blog/detail_blog.html', {'each_post': each_post, 'users': users})


@login_required
def comments_view(request, id=None):
    """ this function is used for commenting the blog """
    comments = Comment.objects.filter(post_id=id)
    each_post = Post.objects.get(id=id)
    if request.method == "POST":
        comment = request.POST.get('comment')
        post = Post.objects.get(id=id)
        com_count = post.no_of_comments
        com_count = com_count + 1
        Post.objects.filter(id=id).update(no_of_comments=com_count)
        Comment.objects.create(post_id=post.id, comment=comment, user=request.user)
        return redirect(home_page)

    return render(request, 'blog/detail_blog.html', {'each_post': each_post, 'comments': comments})
