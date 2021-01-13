from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from markdown import markdown
from django.utils.html import mark_safe

from cal.models import Class

class class_wiki(models.Model):
    dept = models.CharField("Department", max_length=4)
    courseNumber = models.CharField("Course Number", max_length = 10)
    courseName = models.CharField("Course Name", max_length=200, blank=True, default="No name given")
    professor = models.CharField("Professor", max_length = 500, blank=True, default="No professor given")
    starter = models.ForeignKey(User, related_name='class_wikis', on_delete=models.CASCADE)
    contributors = models.ManyToManyField(User, related_name = "contributing_wikis", blank=True)
    current_connected_class = models.ForeignKey(Class, related_name='wiki', blank=True, null=True, on_delete = models.CASCADE)
    followers = models.ManyToManyField(User, related_name = "following_wikis", blank=True)
    views = models.PositiveIntegerField(default=0)
    is_reported_duplicate = models.BooleanField(default=False)

    class Meta:
        ordering = ['views']

    def has_connected_class(self):
        return hasattr(self, 'current_connected_class') and self.current_connected_class != None

    def __str__(self):
        return (self.dept + " " + self.courseNumber)

class class_wiki_topic(models.Model):
    subject = models.CharField(max_length = 30, null=True)
    description = models.CharField(max_length = 20000, blank=True, default="No description provided", null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    last_updated = models.DateTimeField(auto_now_add=True, null=True)
    class_wiki_reference = models.ForeignKey(class_wiki, related_name='class_wiki_topics', default='', on_delete=models.CASCADE, null=True)
    starter = models.ForeignKey(User, related_name='class_wiki_topics_created', on_delete=models.CASCADE, null=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.subject

class class_wiki_topic_post(models.Model):
    message = models.TextField(max_length=40000)
    topic = models.ForeignKey(class_wiki_topic, related_name = 'class_wiki_topic_posts', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='user_class_wiki_posts', on_delete = models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name = "+", on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']


    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

class class_wiki_content(models.Model):
    subject = models.CharField(max_length = 50)
    description = models.CharField(max_length = 20000)
    content = models.TextField(max_length = 400000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='user_class_wiki_content', on_delete = models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name = "+", on_delete=models.CASCADE)
    class_wiki = models.ForeignKey(class_wiki, related_name = "content", null=True, on_delete = models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.subject

    def get_content_as_markdown(self):
        return mark_safe(markdown(self.content, safe_mode='escape'))
