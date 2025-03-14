from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Category, Product

# Create your views here.

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

def test_view(request):
    return render(request, 'products/test.html')

def home(request):
    categories = Category.objects.all()
    search_query = request.GET.get('q', '')
    
    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).distinct()[:12]
    else:
        products = Product.objects.filter(featured=True)[:6]
    
    context = {
        'categories': categories,
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'products/home.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    search_query = request.GET.get('q', '')
    
    if search_query:
        products = category.products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        ).distinct()
    else:
        products = category.products.all()
    
    context = {
        'category': category,
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'products/category_detail.html', context)
