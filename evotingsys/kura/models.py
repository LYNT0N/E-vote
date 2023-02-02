from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    year_of_study = models.PositiveSmallIntegerField(default=1)
    faculty = models.CharField(max_length=100)

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.voter_id = self.user.username + '_' + str(self.user.id)
        super(Voter, self).save(*args, **kwargs)    