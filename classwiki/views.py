from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.views import generic
from datetime import datetime
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime as datetime

from .models import class_wiki, class_wiki_topic, class_wiki_topic_post, class_wiki_content
from .forms import new_content_form, new_class_wiki_topic_form, reply_class_wiki_topic_post_form, new_class_wiki_form, attach_wiki_to_class_form
from accounts.views import email_check
from accounts.models import Message, User

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def report_duplicate(request, pk):

    curr_wiki = get_object_or_404(class_wiki, pk=pk)
    curr_wiki.is_reported_duplicate = True
    curr_wiki.save()

    return render(request, 'report_duplicate.html', {'wiki': curr_wiki})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def see_all_class_wikis(request):
    class_wikis = class_wiki.objects.all()
    return render(request, 'see_all_class_wikis_view.html', {'class_wikis': class_wikis})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def new_class_wiki(request):
    user = request.user
    if request.method == 'POST':
        form = new_class_wiki_form(request.POST)
        if form.is_valid():
            class_wiki = form.save(commit=False)
            class_wiki.starter = user
            class_wiki.save()
            return redirect('class_wiki_details', pk=class_wiki.pk)
    else:
        form = new_class_wiki_form()

    return render(request, 'new_class_wiki_form.html', {'form': form})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def attach_wiki_to_class(request, pk):
    wiki = get_object_or_404(class_wiki, pk=pk)
    if request.method == 'POST':
        form = attach_wiki_to_class_form(request.POST, instance=wiki)
        if form.is_valid():
            form.save()
            return redirect('class_wiki_details', pk=pk)
    else:
        form = attach_wiki_to_class_form()

    return render(request, 'attach_wiki_to_class.html', {'form': form, 'class_wiki': wiki})




@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def class_wiki_details(request, pk):
    selected_class_wiki = get_object_or_404(class_wiki, pk=pk)
    selected_class_wiki.views += 1
    selected_class_wiki.save()

    if request.user in selected_class_wiki.followers.all():
        user_is_a_follower = True
    else:
        user_is_a_follower = False

    topics = []
    topics = selected_class_wiki.class_wiki_topics.all()[0:4]

    if selected_class_wiki.has_connected_class() == True:
        class_wiki_has_current_class = True
    elif selected_class_wiki.has_connected_class() == False:
        class_wiki_has_current_class = False

    return render(request, 'class_wiki_details.html', {'class_wiki': selected_class_wiki, 'user_is_a_follower': user_is_a_follower, 'topics': topics, 'class_wiki_has_current_class': class_wiki_has_current_class, 'connected_class': selected_class_wiki.current_connected_class})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def follow_class_wiki(request, pk):
    selected_class_wiki = get_object_or_404(class_wiki, pk=pk)
    followers = selected_class_wiki.followers.all()
    currUser = request.user

    if currUser not in followers:
        selected_class_wiki.followers.add(currUser)
        return render(request, 'follow_wiki_success.html', {'class_wiki': selected_class_wiki, 'currUser': currUser})
    if currUser in followers:
        error_message = "You already follow this class wiki!"
        return render(request, 'follow_wiki_failure.html', {'class_wiki': selected_class_wiki, 'currUser': currUser, 'error_message': error_message})


@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def unfollow_class_wiki(request, pk):
    selected_class_wiki = get_object_or_404(class_wiki, pk=pk)
    followers = selected_class_wiki.followers.all()
    currUser = request.user

    if currUser not in followers:
        error_message = "You already weren't following this class wiki!"
        return render(request, 'unfollow_wiki_failure.html', {'class_wiki': selected_class_wiki, 'currUser': currUser, 'error_message': error_message})

    if currUser in followers:
        selected_class_wiki.followers.remove(currUser)
        return render(request, 'unfollow_wiki_success.html', {'class_wiki': selected_class_wiki, 'currUser': currUser})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def see_class_wiki_followers(request, pk):
    selected_class_wiki = get_object_or_404(class_wiki, pk=pk)
    return render(request, 'see_class_wiki_followers.html', {'class_wiki': selected_class_wiki})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def new_class_wiki_content_post(request, pk):
    current_class_wiki = get_object_or_404(class_wiki, pk=pk)
    if request.method == 'POST':
        form = new_content_form(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.created_by = request.user
            content.class_wiki = current_class_wiki
            content.save()
            return redirect('class_wiki_details', pk=pk)
    else:
        form = new_content_form()
    return render(request, 'new_class_wiki_content_form.html', {'class_wiki': current_class_wiki, 'form': form})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def class_wiki_topics(request, pk):
    current_class_wiki = get_object_or_404(class_wiki, pk=pk)
    return render(request, 'class_wiki_topics.html', {'class_wiki': current_class_wiki})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def new_class_wiki_topic(request, pk):
    current_class_wiki = get_object_or_404(class_wiki, pk=pk)
    if request.method == 'POST':
        form = new_class_wiki_topic_form(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.starter = request.user
            topic.class_wiki_reference = current_class_wiki
            topic.save()
            return redirect('class_wiki_topics', pk=pk)
    else:
        form = new_class_wiki_topic_form()
    return render(request, 'new_class_wiki_topic.html', {'class_wiki': current_class_wiki, 'form': form})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def class_wiki_topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(class_wiki_topic, class_wiki_reference__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'class_wiki_topic_posts.html', {'topic': topic})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def reply_class_wiki_topic(request, pk, topic_pk):
    topic = get_object_or_404(class_wiki_topic, class_wiki_reference__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = reply_class_wiki_topic_post_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('class_wiki_topic_posts', pk=pk, topic_pk = topic_pk)
    else:
        form = reply_class_wiki_topic_post_form()
    return render(request, 'reply_class_wiki_topic.html', {'topic': topic, 'form': form})


@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def see_class_wiki_content(request, pk, content_pk):
    content = get_object_or_404(class_wiki_content, class_wiki__pk=pk, pk=content_pk)
    return render(request, 'class_wiki_content.html', {'content': content})
