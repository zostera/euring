from unittest import TestCase

from euring import __version__


class TestVersion(TestCase):
    def test_is_string(self):
        self.assertEqual(len(__version__.split(".")), 3)
