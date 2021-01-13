from django.contrib import admin
from .models import Message, message_reply, user_profile, Announcement

admin.site.register(Message)
admin.site.register(message_reply)
admin.site.register(user_profile)
admin.site.register(Announcement)
