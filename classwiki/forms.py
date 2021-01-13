from django import forms
from .models import class_wiki, class_wiki_topic, class_wiki_topic_post, class_wiki_content
import datetime as dt
from cal.models import Class

class new_content_form(forms.ModelForm):
    content = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 8, 'placeholder': "Put the full long content here. If you'd like, you can add a link to a file uploaded to Google Drive. Native file sharing is coming soon."}
    ), max_length = 400000)

    subject = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1, 'placeholder': "Put a brief description here"}
    ), max_length = 15)

    description = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 3, 'placeholder': "Put a short description of what's in this post"}
    ), max_length = 500, help_text="Ex: This has a file attachment for the syllabus from AU2020")


    class Meta:
        model = class_wiki_content
        fields = ['content', 'subject', 'description']

class new_class_wiki_topic_form(forms.ModelForm):
    subject = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1, 'placeholder': "Put a brief description here"}
    ), max_length = 30, help_text="Syllabus Question", label="Subject")

    description = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 5, 'placeholder': "Put full content here"}
    ), max_length = 20000, label="Description")

    class Meta:
        model = class_wiki_topic
        fields = ['subject', 'description']

class reply_class_wiki_topic_post_form(forms.ModelForm):
    message = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 8, 'placeholder': "Put the full post here"}
    ), max_length = 40000)

    class Meta:
        model = class_wiki_topic_post
        fields = ['message']

class new_class_wiki_form(forms.ModelForm):
    dept = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1, 'placeholder': "Put department abbreviation here"}
    ), max_length = 15, help_text="Ex: CIS, CSE, ECON", label="Department")

    courseNumber = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1, 'placeholder': 'Put the course number here'}
    ), max_length = 10, help_text="Ex: 1223, 4001.02, 3750", label="Course Number")

    courseName = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1, 'placeholder': 'Put the full name of the course here'}
    ), max_length=200, help_text="Ex: Introduction to Programming in Java", label = "Course Name")

    professor = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1, 'placeholder': 'Put your professor here'}
    ), max_length = 500, help_text = "Ex: Professor Adam Apple", label="Professor")

    current_connected_class = forms.ModelChoiceField(queryset=Class.objects.all(), required=False, label="Connect this wiki to an existing class for SP2021")

    class Meta:
        model = class_wiki
        fields = ('dept', 'courseNumber', 'courseName', 'professor', 'current_connected_class')

class attach_wiki_to_class_form(forms.ModelForm):
    current_connected_class = forms.ModelChoiceField(queryset=Class.objects.all(), required=False, label="Connect this wiki to an existing class for SP2021")

    class Meta:
        model = class_wiki
        fields = ('current_connected_class',)
