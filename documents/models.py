from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    uploaded_by = models.ForeignKey(User, related_name = "files", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='documents/')
    name = models.CharField(max_length = 255)
