# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import reduce
from string import ascii_lowercase

import django_webtest
import pytest
from blog.posts.models import Comment, Post
from django.core.urlresolvers import reverse
from django_dynamic_fixture import G, N


# Fixtures
@pytest.fixture
def post():
    return G(Post)


@pytest.fixture
def posts():
    return [post() for _ in range(0, 4)]


@pytest.fixture
def comment(post):
    return G(Comment, post=post)


@pytest.fixture
def post_with_comments():
    post = G(Post)
    for _ in range(0, 3):
        comment(post)
    return post


@pytest.fixture
def new_post_2_words_with_doubles():
    return N(Post, body='lorremm ipssum dolor sit')


@pytest.fixture
def new_post_3_words_with_doubles():
    return N(Post, body='lorrem ipssum dollor sit')


# This fixture wraps DjangoTestApp to test views
@pytest.fixture
def app(request):
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    return django_webtest.DjangoTestApp()


# Test for the method comments_number, uses db
@pytest.mark.django_db
def test_post_comments_number(comment):
    assert comment.post.comments_number == 1


# Unit tests for the method number_of_words_with_doubles
def test_post_number_of_words_with_doubles_2(new_post_2_words_with_doubles):
    assert new_post_2_words_with_doubles.number_of_words_with_doubles == 2


def test_post_number_of_words_with_doubles_3(new_post_3_words_with_doubles):
    assert new_post_3_words_with_doubles.number_of_words_with_doubles == 3


def text_with_doubles(w):
    text = reduce(lambda x, y: x + ascii_lowercase[y]*2 + ' ', range(0, w), '')
    return text


# Parametric unit tests for the method number_of_words_with_doubles
@pytest.mark.parametrize(
    'post,words_with_doubles',
    [(N(Post, body=text_with_doubles(w)), w) for w in range(0, 10)]
)
def test_post_number_of_words_with_doubles(post, words_with_doubles):
    assert post.number_of_words_with_doubles == words_with_doubles


# Tests for views using webtest and Beautiful Soup
@pytest.mark.django_db
def test_post_list(app, posts):
    res = app.get(reverse('post-list'))
    assert len(res.html.select('.post')) == 4


@pytest.mark.django_db
def test_post_detail(app, post_with_comments):
    res = app.get(reverse('post-detail', kwargs={'pk': post_with_comments.pk}))
    assert len(res.html.select('.post')) == 1
    assert len(res.html.select('.comment')) == 3


# Test form submission with webtest
@pytest.mark.django_db
def test_add_comment(app, post):
    res = app.get(reverse('comment-add', kwargs={'post_pk': post.pk}))
    assert len(res.html.select('#add-comment-form')) == 1
    form = res.forms['add-comment-form']
    form['body'] = 'Cool!'
    res = form.submit()
    assert res.status_code == 302
    assert res.location.endswith(
        reverse('post-detail', kwargs={'pk': post.pk}))
    res = res.follow()
    assert res.status_code == 200
    assert len(res.html.find_all(text='Cool!')) == 1


# Functional test with splinter for ajax client-side behaviour, uses Firefox
@pytest.mark.selenium
@pytest.mark.django_db
def test_post_list_comments_toggle(live_server, browser, post_with_comments):
    browser.visit(live_server.url + reverse('post-list'))
    post_selector = '#post-' + str(post_with_comments.pk)
    button = browser.find_by_css(
        post_selector + ' .toggle-comments')
    button.click()
    assert browser.is_element_visible_by_css(
        post_selector + ' ul.comments li', wait_time=1)
    button.click()
    assert browser.is_element_not_present_by_css(
        post_selector + ' ul.comments li', wait_time=1)
