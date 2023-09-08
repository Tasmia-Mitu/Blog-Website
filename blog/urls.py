# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('create-blog/', views.create_blog, name='create_blog'),
    path('update-blog/<int:pk>/', views.update_blog, name='update_blog'),
    path('delete-blog/<int:pk>/', views.delete_blog, name='delete_blog'),
    path('blog-detail/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/', views.blog_list, name='blog_list'),

    path('bookmark-add/<int:pk>/', views.bookmark_add, name='bookmark_add'),
    path('bookmark-remove/<int:pk>/', views.bookmark_remove, name='bookmark_remove'),

    path('bookmarks/', views.bookmarks_list, name='bookmarks_list'),
]
