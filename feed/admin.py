from django.contrib import admin
from .models import Source, Post, RawPost, ScoredPost, SourceGroup

admin.site.register(Source)
admin.site.register(Post)
admin.site.register(RawPost)
admin.site.register(ScoredPost)
admin.site.register(SourceGroup)