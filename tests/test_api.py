from unittest import TestCase

import json
import os

from euring.config import API_DIR


class TestApi(TestCase):
    def test_fields(self):
        with open(os.path.join(API_DIR, "fields.json")) as fields_file:
            unique_names = []
            unique_slugs = []
            unique_indexes = []
            fields = json.load(fields_file)
            for field in fields:
                self.assertFalse(field["name"] in unique_names)
                unique_names.append((field["name"]))
                self.assertFalse(field["slug"] in unique_slugs)
                unique_slugs.append((field["slug"]))
                self.assertFalse(field["index"] in unique_indexes)
                unique_indexes.append((field["index"]))