from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# View to display all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'forum/category_list.html', {'categories': categories})

# View to display posts in a specific category
def post_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = category.posts.all()
    return render(request, 'forum/post_list.html', {'category': category, 'posts': posts})

# View to display a single post with comments
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.created_by = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

# View to create a new post
from django.contrib.auth.decorators import login_required
@login_required
def create_post(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.created_by = request.user
            new_post.category = category
            new_post.save()
            return redirect('post_list', category_id=category.id)
    else:
        post_form = PostForm()
    return render(request, 'forum/create_post.html', {'post_form': post_form, 'category': category})

@login_required
def delete_post(request, post_id):
    # Get the post
    post = get_object_or_404(Post, id=post_id)

    # Check if the logged-in user is the creator of the post
    if post.created_by != request.user:
        raise Http404("You are not authorized to delete this post")

    # Delete the post
    post.delete()

    # Redirect the user to the post list or another page
    return redirect('category_list')  # Redirect to a relevant page, e.g., category list or home