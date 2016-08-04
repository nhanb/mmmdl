#!/usr/bin/env python3

from collections import namedtuple
import os

import feedparser
import requests
from ebooklib import epub
from bs4 import BeautifulSoup
import requests_cache
requests_cache.install_cache('cache')


FEED_INDEX = 'http://www.mrmoneymustache.com/feed/?order=ASC&paged=%d'
DIST_PATH = 'dist'
IMG_DIR = 'img'
IMG_PATH = os.path.join(DIST_PATH, IMG_DIR)

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
            print('>', post.title)
            content = replace_images(post.content[0].value)
            yield Post(post.title, post.author, content)

        page_number += 1


def replace_images(post_content):
    '''Download images in post to local filesystem, replace src attribute'''

    soup = BeautifulSoup(post_content, 'lxml')

    for img_tag in soup.find_all('img'):

        # Download
        url = img_tag['src']
        if not url.startswith('http'):
            continue
        print('--- Downloading', url)
        filename = url.split('/')[-1]
        filepath = os.path.join(IMG_PATH, filename)
        if not os.path.isfile(filepath):
            resp = requests.get(url)
            if resp.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(resp.content)

        # Rewrite
        img_tag['src'] = os.path.join('.', IMG_DIR, filename)

    return str(soup)


def generate_epub(posts):
    book = epub.EpubBook()
    book.set_title('Mr. Money Mustache Blog')
    book.set_language('en')
    book.add_author('Mr. Money Mustache')

    spine_list = ['nav']
    toc = []

    for index, post in enumerate(posts):

        # create chapter
        file_name = '%04d.xhtml' % index
        chapter = epub.EpubHtml(title=post.title, file_name=file_name)
        chapter.content = post.content

        # add chapter
        book.add_item(chapter)

        spine_list.append(chapter)
        toc.append(epub.Link(file_name, post.title, file_name))

    # create table of contents
    book.toc = toc

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = spine_list

    # write to the file
    epub.write_epub(os.path.join(DIST_PATH, 'mmm.epub'), book, {})


if __name__ == '__main__':
    if not os.path.isdir(DIST_PATH):
        os.mkdir(DIST_PATH)

    if not os.path.isdir(IMG_PATH):
        os.mkdir(IMG_PATH)

    generate_epub(get_posts())
