# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Model, CharField, TextField, ForeignKey


class Post(Model):
    title = CharField('title', max_length=255, blank=True, null=True)
    body = TextField('body', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def comments_number(self):
        return self.comments.count()

    @property
    def number_of_words_with_doubles(self):
        """
        Calculates the number of words in the body that contain at least
        two consecutive equal characters
        """
        words = self.body.split()
        words_with_doubles_count = 0
        for word in words:
            for char in word[0:len(word) - 1]:
                if char == word[word.index(char) + 1]:
                    words_with_doubles_count += 1
                    break
        return words_with_doubles_count


class Comment(Model):
    body = TextField('body', blank=True, null=True)
    post = ForeignKey(Post, verbose_name='post', related_name='comments')

    def __str__(self):
        return 'comment to post' + self.post.__str__()
