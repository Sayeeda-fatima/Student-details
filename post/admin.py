from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ("post_title", "created_on", "user", "picture")

admin.site.register(Post, PostAdmin)
    
