from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post
from taggit.models import Tag
from django.http import HttpResponse
from .forms import PostForm

# Create your views here.
def post_list(request, tag_slug=None):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    tag = None

    if tag_slug:
    	tag = get_object_or_404(Tag, slug=tag_slug)
    	posts = Post.objects.filter(tags__in=[tag])

    return render(request, 'blog/post_list.html', {'posts':posts, 'tag': tag})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def tag_list(request):
	tags = Post.tags.all()

	return render(request, 'blog/tag_list.html', {'tags': tags})

def search(request):
    try:
        q = request.GET['q']
        posts = Post.objects.filter(title__contains=q) | \
                Post.objects.filter(text__contains=q)
        return render(request, 'blog/result.html', {'posts':posts, 'q':q})

    except KeyError:
        return render(request, 'blog/result.html')

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            #save tags
            form.save_m2m()

            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

             #save tags
            form.save_m2m()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
