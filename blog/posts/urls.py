# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from blog.posts.views import PostListView, PostDetailView, CommentListView, CommentCreate


urlpatterns = [
    url(r'^$', PostListView.as_view(), name='post-list'),
    url(r'posts/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'comments/(?P<post_pk>\d+)/$',
        CommentListView.as_view(), name='comment-list'),
    url(r'comment/add/(?P<post_pk>\d+)/$', CommentCreate.as_view(), name='comment-add'),
]
