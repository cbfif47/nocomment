from django.db import models
from django.utils import timezone

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	link = models.URLField()
	liked = models.BooleanField(default=False)
	disliked = models.BooleanField(default=False)
	postType = models.TextField(default='Video')
	sources = models.ManyToManyField('source')
	created_date = models.DateTimeField(
		default=timezone.now)

	def __str__(self):
		return self.link[24:]    #parse out just the piece after youtube

	def create(p):
		#check if we've already posted this one
		existing = Post.objects.filter(link=p.link)
		if not existing:
			#make a list of the post sources, so we can add it later
			postSources = list(s.id for s in p.sources.all())
			newPost = Post(
				author = p.author,
				link = p.link,
				postType = 'Video',
				created_date = p.created_date
				)
			newPost.save()
			#add the sources
			newPost.sources.add(*postSources)

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
	postType = models.TextField(default='Video')
	created_date = models.DateTimeField(
		default=timezone.now)

	def __str__(self):
		return self.link[24:]

	def create_batch(links,source):
		linksource = Source.objects.get(name=source)
		for link in links:
			existing = RawPost.objects.filter(link=link, source=linksource)
			if not existing:
				newRaw = RawPost(
					author = linksource.author,
					source = linksource,
					link = link)
				newRaw.save()

class ScoredPost(models.Model):
	author = models.ForeignKey('auth.User')
	sources = models.ManyToManyField('source')
	link = models.URLField()
	postType = models.TextField(default='Video')
	score = models.IntegerField(default=0)
	created_date = models.DateTimeField(
		default=timezone.now)

	def __str__(self):
		return self.link	[24:]	
	