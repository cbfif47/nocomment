from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta, time
from .models import Post, PrePost, Source, ScoredPost

# Create your views here.
def post_list(request):
	makeNewPosts(1)
	posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
	return render(request, 'feed/post_list.html', {'posts':posts})

def makeNewPosts(user):
	yesterday = timezone.now().date() - timedelta(1)
	prePosts = PrePost.objects.filter(source__author=user,created_date__gte=yesterday)   #need to maybe just make it yesterday, not today
	for prePost in prePosts:
		try:
			#if we're already scoring it, increment the existing score
			existing = ScoredPost.objects.get(link=prePost.link)
			existing.score += prePost.source.score
			existing.sources.add(prePost.source.id)  #add the source
			existing.save()
		except ScoredPost.DoesNotExist:
			#otherwise make a new scoredPost and increment the score
			newScoredPost = ScoredPost(
				link = prePost.link,
				name = prePost.name,
				postType = prePost.postType,
				score = prePost.source.score,
				created_date = prePost.created_date
				)
			newScoredPost.save()
			#add the source relationship after saving the scoredPost
			newScoredPost.sources.add(prePost.source.id)
			newScoredPost.save()

	for prePost in prePosts:
		newSource = prePost.source.id
		existing = Post.objects.filter(link=prePost.link)
		if not existing:
			newPost = Post(
				author = prePost.source.author,
				link = prePost.link,
				name = prePost.name,
				created_date = prePost.created_date
				)
			newPost.save()
			newPost.sources.add(newSource)
			newPost.save()