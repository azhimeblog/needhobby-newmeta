from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .models import Websitedetail
from django.shortcuts import redirect
from .models import Category




# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/postlist.html', {'posts': posts})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post_read.html', {'post': post})

def cat_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/categories.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'blog/category_detail.html', {'category': category})

def website_title(request):
    websitedetail = Websitedetail.object.all()
    return render(request, 'blog/base.html', {'websitedetail': websitedetail})
