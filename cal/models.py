from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from markdown import markdown
from django.utils.html import mark_safe


class Meetup(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length = 20000)
    start_time = models.TimeField()
    end_time = models.TimeField()
    starter = models.ForeignKey(User, related_name='meetups', on_delete=models.CASCADE)
    location = models.CharField(max_length=20000, blank=True, default='')
    onMonday = models.BooleanField(default=False)
    onTuesday = models.BooleanField(default=False)
    onWednesday = models.BooleanField(default=False)
    onThursday = models.BooleanField(default=False)
    onFriday = models.BooleanField(default=False)
    onSaturday = models.BooleanField(default=False)
    onSunday = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=1)
    members = models.ManyToManyField(User)
    maxCapacity = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_time']

class Class(models.Model):
    dept = models.CharField(max_length=4)
    courseNumber = models.CharField(max_length = 10)
    courseName = models.CharField(max_length=200, blank=True, default='No name given')
    professor = models.CharField(max_length = 500, blank=True, default="No professor given")
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=20000, blank=True, default='')
    starter = models.ForeignKey(User, related_name='classes', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    numMembers = models.PositiveIntegerField(default=1)
    members = models.ManyToManyField(User, related_name='classes_is_following')

    onMonday = models.BooleanField(default=False)
    onTuesday = models.BooleanField(default=False)
    onWednesday = models.BooleanField(default=False)
    onThursday = models.BooleanField(default=False)
    onFriday = models.BooleanField(default=False)


    def __str__(self):
        return (self.dept + " " + self.courseNumber)

class ClassConversation(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length = 100)
    classReference = models.ForeignKey(Class, related_name = 'conversation', on_delete=models.CASCADE, default='')


    def __str__(self):
        return self.name

    def get_posts_count(self):
        return ClassConversationPost.objects.filter(ClassConversationTopic__ClassConversation=self).count()

    def get_last_post(self):
        return ClassConversationPost.objects.filter(ClassConversationTopic__ClassConversation=self).order_by('-created_at').first()

class ClassConversationTopic(models.Model):
    subject = models.CharField(max_length = 255)
    description = models.CharField(max_length = 20000, blank=True, default='No description provided')
    last_updated = models.DateTimeField(auto_now_add=True)
    classReference = models.ForeignKey(Class, related_name='class_topics', default='', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='class_topics_created', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['last_updated']

    def __str__(self):
        return self.subject

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

class ClassConversationPost(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(ClassConversationTopic, related_name = 'class_topic_posts', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='user_class_posts', on_delete = models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name = "+", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated_at']


    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

class MeetupConversation(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length = 20000, blank=True, default='')
    meetupReference = models.ForeignKey(Meetup, related_name = 'meetup_conversation', on_delete=models.CASCADE)

    def __str__(self):
        return str(meetupReference.title + " Conversation")



class MeetupConversationTopic(models.Model):
    subject = models.CharField(max_length = 20)
    description = models.CharField(max_length = 20000)
    last_updated = models.DateTimeField(auto_now_add=True)
    meetupReference = models.ForeignKey(Meetup, related_name='meetup_topics', default='', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='meetup_topics_created', on_delete = models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-last_updated']


class MeetupConversationPost(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(MeetupConversationTopic, related_name = 'meetup_topic_posts', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name = 'user_meetup_posts', on_delete = models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name = "+", on_delete = models.CASCADE)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    class Meta:
        ordering = ['-updated_at']
