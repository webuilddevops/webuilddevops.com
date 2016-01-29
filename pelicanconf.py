#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Douglas Land'
SITENAME = u'webuilddevops'
#SITEURL = 'https://webuilddevops.com'
SITEURL = 'http://localhost:8000'
COVER_IMG_URL = 'https://webuilddevops.com/images/snake-40427_640.png'
PROFILE_IMAGE_URL = 'https://webuilddevops.com/images/snake-40427_640.png'
TAGLINE = 'We build DevOps'

PATH = 'content'
STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico', 'extra/apple-touch-icon-precomposed.png', 'extra/apple-touch-icon.png']

#TEMPLATE_PAGES = {'pages/resources/vim.html': 'resources/vim.html', 'extras/search.html': 'search.html'}

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/apple-touch-icon-precomposed.png': {'path': 'apple-touch-icon-precomposed.png'},
    'extra/apple-touch-icon.png': {'path': 'apple-touch-icon.png'},
}

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_RSS = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DISPLAY_CATEGORIES_ON_MENU = True
# Blogroll
#MENUITEMS = (('Pelican', 'http://getpelican.com/'),
OFF = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('user', 'https://webuilddevops.com/pages/about.html'),
    ('book', 'https://webuilddevops.com/pages/resources.html'),
    ('twitter-square', 'https://twitter.com/webuilddevops'),
    ('rss-square', 'https://webuilddevops.com/feeds/all.atom.xml'),
    ('search', 'https://webuilddevops.com/search.html'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = False

PLUGINS = [
    'pelican_youtube',
    'pelican_vimeo',
    'pelican_slideshare',
    'tipue_search',
]

THEME = "pure"
#THEME = "plumage"

TIPUE_SEARCH = True

DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'authors', 'archives', 'search'))
