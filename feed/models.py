from django.db import models
from django.utils import timezone
import feedparser
import ssl 
from urllib.parse import urlparse
from lxml import html
import requests
import shelve
import sys
from .getvideos import find_youtubes

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
	group = models.ForeignKey('SourceGroup')
	rssable = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def get_rss_links(self):
	    if hasattr(ssl, '_create_unverified_context'):
	        ssl._create_default_https_context = ssl._create_unverified_context
	    dd = feedparser.parse(self.rss)
	    output = []
	    for d in dd.entries: 
	        output.append(d.link)
	    return output

	def get_sub_pages(self, allowed_paths):
	    """get address of all links from address along allowed paths, in domain"""
	    page = requests.get(self.rss, allow_redirects=False)
	    domain = self.rss[7:]
	    tree = html.fromstring(page.text)
	    links = tree.xpath('//attribute::href')
	    output = []
	    for link in links:
	        parsed = urlparse(link)
	        path = parsed.path.split('/')
	        if (parsed.netloc == domain and len(path) >1 and path[1] in allowed_paths):
	            output.append(link)
	    return output

	def catch_em_all(self):
		links = []
		if self.rssable:
			links = self.get_rss_links()
		if self.name == 'Stereogum':
		    links = self.get_sub_pages([str(x) for x in range(1920000, 1930000)])
		if self.name == 'Slate':
		    links = self.get_sub_pages(['articles', 'blogs'])
		youtubes = []
		for link in links:
		    youtubes += find_youtubes(link)
		distinct = set()
		for youtube in youtubes:
		    if self.name.lower() not in youtube.lower() and 'user' not in youtube.lower():    #make sure we're not adding its own channel
		        distinct.add(youtube)
		return distinct

class SourceGroup(models.Model):
	name = models.TextField(default='New Group')

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
		for link in links:
			existing = RawPost.objects.filter(link=link.lower(), source=source)
			if not existing:
				newRaw = RawPost(
					author = source.author,
					source = source,
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
	

