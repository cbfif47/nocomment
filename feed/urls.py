from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^filtered/(?P<group>[a-z]\w+)/$', views.post_filtered, name='post_filtered'),
	url(r'^post/(?P<pk>\d+)/like$', views.post_like, name='post_like'),
	url(r'^refresh/$', views.refresh_posts, name='refresh_posts'),
	url(r'^processfeed/(?P<group>[a-z]\w+)/$', views.process_feed, name='process_feed'),
]
