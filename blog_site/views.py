from django.shortcuts import render
from blog.models import Post, BlogRating

def home(request):
    blogs = Post.objects.all()
    
    average_rating = BlogRating.objects.all()

    context= {'blogs': blogs, 'average_rating':average_rating}
    
    return render(request, 'index.html', context )

 
def contact(request):
    return render(request, 'contact.html')  