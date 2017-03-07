from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^accounts/login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, name='logout'),
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
	url(r'^password_reset/done$', auth_views.password_reset_done, name='password_reset_done'),
	url(r'^filtered/(?P<group>[a-z]\w+)/$', views.post_filtered, name='post_filtered'),
	url(r'^post/(?P<pk>\d+)/like$', views.post_like, name='post_like'),
	url(r'^refresh/$', views.refresh_posts, name='refresh_posts'),
	url(r'^processfeed/(?P<group>[a-z]\w+)/$', views.process_feed, name='process_feed'),
]
