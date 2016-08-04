#!/usr/bin/env python3

from collections import namedtuple

import feedparser
import requests

FEED_INDEX = 'http://www.mrmoneymustache.com/feed/?order=ASC&paged=%d'

Post = namedtuple('Post', ['title', 'author', 'content'])


def get_posts():
    page_number = 1

    while True:
        url = FEED_INDEX % page_number
        response = requests.get(url)

        if response.status_code not in (200, 301):
            break

        data = feedparser.parse(response.content)

        for post in data.entries:
            yield Post(post.title, post.author, post.content[0].value)

        page_number += 1
