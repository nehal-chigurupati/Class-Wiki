from django.contrib import admin
from classwiki.models import class_wiki, class_wiki_topic, class_wiki_topic_post, class_wiki_content

admin.site.register(class_wiki)
admin.site.register(class_wiki_topic)
admin.site.register(class_wiki_topic_post)
admin.site.register(class_wiki_content)
