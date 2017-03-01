from django.db import models
from django.utils import timezone

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	link = models.URLField()
	liked = models.BooleanField(default=False)
	disliked = models.BooleanField(default=False)
	postType = models.TextField(default='Video')
	name = models.TextField(default='New Post')
	sources = models.ManyToManyField('source')
	created_date = models.DateTimeField(
		default=timezone.now)

	def __str__(self):
		return self.name

class Source(models.Model):
	author = models.ForeignKey('auth.User')
	rss = models.URLField()
	name = models.TextField(default='New Source')
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.name



class RawPost(models.Model):
	author = models.ForeignKey('auth.User')
	source = models.ForeignKey('source')
	link = models.URLField()
	name = models.TextField(default='')
	postType = models.TextField(default='Video')
	created_date = models.DateTimeField(
		default=timezone.now)

	def __str__(self):
		return self.name

class ScoredPost(models.Model):
	author = models.ForeignKey('auth.User')
	sources = models.ManyToManyField('source')
	link = models.URLField()
	name = models.TextField(default='')
	postType = models.TextField(default='Video')
	score = models.IntegerField(default=0)
	created_date = models.DateTimeField(
		default=timezone.now)

	def __str__(self):
		return self.name		
	