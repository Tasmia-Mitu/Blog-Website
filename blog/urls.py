# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('create_blog/', views.create_blog, name='create_blog'),
    path('update_blog/<int:pk>/', views.update_blog, name='update_blog'),
    path('delete_blog/<int:pk>/', views.delete_blog, name='delete_blog'),
    path('blog_detail/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/', views.blog_list, name='blog_list'),

    path('bookmark_add/<int:pk>/', views.bookmark_add, name='bookmark_add'),
    path('bookmark_remove/<int:pk>/', views.bookmark_remove, name='bookmark_remove'),

    path('bookmarks/', views.bookmarks_list, name='bookmarks_list'),
]
