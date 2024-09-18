# jobs/models.py
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    skills = models.TextField()
    link = models.URLField(max_length=500)
    responsibilities = models.TextField(blank=True, null=True)
    salary = models.CharField(max_length=255, blank=True, null=True)