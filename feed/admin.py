from django.contrib import admin
from .models import Source, Post, PrePost, ScoredPost

admin.site.register(Source)
admin.site.register(Post)
admin.site.register(PrePost)
admin.site.register(ScoredPost)
