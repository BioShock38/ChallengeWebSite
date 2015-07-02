from django.db import models
from django.conf import settings

# Create your models here.
class Simulation(models.Model):
    name = models.CharField(max_length=200,unique=True)
    numero = models.IntegerField(unique=True)
    truth = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    def parse_truth(self,delimiter=','):
        return map(int,self.truth.split(delimiter))

class Submission(models.Model):
    simu = models.ForeignKey(Simulation)
    answer = models.CharField(max_length=400)

    BEGINNER = 'BEG'
    ADVANCE = 'ADV'
    EXPERT = 'EXP'
    LEVEL_CHOICES = [
        (BEGINNER, 'Beginner'),
        (ADVANCE, 'Advance'),
        (EXPERT, 'Expert')
    ]

    level = models.CharField(max_length=3,
                             choices = LEVEL_CHOICES,
                             default = BEGINNER)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    methods = models.CharField(max_length=100,
                               default = 'Random')

    def __str__(self):
        return self.answer

    def parse_answer(self,delimiter=','):
        return map(int,self.answer.split(delimiter))

class Result(models.Model):
    submission = models.ForeignKey(Submission)
    f1score = models.FloatField(verbose_name="F1 Score")

    def __str__(self):
        return str(self.f1score)
