# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Post, Comment
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.core.urlresolvers import reverse


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


class CommentListView(ListView):
    model = Comment

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        unfiltered_queryset = super(CommentListView, self).get_queryset()
        return unfiltered_queryset.filter(post=post).values()

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(list(context['object_list']),
                            safe=False, **response_kwargs)


class CommentCreate(CreateView):
    model = Comment
    fields = ['body', 'post']

    def get_initial(self):
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        return {'post': post}

    def get_success_url(self):
        return reverse('post-detail',
                       args=(self.kwargs['post_pk'],))
