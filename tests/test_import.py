import pytest
import os
import json
from importer.utils import create_fixture, componentify

class TestCreateFixtures(object):
    json_example = {
    "model": "mirrors.component",
    "pk": 4,
    "fields": {
         "schema_name": "author",
         "updated_at": "2015-04-29T16:39:32.153Z",
         "content_type": "text/x-markdown",
         "slug": "jane-doe",
         "current_metadata": "{\"name\": \"Jane Doe\", \"email\": \"jdoe@example.com\", \"sortable_name\": \"doe jane\", \"short_bio\": \"I write things about stuff.\", \"position\": \"Reporter\", \"twitter_user\": \"jdoeSF\"}",
         "created_at": "2015-04-29T16:39:32.153Z"
         }
      }
    example_author_payload = json.dumps({
        "data": None,
        "end_of_article_bio": "end of article bio for Jane Doe",
        "full_name": "Jane Doe",
        "img_path": "drum_kevin80x95.jpg",
        "nid": 4,
        "short_bio": "I write things about stuff.",
        "title": "Reporter",
        "twitter": "jdoeSF",
        "vid": 123456
        })

    def setup(self):
        if not os.path.exists('tests/cached/author/0'):
            os.makedirs('tests/cached/author/0')
        with open('tests/cached/author/0/0.orig.json', 'w') as fixture:
            fixture.write(self.example_author_payload)

    def teardown(self):
        pass

    def test_create_no_fixtures(self):
        with pytest.raises(RuntimeError):
            create_fixture('foo', 'tests')

    def test_create_fixture_file(self):
        fixture_path = os.path.join(os.curdir, 'tests', 'fixtures', 'mirrors_legacy_author.json')
        create_fixture('author', 'tests')
        assert os.path.isfile(fixture_path) == True

    def test_format_conversion(self):
        assert componentify(self.example_author_payload) == self.json_example
