from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta, time
from .models import Post, RawPost, Source, ScoredPost
from .forms import PostLike
from django.contrib import messages
from django.core.paginator import Paginator

#these are for scraping
from lxml import html
from urllib.parse import urlparse
import requests
import shelve
import sys
import feedparser
import ssl 

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
	paginator = Paginator(posts, 9)
	page = request.GET.get('page',1)
	try:
		pagePosts = paginator.page(page)
	except PageNotAnInteger:
		pagePosts = paginator.page(1)
	except EmptyPage:
		pagePosts = paginator.page(paginator.num_pages)
	return render(request, 'feed/post_list.html', {'posts': pagePosts})

def post_filtered(request, group):
	posts = Post.objects.filter(sources__group__name=group).order_by('-created_date')
	paginator = Paginator(posts, 9)
	page = request.GET.get('page',1)
	try:
		pagePosts = paginator.page(page)
	except PageNotAnInteger:
		pagePosts = paginator.page(1)
	except EmptyPage:
		pagePosts = paginator.page(paginator.num_pages)
	return render(request, 'feed/post_list.html', {'posts': pagePosts})

def refresh_posts(request):
	scorePosts(1)
	makePosts(1)
	#posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
	messages.success(request, 'Posts refreshed!')
	return redirect('post_list')

def scorePosts(user):
	yesterday = timezone.now().date() - timedelta(1)
	rawPosts = RawPost.objects.all()  #need to maybe just make it yesterday, not today
	for rawPost in rawPosts:
		try:
			#if we're already scoring it, increment the existing score
			existing = ScoredPost.objects.get(link=rawPost.link)
			if rawPost.source not in existing.sources.all():    #if we've already got it, just ignore
				existing.score += rawPost.source.score
				existing.sources.add(rawPost.source.id)  #add the source
				existing.save()
		except ScoredPost.DoesNotExist:
			#otherwise make a new scoredPost and increment the score
			newScoredPost = ScoredPost(
				author = rawPost.author,
				link = rawPost.link,
				postType = rawPost.postType,
				score = rawPost.source.score,
				created_date = rawPost.created_date
				)
			newScoredPost.save()
			#add the source relationship after saving the scoredPost
			newScoredPost.sources.add(rawPost.source.id)
			newScoredPost.save()


def makePosts(user):
	#look at our sources right now to determine the threshold
	sources = Source.objects.all()
	totalScore = sources.aggregate(Sum('score'))['score__sum']  #it makes a dict, gotta access the value
	sourceCount = sources.count()
	threshold = totalScore/sourceCount
	yesterday = timezone.now().date() - timedelta(1)

	#grab posts that meet the threshold
	scoredPosts = ScoredPost.objects.filter(score__gte=threshold)
	for p in scoredPosts:
		Post.create(p)

def post_like(request, pk):
	post = Post.objects.get(pk=pk)
	if request.method == "POST":
		form = PostLike(request.POST, instance=post)
		if form.is_valid():
			post = form.save()
			return redirect('post_like', pk=post.pk)
	post = Post.objects.get(pk=pk)
	form = PostLike(instance=post)
	return render(request, 'feed/post_detail.html', {'post':post, 'form':form})


##### Here's how we get the vids

def find_youtubes(address):
    """finds any embedded youtube addresses on the page"""
    page = requests.get(address)
    output = set()
    try:
        tree = html.fromstring(page.text)
        sources = tree.xpath('//a/@href')
        for source in sources:
            if "youtube.com" in source:
                parsed = urlparse(str(source))
                output.add(source)
    except html.etree.ParserError:
        pass
    return output
    

def get_sub_pages(mainaddress, domain, allowed_paths):
    """get address of all links from address along allowed paths, in domain"""
    page = requests.get(mainaddress, allow_redirects=False)
    tree = html.fromstring(page.text)
    links = tree.xpath('//attribute::href')
    output = []
    for link in links:
        parsed = urlparse(link)
        path = parsed.path.split('/')
        if (parsed.netloc == domain and len(path) >1 and path[1] in allowed_paths):
            output.append(link)
    return output

def get_rss_links(mainaddress):
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    dd = feedparser.parse(mainaddress)
    output = []
    for d in dd.entries: 
        output.append(d.link)
    return output

def catch_em_all(source):
	links = []
	if source.rssable:
		links += source.get_rss_links()
	if source.name == 'Stereogum':
	    links += get_sub_pages('http://www.stereogum.com','www.stereogum.com',[str(x) for x in range(1920000, 1930000)])
	if source.name == 'Slate':
	    links += get_sub_pages('http://www.slate.com','www.slate.com',['articles', 'blogs'])
	#if source.name == 'Noisey':
	#	noisey = Source.objects.get(name='Noisey')
	#	links = noisey.get_rss_links()
	youtubes = []
	for link in links:
	    youtubes += find_youtubes(link)
	distinct = set()
	for youtube in youtubes:
	    if source.name.lower() not in youtube:    #make sure we're not adding its own channel
	        distinct.add(youtube)
	return distinct

def process_feed(request,group):
	sources = Source.objects.filter(group__name=group)
	for s in sources:
		tubes = []
		tubes += catch_em_all(s)
		RawPost.create_batch(tubes,s)
		messages.success(request, 'Processed {}'.format(s.name))
	return redirect('post_list')   



