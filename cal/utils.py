from .models import Meetup, Class, ClassConversation, ClassConversationTopic, ClassConversationPost, MeetupConversation, MeetupConversationTopic, MeetupConversationPost

def MeetupTimeSort(day, meetups):
    todayMeetups = []

    for meetup in meetups:
        if day == 1:
            if meetup.onMonday == True:
                todayMeetups.append(meetup)
        if day == 2:
            if meetup.onTuesday == True:
                todayMeetups.append(meetup)
        if day == 3:
            if meetup.onWednesday == True:
                todayMeetups.append(meetup)
        if day == 4:
            if meetup.onThursday == True:
                todayMeetups.append(meetup)
        if day == 5:
            if meetup.onFriday == True:
                todayMeetups.append(meetup)
        if day == 6:
            if meetup.onSaturday == True:
                todayMeetups.append(meetup)

        if day == 7:
            if meetup.onSunday == True:
                todayMeetups.append(meetup)
    n = len(todayMeetups)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if todayMeetups[j].start_time > todayMeetups[j+1].start_time:
                todayMeetups[j], todayMeetups[j+1] = todayMeetups[j+1], todayMeetups[j]
    return todayMeetups


def ClassTimeSort(day, classes):
    todayClasses = []

    for Class in classes:
        if day == 1:
            if Class.onMonday == True:
                todayClasses.append(Class)
        if day == 2:
            if Class.onTuesday == True:
                todayClasses.append(Class)
        if day == 3:
            if Class.onWednesday == True:
                todayClasses.append(Class)
        if day == 4:
            if Class.onThursday == True:
                todayClasses.append(Class)
        if day == 5:
            if Class.onFriday == True:
                todayClasses.append(Class)
        if day == 6:
            if Class.onSaturday == True:
                todayClasses.append(Class)

        if day == 7:
            if Class.onSunday == True:
                todayClasses.append(Class)
    n = len(todayClasses)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if todayClasses[j].start_time > todayClasses[j+1].start_time:
                todayClasses[j], todayClasses[j+1] = todayClasses[j+1], todayClasses[j]
    return todayClasses
