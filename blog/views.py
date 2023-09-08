from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Bookmark, BlogRating, Category
from .forms import BlogForm, BlogRatingForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator, Page
from django.http import Http404

# Create a new blog post
def create_blog(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Set the current user as the author
            blog.save()
            return redirect('blog_detail', pk=blog.id) 
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})


# Update an existing blog post
def update_blog(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    
    blog = get_object_or_404(Post, pk=pk)

    # if blog.author != request.user:
    #     raise Http404("You don't have permission to edit this post.")
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.instance.image = blog.image
            form.save()
            return redirect('blog_detail', pk=blog.id)
    else:
        form = BlogForm(instance=blog)

    categories = Category.objects.all()

    return render(request, 'blog/update_blog.html', {'form': form, 'blog': blog, 'categories': categories})


# Delete a blog post
def delete_blog(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    
    blog = get_object_or_404(Post, pk=pk)

    # if blog.author != request.user:
    #     raise Http404("You don't have permission to edit this post.")

    
    if request.method == 'POST':
        blog.delete()
        return redirect('home')  # Redirect to the homepage or another appropriate page
    return render(request, 'blog/delete_blog.html', {'blog': blog})



@login_required
def blog_detail(request, pk):
    blog = get_object_or_404(Post, pk=pk)
    
    related_posts = Post.objects.filter(categories__in=blog.categories.all()).exclude(pk=pk)

    form = BlogRatingForm(request.POST)

    if request.method == 'POST':
        
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            blog_rating, created = BlogRating.objects.get_or_create(blog=blog, user=request.user, defaults={'rating': rating_value})

            if not created:
                blog_rating.rating = rating_value
                blog_rating.save()

            messages.success(request, 'Thank you for rating this blog!')
        else:
            messages.error(request, 'Failed to rate the blog. Please check your input.')

    average_rating = BlogRating.objects.filter(blog=blog).aggregate(Avg('rating'))['rating__avg']

    # Round the average_rating to one decimal place
    if average_rating is not None:
        average_rating = round(average_rating, 1)

    return render(request, 'blog/blogdetail.html', {'blog': blog, 'blog_posts': related_posts, 'form': form, 'average_rating': average_rating})



def blog_list(request):
    query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    blog_posts = Post.objects.all()
    form = SearchForm()

    categories = Category.objects.all()


    if start_date and end_date:
        blog_posts = blog_posts.filter(date__range=[start_date, end_date])


    if query:
        # Filter blog_posts based on the search query
        blog_posts = blog_posts.filter(
            Q(title__icontains=query) | 
            Q(body__icontains=query) 
        )


    blog_posts = blog_posts.order_by('-date')
    blog_posts = blog_posts.annotate(average_rating=Avg('blograting__rating')).order_by('-average_rating')


    paginator = Paginator(blog_posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'blog/blogpost.html', {
        'blog_posts': page, 
        'form': form
    })



@login_required
def bookmark_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not Bookmark.objects.filter(user=request.user, post=post).exists():
        Bookmark.objects.create(user=request.user, post=post)

    return redirect('bookmarks_list')
 

@login_required
def bookmark_remove(request, pk):
    try:
        bookmark = Bookmark.objects.get(user=request.user, pk=pk)
        bookmark.delete()
        
    except Bookmark.DoesNotExist:
        pass
    return redirect('bookmarks_list')
    
    

@login_required
def bookmarks_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'blog/bookmarks_list.html', {'bookmarks': bookmarks})