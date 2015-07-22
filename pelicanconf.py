#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Douglas Land'
SITENAME = u'webuilddevops'
SITEURL = 'http://webuilddevops.com'
COVER_IMG_URL = 'http://webuilddevops.com/images/snake-40427_640.png'
PROFILE_IMAGE_URL = 'http://webuilddevops.com/images/snake-40427_640.png'
TAGLINE = 'We build devops'

PATH = 'content'
STATIC_PATHS = ['images']

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
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
    ('user', 'https://webuilddevops.com/pages/about.html'),
    ('book', 'https://webuilddevops.com/pages/resources.html'),
    ('twitter-square', 'https://twitter.com/webuilddevops'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGINS = [
    'pelican_youtube',
    'pelican_vimeo',
    'pelican_slideshare',
]
