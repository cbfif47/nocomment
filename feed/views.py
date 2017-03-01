from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta, time
from .models import Post, RawPost, Source, ScoredPost
from .forms import PostLike

# Create your views here.
def post_list(request):
	scorePosts(1)
	makePosts(1)
	posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
	return render(request, 'feed/post_list.html', {'posts':posts})

def scorePosts(user):
	yesterday = timezone.now().date() - timedelta(1)
	rawPosts = RawPost.objects.filter(source__author=user,created_date__gte=yesterday)   #need to maybe just make it yesterday, not today
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
				link = rawPost.link,
				name = rawPost.name,
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
	scoredPosts = ScoredPost.objects.filter(author=user,created_date__gte=yesterday,score__gte=threshold)
	for p in scoredPosts:
		#check if we've already posted this one
		existing = Post.objects.filter(link=p.link)
		if not existing:
			#make a list of the post sources, so we can add it later
			postSources = list(s.id for s in p.sources.all())
			newPost = Post(
				author = p.author,
				link = p.link,
				name = p.name,
				postType = 'Video',
				created_date = p.created_date
				)
			newPost.save()
			#add the sources
			newPost.sources.add(*postSources)

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