from django.contrib import admin
from.models import Post, Bookmark, Category

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_category_names','author','date' , 'modified_date']

    def get_category_names(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    
    get_category_names.short_description = 'Categories'


admin.site.register(Post, PostAdmin)
admin.site.register(Bookmark)
admin.site.register(Category)
