from django.db import models
from django.contrib.auth.models import User

CATEGORY = [
    ('MachineLearning', 'Machine Learning'),
    ('News', 'News'),
    ('Sports', 'Sports'),
    ('Test', 'Test'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, choices=CATEGORY)
    
    def __str__(self):
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length=200) 
    body = models.TextField()
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/blog', blank=True)
    #image = models.FileField(upload_to='photos/blog')
    date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.title

     
     
    
class BlogRating(models.Model):
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s bookmark for {self.post.title}"