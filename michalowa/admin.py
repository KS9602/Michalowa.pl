from django.contrib import admin
from .models import ForumUser, Subject, Post, Section

admin.site.register(ForumUser)
admin.site.register(Subject)
admin.site.register(Post)
admin.site.register(Section)
