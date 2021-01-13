from django import forms
from .models import Class, ClassConversation, ClassConversationTopic, ClassConversationPost, Meetup, MeetupConversation, MeetupConversationPost, MeetupConversationTopic
import datetime as dt


class NewClassForm(forms.ModelForm):
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
    ), max_length = 500, help_text = "Ex: Professor Adam Apple", label = "Professor")

    start_time = forms.TimeField(
    widget = forms.TimeInput(
        attrs = {'rows': 1, 'placeholder': 'Enter the start time of your class here'}
    ), help_text = "Format: 00:00 AM/PM", label="Start Time")

    end_time = forms.TimeField(
    widget = forms.Textarea(
        attrs = {'rows': 1, 'placeholder': 'Enter the start time of your class here'}
    ), help_text = "Format: 00:00 AM/PM", label = "End Time")

    location = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 2, 'placeholder': 'Put the location of the class here'}
    ), max_length = 20000, help_text = "Ex: Pomerene Hall 250", label="Location")

    onMonday = forms.BooleanField(widget = forms.CheckboxInput(), required=False, label="Monday")
    onTuesday = forms.BooleanField(widget = forms.CheckboxInput(), required=False, label = "Tuesday")
    onWednesday = forms.BooleanField(widget = forms.CheckboxInput(), required=False, label = "Wednesday")
    onThursday = forms.BooleanField(widget = forms.CheckboxInput(), required=False, label="Thursday")
    onFriday = forms.BooleanField(widget = forms.CheckboxInput(), required=False, label="Friday")

    class Meta:
        model = Class
        fields = ['dept', 'courseNumber', 'courseName', 'professor', 'start_time', 'end_time', 'location', 'onMonday', 'onTuesday', 'onWednesday', 'onThursday', 'onFriday']

class NewTopicForm(forms.ModelForm):
    subject = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1, 'placeholder': 'Put the subject of the topic here'}),
    max_length = 255, help_text = "Ex: Questions about Assignment 11", label="Subject")

    description = forms.CharField(
    widget=forms.Textarea(attrs={'rows': 6, 'placeholder': "Put a more detailed description of the topic here, if you'd like"}), max_length=20000, label="Description")

    class Meta:
        model = ClassConversationTopic
        fields = ['subject', 'description']

class ClassPostForm(forms.ModelForm):
    message = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 5, 'placeholder': 'Put your reply here'}),
    max_length = 4000, help_text="Max length is 4000 characters", label="Message")

    class Meta:
        model = ClassConversationPost
        fields = ['message']

class NewMeetupForm(forms.ModelForm):
    title = forms.CharField(
    widget = forms.Textarea(attrs = {'rows': 1, 'placeholder': 'Put a short name for your meetup here'}),
    max_length = 25, help_text="Ex: Lunch @ Scott")

    description = forms.CharField(widget = forms.Textarea(attrs = {'rows': 5, 'placeholder': "Put a description of your meetup here if you'd like"}))


    start_time = forms.TimeField(
    widget = forms.TimeInput(
        attrs = {'rows': 1, 'placeholder': 'Enter the start time of your meetup here'}
    ), help_text = "Format: 00:00 AM/PM")

    end_time = forms.TimeField(
    widget = forms.Textarea(
        attrs = {'rows': 1, 'placeholder': 'Enter the start time of your meetup here'}
    ), help_text = "Format: 00:00 AM/PM")

    location = forms.CharField(
    widget = forms.Textarea(
        attrs={'rows': 1, 'placeholder': "Ex: Scott Traditions"}),
    max_length = 20000)

    onMonday = forms.BooleanField(widget = forms.CheckboxInput(), required=False)
    onTuesday = forms.BooleanField(widget = forms.CheckboxInput(), required=False)
    onWednesday = forms.BooleanField(widget = forms.CheckboxInput(), required=False)
    onThursday = forms.BooleanField(widget = forms.CheckboxInput(), required=False)
    onFriday = forms.BooleanField(widget = forms.CheckboxInput(), required=False)
    onSaturday = forms.BooleanField(widget = forms.CheckboxInput(), required=False)
    onSunday = forms.BooleanField(widget = forms.CheckboxInput(), required=False)

    class Meta:
        model = Meetup
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 'onMonday', 'onTuesday', 'onWednesday', 'onThursday', 'onFriday', 'onSaturday', 'onSunday']

class NewMeetupTopicForm(forms.ModelForm):
    subject = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 1, 'placeholder': 'Put title of the topic here'}),
        max_length = 20)

    description = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 5, 'placeholder': 'Put your first post here'}),
        max_length = 20000)

    class Meta:
        model = MeetupConversationTopic
        fields = ['subject', 'description']

class MeetupPostForm(forms.ModelForm):
    message = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 5, 'placeholder': 'Put your reply here'}),
    max_length = 4000, help_text="Max length is 4000 characters")

    class Meta:
        model = MeetupConversationPost
        fields = ['message']
