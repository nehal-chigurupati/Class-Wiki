"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from boards import views
from accounts import views as accounts_views
from cal import views as cal_views
from classwiki import views as wiki_views

urlpatterns = [
    path('', views.home, name='home'),
    path('boards/<int:pk>/', views.board_topics, name='board_topics'),
    path('admin/', admin.site.urls),
    path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),
    path("signup/", accounts_views.signup, name='signup'),
    path('security_not_osu_email/', accounts_views.not_osu_email, name='not_osu_email'),
    path('boards/<int:pk>/topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('schedule/week/', cal_views.classes_schedule, name='schedule'),
    path('schedule/weekend/', cal_views.weekend_schedule, name='weekend_schedule'),
    path('schedule/<int:pk>/', cal_views.class_details, name='class_details'),
    path('schedule/new_class/', cal_views.new_class, name='new_class'),
    path('schedule/<int:pk>/new_topic/', cal_views.new_topic, name='new_class_topic'),
    path('schedule/<int:pk>/topics/<int:topic_pk>/', cal_views.class_topic_posts,name='class_topic_posts'),
    path('schedule/<int:pk>/topics/<int:topic_pk>/reply/', cal_views.reply_class_topic, name='class_reply_topic'),
    path('schedule/new_meetup/', cal_views.new_meetup, name='new_meetup'),
    path('schedule/meetups/<int:pk>/meetup_details', cal_views.meetup_details, name='meetup_details'),
    path('schedule/meetups/<int:pk>/new_meetup_topic', cal_views.new_meetup_topic, name='new_meetup_topic'),
    path('schedule/meetups/<int:pk>/topics/<int:topic_pk>/', cal_views.meetup_topic_posts, name='meetup_topic_posts'),
    path('schedule/meetups/<int:pk>/topics/<int:topic_pk>/reply/', cal_views.reply_meetup_topic, name='reply_meetup_topic'),
    path('schedule/day/<int:dayNum>/meetups/', cal_views.meetup_day_view, name='meetup_day_view'),
    path('schedule/day/<int:dayNum>/classes/', cal_views.class_day_view, name='class_day_view'),
    path('schedule/meetups/<int:pk>/meetup_details/join_meetup/', cal_views.join_meetup, name='join_meetup'),
    path('schedule/meetups/<int:pk>/meetup_details/leave_meetup/', cal_views.leave_meetup, name='leave_meetup'),
    path('schedule/meetups/<int:pk>/class_details/join_class/', cal_views.join_class, name='join_class'),
    path('schedule/meetups/<int:pk>/class_details/leave_class/', cal_views.leave_class, name='leave_class'),
    path('class_wiki/', wiki_views.see_all_class_wikis, name="class_wiki"),
    path('class_wiki/new_class_wiki/', wiki_views.new_class_wiki, name="new_class_wiki"),
    path('class_wiki/<int:pk>/class_wiki_details/', wiki_views.class_wiki_details, name='class_wiki_details'),
    path('class_wiki/<int:pk>/class_wiki_details/follow/', wiki_views.follow_class_wiki, name='follow_class_wiki'),
    path('class_wiki/<int:pk>/class_wiki_details/unfollow/', wiki_views.unfollow_class_wiki, name='unfollow_class_wiki'),
    path('class_wiki/<int:pk>/class_wiki_details/see_all_followers/', wiki_views.see_class_wiki_followers, name='see_class_wiki_followers'),
    path('class_wiki/<int:pk>/class_wiki_details/new_class_wiki_content/', wiki_views.new_class_wiki_content_post, name="new_class_wiki_content"),
    path('class_wiki/<int:pk>/class_wiki_details/class_wiki_topics/', wiki_views.class_wiki_topics, name="class_wiki_topics"),
    path('class_wiki/<int:pk>/class_wiki_details/class_wiki_topics/new_topic/', wiki_views.new_class_wiki_topic, name="new_class_wiki_topic"),
    path('class_wiki/<int:pk>/class_wiki_details/class_wiki_topics/<int:topic_pk>/posts/', wiki_views.class_wiki_topic_posts, name="class_wiki_topic_posts"),
    path('class_wiki/<int:pk>/class_wiki_details/topics/<int:topic_pk>/reply/', wiki_views.reply_class_wiki_topic, name='class_wiki_reply_topic'),
    path('class_wiki/<int:pk>/class_wiki_details/<int:content_pk>/content/', wiki_views.see_class_wiki_content, name='see_class_wiki_content'),
    path('class_wiki/<int:pk>/class_wiki_details/attach_wiki_to_class/', wiki_views.attach_wiki_to_class, name="attach_wiki_to_class"),
    path('account/messages/', accounts_views.see_messages, name='see_messages'),
    path('account/messages/new_message/', accounts_views.new_message, name='new_message'),
    path('account/messages/<int:pk>/open/', accounts_views.open_message, name='open_message'),
    path('account/messages/<int:pk>/reply/', accounts_views.reply_message, name='reply_message'),
    path('search/', accounts_views.search_view, name="search"),
    path('search/<int:pk>/results/', accounts_views.search_results, name="search_results"),
    path('account/profile/setup/', accounts_views.profile_setup, name='profile_setup'),
    path('account/profile/', accounts_views.view_personal_profile, name="personal_profile"),
    path('search/profiles/<int:pk>/view/', accounts_views.view_profile, name="view_profile"),
    path('profile/update_bio', accounts_views.update_bio, name="update_bio"),
    path('profile/update_dorm', accounts_views.update_dorm, name="update_dorm"),
    path('profile/update_phone_number', accounts_views.update_phone_number, name="update_phone_number"),
    path('profile/update_contact_email', accounts_views.update_contact_email, name="update_contact_email"),
    path('profile/update_name', accounts_views.update_name, name="update_name"),
    path('class_wiki/<int:pk>/class_wiki_details/report_as_duplicate/', wiki_views.report_duplicate, name='report_duplicate_wiki'),
    path('account/change_password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='change_password'),
    path('account/change_password/done', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html', email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt'), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]
