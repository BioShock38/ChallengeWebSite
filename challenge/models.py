from django.db import models
from django.conf import settings

# Create your models here.
class Challenge(models.Model):
    name = models.CharField(max_length=200,unique=True)
    desc = models.TextField()
    rules = models.TextField()
    evaluation = models.TextField()
    lsimu = models.ManyToManyField('Dataset')
    isover = models.BooleanField(default=False)
    difficulty = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class Dataset(models.Model):
    name = models.CharField(max_length=200,unique=True)
    numero = models.IntegerField(unique=True)
    truth = models.CharField(max_length=4000)
    private = models.BooleanField(default=True)
    maxsubmission = models.IntegerField(default=2)

    def __str__(self):
        return self.name

    def parse_truth(self,delimiter=','):
        return map(int,self.truth.split(delimiter))

class Method(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Submission(models.Model):
    simu = models.ForeignKey(Dataset)
    challenge = models.ForeignKey(Challenge)
    answer = models.CharField(max_length=4000)
    date = models.DateTimeField(auto_now_add=True,blank=True)

    BEGINNER = 'BEG'
    ADVANCE = 'ADV'
    EXPERT = 'EXP'
    LEVEL_CHOICES = [
        (BEGINNER, 'Beginner'),
        (ADVANCE, 'Advanced'),
        (EXPERT, 'Expert')
    ]

    level = models.CharField(max_length=3,
                             choices = LEVEL_CHOICES,
                             default = BEGINNER)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    with_env_variable = models.BooleanField(default=True)
    methods = models.CharField(max_length=400,
                               default = 'Random')
    desc_method = models.TextField(max_length=1000, default = "None")

    def __str__(self):
        return "id={id}, date={date}, user={user}".format(id=self.id,date=self.date,user=self.user)

    def parse_answer(self,delimiter=','):
        return map(int,self.answer.split(delimiter))

class Result(models.Model):
    submission = models.ForeignKey(Submission)
    f1score = models.FloatField(verbose_name="F1 Score")

    def __str__(self):
        return "{id} : {score}".format(id=self.id,score=self.f1score)
