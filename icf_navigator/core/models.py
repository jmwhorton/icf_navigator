from django.db import models

class ConsentForm(models.Model):
    study_name = models.CharField(max_length=500)

class Question(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    order = models.FloatField(unique=True)
