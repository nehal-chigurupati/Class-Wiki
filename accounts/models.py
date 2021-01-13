from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from markdown import markdown
from django.utils.html import mark_safe

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete = models.CASCADE)
    recipient = models.ForeignKey(User, related_name = "received_messages", on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length = 255)
    message = models.CharField(max_length=400000)
    sent_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True)
    viewed_by_recipient = models.BooleanField(default=False)
    new_reply_from_recipient = models.BooleanField(default=False)
    new_reply_from_sender = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    class Meta:
        ordering = ['last_updated']

class message_reply(models.Model):
    original_message = models.ForeignKey(Message, related_name='replies', on_delete = models.CASCADE)
    sender = models.ForeignKey(User, related_name='message_replies', on_delete = models.CASCADE, null=True)
    message = models.TextField(max_length=40000000)
    sent_at = models.DateTimeField(auto_now_add=True)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    class Meta:
        ordering = ['sent_at']

class search_query(models.Model):
    query_string = models.CharField(max_length = 10000000000000)
    user = models.ForeignKey(User, related_name = 'searches', on_delete=models.CASCADE)
    queried_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query_string


class user_profile(models.Model):
    user = models.ForeignKey(User, related_name = 'profile', on_delete=models.CASCADE)
    biography = models.CharField(max_length = 10000000, null=True, default = "")
    dorm = models.CharField(max_length = 10000000, null=True, default="")
    phone_number = models.CharField(max_length = 14, null=True, default="")
    contact_email = models.CharField(max_length = 10000000, null=True, default = "")
    first_name = models.CharField(max_length = 100000000, null=True, default="")
    last_name = models.CharField(max_length = 100000000, null=True, default="")

    def get_biography_as_markdown(self):
        return mark_safe(markdown(self.biography, safe_mode='escape'))

    def get_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def __str__(self):
        return str(self.user)

class Announcement(models.Model):
    content = models.CharField(max_length = 10000, null=True, default="")
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)

    class Meta:
        ordering = ['posted_at']

    def get_three_most_recent_announcements():
        if len(Announcement.objects.all()) > 3:
            return Announcement.objects.all()[0:3]
        else:
            return Announcement.objects.all()
