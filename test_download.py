import unittest
from itertools import islice

from download import get_posts, generate_epub


class TestGetFeedIndex(unittest.TestCase):

    def test_get_posts(self):
        posts = list(get_posts())

        self.assertGreater(len(posts), 460)

        post = posts[0]
        self.assertEqual(post.title, 'Meet Mr. Money Mustache')
        self.assertEqual(post.author, 'Mr. Money Mustache')

        post = posts[425]
        self.assertEqual(post.title, 'Mr. Frugal Toque on Mortgage Freedom'),
        self.assertEqual(post.author, 'Mr. Frugal Toque')

    def test_generate_epub(self):
        # Get first 3 posts as sample
        posts = list(islice(get_posts(), 3))
        generate_epub(posts)

        # how the hell do I test this cleanly???


if __name__ == '__main__':
    unittest.main()
