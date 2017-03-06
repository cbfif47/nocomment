from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta, time
from .models import Post, RawPost, Source, ScoredPost
from .forms import PostLike
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.
def post_list(request):
	posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
	paginator = Paginator(posts, 9)
	page = request.GET.get('page',1)
	try:
		page_posts = paginator.page(page)
	except PageNotAnInteger:
		page_posts = paginator.page(1)
	except EmptyPage:
		page_posts = paginator.page(paginator.num_pages)
	return render(request, 'feed/post_list.html', {'posts': page_posts})

def post_filtered(request, group):
	posts = Post.objects.filter(sources__group__name=group).order_by('-created_date')
	paginator = Paginator(posts, 9)
	page = request.GET.get('page',1)
	try:
		page_posts = paginator.page(page)
	except PageNotAnInteger:
		page_posts = paginator.page(1)
	except EmptyPage:
		page_posts = paginator.page(paginator.num_pages)
	return render(request, 'feed/post_list.html', {'posts': page_posts})

def refresh_posts(request):
	score_posts(1)
	make_posts(1)
	#posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
	messages.success(request, 'Posts refreshed!')
	return redirect('post_list')

def score_posts(user):
	yesterday = timezone.now().date() - timedelta(1)
	raw_posts = RawPost.objects.all()  #need to maybe just make it yesterday, not today
	for raw_post in raw_posts:
		try:
			#if we're already scoring it, increment the existing score
			existing = ScoredPost.objects.get(link=raw_post.link)
			if raw_post.source not in existing.sources.all():    #if we've already got it, just ignore
				existing.score += raw_post.source.score
				existing.sources.add(raw_post.source.id)  #add the source
				existing.save()
		except ScoredPost.DoesNotExist:
			#otherwise make a new scoredPost and increment the score
			new_scored_post = ScoredPost(
				user = raw_post.user,
				link = raw_post.link,
				post_type = raw_post.post_type,
				score = raw_post.source.score,
				created_date = raw_post.created_date
				)
			new_scored_post.save()
			#add the source relationship after saving the scoredPost
			new_scored_post.sources.add(raw_post.source.id)
			new_scored_post.save()

def make_posts(user):
	#look at our sources right now to determine the threshold
	sources = Source.objects.all()
	total_score = sources.aggregate(Sum('score'))['score__sum']  #it makes a dict, gotta access the value
	source_count = sources.count()
	threshold = total_score/source_count
	yesterday = timezone.now().date() - timedelta(1)

	#grab posts that meet the threshold
	scored_posts = ScoredPost.objects.filter(score__gte=threshold)
	for p in scored_posts:
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


def process_feed(request,group):
	sources = Source.objects.filter(group__name=group)
	for s in sources:
		tubes = []
		tubes += s.catch_em_all()
		RawPost.create_batch(tubes,s)
		messages.success(request, 'Processed {}'.format(s.name))
	return redirect('post_list')   



