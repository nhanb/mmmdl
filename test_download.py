import unittest

from download import get_posts

import requests_cache
requests_cache.install_cache('test_cache')


class TestGetFeedIndex(unittest.TestCase):

    def test_get_posts(self):
        posts = [post for post in get_posts()]

        self.assertGreater(len(posts), 460)

        post = posts[0]
        self.assertEqual(post.title, 'Meet Mr. Money Mustache')
        self.assertEqual(post.author, 'Mr. Money Mustache')

        post = posts[425]
        self.assertEqual(post.title, 'Mr. Frugal Toque on Mortgage Freedom'),
        self.assertEqual(post.author, 'Mr. Frugal Toque')


if __name__ == '__main__':
    unittest.main()
