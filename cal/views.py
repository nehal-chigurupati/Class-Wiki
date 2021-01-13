from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.views import generic
from datetime import datetime
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import datetime as datetime
from django.contrib.auth.decorators import user_passes_test

from .models import Meetup, Class, ClassConversation, ClassConversationTopic, ClassConversationPost, MeetupConversation, MeetupConversationTopic, MeetupConversationPost
from .forms import NewClassForm, NewTopicForm, ClassPostForm, NewMeetupForm, NewMeetupTopicForm, MeetupPostForm
from .utils import MeetupTimeSort, ClassTimeSort
from accounts.views import email_check
from classwiki.models import class_wiki

# Create your views here.
@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def weekend_schedule(request):
    raw_meetups = Meetup.objects.all()
    saturday_meetups = []
    saturday_meetups = []
    sunday_meetups = []

    for meetup in raw_meetups:
        if meetup.onSaturday == True:
            saturday_meetups.append(meetup)
        if meetup.onSunday == True:
            sunday_meetups.append(meetup)

    def get_meetups_at_time(inputList, timePeriod):
        outputMeetups = []
        if (timePeriod == 1):
            for i in inputList:
                if i.start_time < datetime.time(12) and i.start_time > datetime.time(0):
                    outputMeetups.append(i)
        if (timePeriod == 2):
            for i in inputList:
                if i.start_time >= datetime.time(12) and i.start_time < datetime.time(17):
                    outputMeetups.append(i)
        if (timePeriod == 3):
            for i in inputList:
                if i.start_time >= datetime.time(17):
                    outputMeetups.append(i)
        return outputMeetups




    return render(request, 'weekend_schedule.html', {'saturday_meetups': saturday_meetups, 'sunday_meetups': sunday_meetups, 'saturday_morning_meetups': get_meetups_at_time(saturday_meetups, 1), 'saturday_afternoon_meetups': get_meetups_at_time(saturday_meetups, 2), 'saturday_evening_meetups': get_meetups_at_time(saturday_meetups, 3), 'sunday_morning_meetups': get_meetups_at_time(sunday_meetups, 1), 'sunday_afternoon_meetups': get_meetups_at_time(sunday_meetups, 2), 'sunday_evening_meetups': get_meetups_at_time(sunday_meetups, 3)})


@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def classes_schedule(request):
    classes = Class.objects.all()
    def get_classes_at_time(timePeriod):
        outputClasses = []
        if (timePeriod == 1):
            for i in classes:
                if i.start_time < datetime.time(12) and i.start_time > datetime.time(0):
                    outputClasses.append(i)
        if (timePeriod == 2):
            for i in classes:
                if i.start_time >= datetime.time(12) and i.start_time < datetime.time(17):
                    outputClasses.append(i)
        if (timePeriod == 3):
            for i in classes:
                if i.start_time >= datetime.time(17):
                    outputClasses.append(i)
        return outputClasses

    return render(request, 'classes_schedule.html', {'morningClasses': get_classes_at_time(1), 'afternoonClasses': get_classes_at_time(2), 'eveningClasses': get_classes_at_time(3)})



@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def squareClassView(request):
    classes = Class.objects.all()
    meetups = Meetup.objects.all()

    def get_classes_at_time(timePeriod):
        outputClasses = []
        if (timePeriod == 1):
            for i in classes:
                if i.start_time < datetime.time(12) and i.start_time > datetime.time(0):
                    outputClasses.append(i)
        if (timePeriod == 2):
            for i in classes:
                if i.start_time >= datetime.time(12) and i.start_time < datetime.time(17):
                    outputClasses.append(i)
        if (timePeriod == 3):
            for i in classes:
                if i.start_time >= datetime.time(17):
                    outputClasses.append(i)
        return outputClasses

    def get_meetups_at_time(timePeriod):
        outputMeetups = []
        if (timePeriod == 1):
            for i in meetups:
                if i.start_time < datetime.time(12) and i.start_time > datetime.time(0):
                    outputMeetups.append(i)
        if (timePeriod == 2):
            for i in meetups:
                if i.start_time >= datetime.time(12) and i.start_time < datetime.time(17):
                    outputMeetups.append(i)
        if (timePeriod == 3):
            for i in meetups:
                if i.start_time >= datetime.time(17):
                    outputMeetups.append(i)
        return outputMeetups

    return render(request, 'squareClassSchedule.html', {'classes': classes, 'meetups': meetups, 'morningClasses': get_classes_at_time(1), 'afternoonClasses': get_classes_at_time(2), 'eveningClasses': get_classes_at_time(3), 'morningMeetups': get_meetups_at_time(1), 'afternoonMeetups': get_meetups_at_time(2), 'eveningMeetups': get_meetups_at_time(3)})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def meetup_day_view(request, dayNum):

    meetups = Meetup.objects.all()
    sortedMeetups = MeetupTimeSort(dayNum, meetups)

    if dayNum == 1:
        day = "Monday"
    elif dayNum == 2:
        day = "Tuesday"
    elif dayNum == 3:
        day = "Wednesday"
    elif dayNum == 4:
        day = "Thursday"
    elif dayNum == 5:
        day = "Friday"
    elif dayNum == 6:
        day = "Saturday"
    elif dayNum == 7:
        day = "Sunday"



    return render(request, 'meetup_day_view.html', {'meetups': sortedMeetups, 'number_meetups': len(sortedMeetups), 'day': day, 'currUser': request.user})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def class_day_view(request, dayNum):
    classes = Class.objects.all()
    sortedClasses = ClassTimeSort(dayNum, classes)

    if dayNum == 1:
        day = "Monday"
    elif dayNum == 2:
        day = "Tuesday"
    elif dayNum == 3:
        day = "Wednesday"
    elif dayNum == 4:
        day = "Thursday"
    elif dayNum == 5:
        day = "Friday"

    return render(request, 'class_day_view.html', {'classes': sortedClasses, 'number_classes': len(sortedClasses), 'day': day, 'currUser': request.user})



@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def class_details(request, pk):
    currClass = get_object_or_404(Class, pk=pk)
    currClass.views += 1
    currClass.save()
    topics = currClass.class_topics.order_by('-last_updated')
    username = request.user.username
    currUser = request.user

    if currUser in currClass.members.all():
        user_is_in_class = True
    else:
        user_is_in_class = False

    attached_wikis = []

    for i in currClass.wiki.all():
        attached_wikis.append(i)


    return render(request, 'class_details.html', {'class': currClass, 'username': username, 'topics': topics, 'user': currUser, 'user_is_in_class': user_is_in_class, 'attached_wikis': attached_wikis})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def meetup_details(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    currUser = request.user
    meetup.views += 1
    meetup.save()
    topics = meetup.meetup_topics.order_by('-last_updated')

    if currUser in meetup.members.all():
        user_is_in_meetup = True
    else:
        user_is_in_meetup = False

    return render(request, 'meetup_details.html', {'meetup': meetup, 'topics': topics, 'user_is_in_meetup': user_is_in_meetup})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def join_meetup(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    currUser = request.user
    numMembers = len(meetup.members.all())
    if (currUser not in meetup.members.all()) and (numMembers < meetup.maxCapacity):
        meetup.members.add(currUser)
        return render(request, 'join_meetup_success.html', {'meetup': meetup, 'currUser': request.user})

    if (currUser in meetup.members.all()) and (numMembers == meetup.maxCapacity):
        errors = str("This meetup is already at max capacity. Nothing to worry about, though - you have already joined it!")
        return render(request, 'join_meetup_failure.html', {'error_message': errors, 'meetup': meetup})

    if (currUser in meetup.members.all()) and (numMembers < meetup.maxCapacity):
        errors = str("You've already joined this meetup!")
        return render(request, 'join_meetup_failure.html', {'error_message': errors, 'meetup': meetup})

    if (currUser not in meetup.members.all()) and (numMembers == meetup.maxCapacity):
        errors = str("Sorry, too many people have already joined this meetup!")
        return render(request, 'join_meetup_failure.html', {'error_message': errors, 'meetup': meetup})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def leave_meetup(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    currUser = request.user

    if (currUser in meetup.members.all()):
        meetup.members.remove(currUser)
        return render(request, 'leave_meetup_success.html', {'meetup': meetup, 'currUser': currUser})

    if (currUser not in meetup.members.all()):
        error_message = "You aren't in this meetup, so you have nothing to worry about!"
        return render(request, 'leave_meetup_failure.html', {'meetup': meetup})

    if (currUser in meetup.members.all()) and (numMembers == meetup.maxCapacity):
        errors = str("This meetup is already at max capacity. Nothing to worry about, though - you have already joined it!")
        return render(request, 'join_meetup_failure.html', {'error_message': errors, 'meetup': meetup})

    if (currUser in meetup.members.all()) and (numMembers < meetup.maxCapacity):
        errors = str("You've already joined this meetup!")
        return render(request, 'join_meetup_failure.html', {'error_message': errors, 'meetup': meetup})

    if (currUser not in meetup.members.all()) and (numMembers == meetup.maxCapacity):
        errors = str("Sorry, too many people have already joined this meetup!")
        return render(request, 'join_meetup_failure.html', {'error_message': errors, 'meetup': meetup})


@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def join_class(request, pk):
    currClass = get_object_or_404(Class, pk=pk)
    currUser = request.user

    if (currUser not in currClass.members.all()):
        currClass.members.add(currUser)
        return render(request, 'join_class_success.html', {'class': currClass, 'currUser': currUser})

    if (currUser in currClass.members.all()):
        errors = str("You have already joined this class!")
        return render(request, 'join_class_failure.html', {'class': currClass, 'error_message': errors})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def leave_class(request, pk):
    currClass = get_object_or_404(Class, pk=pk)
    currUser = request.user

    if currUser in currClass.members.all():
        currClass.members.remove(currUser)
        return render(request, 'leave_class_success.html', {'class': currClass})

    if currUser not in currClass.members.all():
        errors = "You haven't joined this class, so you can't leave it!"
        return render(request, 'leave_class_failure.html', {'class': currClass, 'error_message': errors})


@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def new_class(request):
    if request.method == 'POST':
        form = NewClassForm(request.POST)
        if form.is_valid():
            currClass = form.save(commit=False)
            ClassConversation(
                name=str(currClass.dept + " " + currClass.courseNumber + " conversation"),
                description=str("A discussion about anything involving " + currClass.dept + " " + currClass.courseNumber),
                classReference = currClass
            )
            currClass.starter = request.user
            currClass.save()
            currClass.members.add(request.user)
            currClass.save()
            return redirect('schedule')
    else:
        form = NewClassForm()
    return render(request, 'new_class.html', {'form': form})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def new_meetup(request):
    if request.method == 'POST':
        form = NewMeetupForm(request.POST)
        if form.is_valid():
            meetup = form.save(commit=False)
            MeetupConversation(name=str("Conversation about: " + meetup.title), description="A conversation discussing this event", meetupReference = meetup)
            meetup.starter = request.user
            meetup.members.add(request.user)
            meetup.save()
            return redirect('schedule')
    else:
        form = NewMeetupForm()
    return render(request, 'new_meetup.html', {'form': form})


@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def new_topic(request, pk):
    currClass = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.starter = request.user
            topic.classReference = currClass
            topic.save()
            return redirect('class_details', pk=pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_class_topic.html', {'class': currClass, 'form': form})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def new_meetup_topic(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    if request.method == 'POST':
        form = NewMeetupTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.starter = request.user
            topic.meetupReference = meetup
            topic.save()
            return redirect('meetup_details', pk=pk)
    else:
        form = NewMeetupTopicForm()
    return render(request, 'new_meetup_topic.html', {'meetup': meetup, 'form': form})



@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def class_topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(ClassConversationTopic, classReference__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'class_topic_posts.html', {'topic': topic})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def meetup_topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(MeetupConversationTopic, meetupReference__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'meetup_topic_posts.html', {'topic': topic,'meetup': topic.meetupReference})


@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def reply_class_topic(request, pk, topic_pk):
    topic = get_object_or_404(ClassConversationTopic, classReference__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = ClassPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('class_topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = ClassPostForm()
    return render(request, 'reply_class_topic.html', {'topic': topic, 'form': form})

@login_required
@user_passes_test(email_check, login_url='not_osu_email')
def reply_meetup_topic(request, pk, topic_pk):
    topic = get_object_or_404(MeetupConversationTopic, meetupReference__pk=pk, pk=topic_pk)
    if request.method ==  'POST':
        form = MeetupPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('meetup_topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = MeetupPostForm()
    return render(request, 'reply_meetup_topic.html', {'topic': topic, 'form': form})
