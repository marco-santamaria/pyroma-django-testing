# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post']
