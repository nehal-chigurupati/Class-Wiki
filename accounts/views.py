from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from itertools import chain
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import UpdateView


from .forms import SignUpForm, new_message_form, reply_message_form, search_query_form, setup_profile_form, update_profile_bio, update_profile_dorm, update_profile_phone_number, update_profile_contact_email, update_profile_phone_number, update_profile_name
from .models import Message, message_reply, search_query, user_profile
from cal.models import Class, ClassConversationTopic
from classwiki.models import class_wiki, class_wiki_topic
from .utils import messages_recency_last_updated_sort, messages_reverse_recency_sort

def email_check(user):
    return user.email.endswith('@osu.edu') or user.email == "nehal.chigurupati@gmail.com"


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def not_osu_email(request):
    return render(request, 'not_osu_email_error.html')

@login_required
def profile_setup(request):
    user = request.user
    if request.method == 'POST':
        form = setup_profile_form(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('personal_profile')
    else:
        form = setup_profile_form()
    return render(request, 'profile_setup.html', {'form': form, 'user': user})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def update_bio(request):
    user = request.user
    profile = user.profile.get()
    if request.method == 'POST':
        form = update_profile_bio(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('personal_profile')
    else:
        form = update_profile_bio()
    return render(request, 'update_profile.html', {'form': form, 'user': user, 'field': "bio"})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def update_dorm(request):
    user = request.user
    profile = user.profile.get()
    if request.method == 'POST':
        form = update_profile_dorm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('personal_profile')
    else:
        form = update_profile_dorm()
    return render(request, 'update_profile.html', {'form': form, 'user': user, 'field': "dorm"})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def update_phone_number(request):
    user = request.user
    profile = user.profile.get()
    if request.method == 'POST':
        form = update_profile_phone_number(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('personal_profile')
    else:
        form = update_profile_phone_number()
    return render(request, 'update_profile.html', {'form': form, 'user': user, 'field': "phone number"})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def update_contact_email(request):
    user = request.user
    profile = user.profile.get()
    if request.method == 'POST':
        form = update_profile_contact_email(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('personal_profile')
    else:
        form = update_profile_contact_email()
    return render(request, 'update_profile.html', {'form': form, 'user': user, 'field': "contact email"})


@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def update_name(request):
    user = request.user
    profile = user.profile.get()
    if request.method == 'POST':
        form = update_profile_name(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('personal_profile')
    else:
        form = update_profile_name()
    return render(request, 'update_profile.html', {'form': form, 'user': user, 'field': "name"})











@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def view_personal_profile(request):
    current_user = request.user
    all_profiles = user_profile.objects.all()
    num_profiles = len(all_profiles)
    i = 0
    has_profile = False
    while i < num_profiles:
        if all_profiles[i].user == current_user:
            has_profile = True
            break
        else:
            i = i + 1

    return render(request, 'view_personal_profile.html', {'user': current_user, 'profile': current_user.profile.get(), 'has_profile': has_profile})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def view_profile(request, pk):
    user = request.user
    requested_user = get_object_or_404(User, pk=pk)
    if requested_user == user:
        return redirect('personal_profile')
    else:
        if requested_user.profile.exists():
            profile_exists = True
        elif requested_user.profile.exists() == False:
            profile_exists = False
        return render(request, 'view_profile.html', {'requested_user': requested_user, 'current_user': user, 'has_profile': profile_exists})



@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def see_messages(request):
    user = request.user
    messages_list = list(chain(user.sent_messages.all(), user.received_messages.all()))
    new_messages_list = []
    not_new_messages_list = []

    for message in messages_list:
        if message.sender == user:
            if message.new_reply_from_recipient == True:
                new_messages_list.append(message)
            else:
                not_new_messages_list.append(message)
        if message.recipient == user:
            if message.viewed_by_recipient == False or message.new_reply_from_sender == True:
                new_messages_list.append(message)
            else:
                not_new_messages_list.append(message)

    return render(request, 'see_messages.html', {'new_messages': messages_recency_last_updated_sort(new_messages_list), 'old_messages': messages_recency_last_updated_sort(not_new_messages_list), 'user': user})


@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def new_message(request):
    user = request.user
    if request.method == 'POST':
        form = new_message_form(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.last_updated = datetime.now()
            message.save()
            return redirect('see_messages')
    else:
        form = new_message_form()
    return render(request, 'new_message_form.html', {'form': form})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def open_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    user = request.user
    if message.sender == user or message.recipient == user:
        reply_list = messages_reverse_recency_sort(message.replies.all())
        if message.recipient == user:
            message.viewed_by_recipient = True
            message.new_reply_from_sender = False
        if message.sender == user:
            message.new_reply_from_recipient = False
        message.save()
        return render(request, 'open_message.html', {'message': message, 'replies': reply_list})
    else:
        return render(request, 'unauthorized_message_access.html', {'user': user})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def reply_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    user = request.user
    if message.sender == user or message.recipient == user:
        reply_list = messages_reverse_recency_sort(message.replies.all())
        if request.method == 'POST':
            form = reply_message_form(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.sender = request.user
                reply.original_message = message
                if user == message.sender:
                    message.new_reply_from_sender = True
                else:
                    message.new_reply_from_recipient = True
                message.last_updated = datetime.now()
                message.save()
                reply.save()
                return redirect('open_message', pk=pk)
        else:
            form = reply_message_form()
        return render(request, 'reply_message_form.html', {'form': form, 'message': message, 'replies': reply_list, 'user': user})
    else:
        return render(request, 'unauthorized_message_access.html', {'user': user})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def search_view(request):
    if request.method == 'POST':
        form = search_query_form(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.user = request.user
            search.save()
            return redirect('search_results', pk=search.pk)
    else:
        form = search_query_form()
    return render(request, 'search_query_form.html', {'form': form})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def search_results(request, pk):
    user_search = get_object_or_404(search_query, pk=pk)

    users = list(User.objects.all())
    messages = list(chain(request.user.sent_messages.all(), request.user.received_messages.all()))
    user_replies = []
    for message in messages:
        user_replies = user_replies + list(message.replies.all())
    all_classes = list(Class.objects.all())
    class_topics = list(ClassConversationTopic.objects.all())
    all_class_wikis = list(class_wiki.objects.all())
    class_wiki_topics = list(class_wiki_topic.objects.all())

    user_matches = []
    for user in users:
        if str(user_search.query_string) in str(user.username):
            user_matches.append(user)

    message_matches = []
    for message in messages:
        if str(user_search.query_string) in str(message.subject) or str(user_search.query_string) in str(message.message):
            message_matches.append(message)

    user_reply_matches = []
    for reply in user_replies:
        if str(user_search.query_string) in str(reply.message):
            user_reply_matches.append(reply)

    class_matches = []
    for i in all_classes:
        if str(user_search.query_string) in (str(i.dept) + " " + str(i.courseNumber)) or str(user_search.query_string) in str(i.courseName):
            class_matches.append(i)

    class_topic_matches = []
    for i in class_topics:
        if str(user_search.query_string) in str(i.subject):
            class_topic_matches.append(i)
        if str(user_search.query_string) in str(i.description):
            class_topic_matches.append(i)

    class_wiki_matches = []
    for i in all_class_wikis:
        if str(user_search.query_string) in (str(i.dept) + " " + str(i.courseNumber)):
            class_wiki_matches.append(i)

        if str(user_search.query_string) in (str(i.courseName)):
            class_wiki_matches.append(i)

    class_wiki_topic_matches = []
    for i in class_wiki_topics:
        if str(user_search.query_string) in str(i.subject):
            class_wiki_topic_matches.append(i)

        if str(user_search.query_string) in str(i.description):
            class_wiki_topic_matches.append(i)

    length_of_match_lists = [len(user_matches), len(message_matches), len(user_reply_matches), len(class_matches), len(class_topic_matches), len(class_wiki_matches), len(class_wiki_topic_matches)]

    matches_found = False
    index = 0

    while matches_found != True and index < len(length_of_match_lists):
        if length_of_match_lists[index] != 0:
            matches_found = True
        index = index + 1


    return render(request, 'search_results.html', {'results': [user_matches, message_matches, user_reply_matches, class_matches, class_topic_matches, class_wiki_matches, class_wiki_topic_matches], 'user_search': user_search, 'length_of_match_lists': length_of_match_lists, 'matches_found': matches_found})
