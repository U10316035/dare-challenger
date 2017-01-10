#!/usr/bin/python
#coding:utf-8
from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User
import django.utils.timezone as timezone
# from datetime import datetime
import datetime

# Create your models here.
#class Post(models.Model):
#	text = models.CharField(max_length=30)

class UserData(models.Model):
	username = models.CharField(max_length=20,default="")
	password = models.CharField(max_length=30,default="")
	email = models.EmailField(max_length=100,default="")

class challengeData(models.Model):
	#id = models.AutoField(primary_key=True)
	#urlnumber = models.CharField(max_length=20,default="")
	urlnumber = models.AutoField(primary_key=True)
	urlnum = models.CharField(max_length=20,default="")
	username = models.CharField(max_length=20,default="")
	title = models.CharField(max_length=20,default="")
	detail = models.TextField(max_length=200,default="",null=True)
	stTime = models.DateTimeField(default=timezone.now,editable=True)
	# startTime = models.CharField(max_length=50,default="")
	endTime = models.PositiveIntegerField(default=0)
	mancount = models.PositiveIntegerField(default=0)
	permission = models.CharField(max_length=50,default="")
	joincount = models.PositiveIntegerField(default=0)
	#timeobject


class detail(models.Model):
	urlnumber = models.CharField(max_length=20,default="")
	username = models.CharField(max_length=20,default="")
	title = models.CharField(max_length=20,default="")
	detail = models.CharField(max_length=200,default="")
	video = models.CharField(max_length=300,default="")
	startTime = models.DateTimeField(default=timezone.now,editable=True)
	endTime = models.CharField(max_length=50,default="")
	mancount = models.PositiveIntegerField(default=0)
	isFinish = models.BooleanField(default=False)
	videopic = models.CharField(max_length=300,default="")

	#whichChallenge = models.ForeignKey(challenge,related_name='proofofchallenge')
	#data = detail.objects.create(urlnumber='0',username='dare',title='ice challenge',detail='an ice challenge',whichChallenge=0)

class detailResponse(models.Model):
	urlnumber = models.CharField(max_length=20,default="")
	username = models.CharField(max_length=20,default="")
	response = models.CharField(max_length=100,default="")
	postTime = models.CharField(max_length=20,default="")
	whichDetail = models.ForeignKey(detail)
	detailowner = models.CharField(max_length=20,default="")
