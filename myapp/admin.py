from django.contrib import admin

from .models import Profile,ChatMessage,Post

admin.site.register(Profile)
admin.site.register(ChatMessage)
admin.site.register(Post)