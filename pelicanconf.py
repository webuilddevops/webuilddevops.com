#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Douglas Land'
SITENAME = u'webuilddevops'
SITEURL = 'https://webuilddevops.com'
COVER_IMG_URL = 'images/snake-40427_640.png'
PROFILE_IMAGE_URL = 'images/snake-40427_640.png'
TAGLINE = 'We build devops'

PATH = 'content'
STATIC_PATHS = ['images']

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('user', 'pages/about.html'),
    ('book', 'pages/resources.html'),
    ('twitter-square', 'https://twitter.com/webuilddevops'),
    ('rss-square', 'feeds/all.rss.xml'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

PLUGINS = [
    'pelican_youtube',
    'pelican_vimeo',
    'pelican_slideshare',
]
