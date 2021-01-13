from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Message, message_reply, search_query, user_profile

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class new_message_form(forms.ModelForm):

    recipient = forms.ModelChoiceField(queryset=User.objects.all())

    subject = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 255)

    message = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 5}),
    max_length = 4000000000000
    )

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'message']

class reply_message_form(forms.ModelForm):
    message = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 5}),
    max_length = 40000000)

    class Meta:
        model = message_reply
        fields = ['message']

class search_query_form(forms.ModelForm):
    query_string = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 10000000000000, label="What would you like to search?")

    class Meta:
        model = search_query
        fields = ['query_string']

class setup_profile_form(forms.ModelForm):
    biography = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 5}),
    max_length = 10000000, required=False
    )

    dorm = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 10000000, required=False
    )

    phone_number = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 10000000, required=False
    )

    contact_email = forms.CharField(max_length=254, required=False, widget=forms.EmailInput())

    first_name = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 10000000, required=False, help_text="Put an email other than your OSU email for people to contact you, if you'd like"
    )

    last_name = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 10000000, required=False
    )

    class Meta:
        model = user_profile
        fields = ['biography', 'dorm', 'phone_number', 'contact_email', 'first_name', 'last_name']


class update_profile_bio(forms.ModelForm):
    biography = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 5}),
    max_length = 10000000, required=True)

    class Meta:
        model = user_profile
        fields = ('biography',)

class update_profile_dorm(forms.ModelForm):
    dorm = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 10000000, required=False)

    class Meta:
        model = user_profile
        fields = ('dorm',)

class update_profile_phone_number(forms.ModelForm):
    phone_number = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 10000000, required=False)

    class Meta:
        model = user_profile
        fields = ('phone_number',)

class update_profile_contact_email(forms.ModelForm):
    contact_email = forms.CharField(max_length=254, required=False, widget=forms.EmailInput(), help_text = "Put a non-osu email for people to contact you here, if you'd like!")
    class Meta:
        model = user_profile
        fields = ('contact_email',)

class update_profile_name(forms.ModelForm):
    first_name = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 10000000, required=False)

    last_name = forms.CharField(
    widget = forms.Textarea(
        attrs = {'rows': 1}),
    max_length = 10000000, required=False)

    class Meta:
        model = user_profile
        fields = ('first_name', 'last_name')
