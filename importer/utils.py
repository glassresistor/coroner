import os
import json
from glob import glob
# load n files from x location
# - get count of all files of component type Y
# - find or create file settings.mirrors_dir / fixtures / mirrors_legacy_ Y .json
#   - add to settings

def create_fixture(component_type, current_path):
    fixture_path = os.path.join(current_path, 'fixtures')
    # create directory if it doesn't exist
    if not os.path.exists(fixture_path):
        os.mkdir(fixture_path)
    fixture = open(os.path.join(fixture_path, 'mirrors_legacy_%s.json' % component_type), "a")
    glob_path = os.path.join(current_path, 'cached', component_type, '*', '*.orig.json')
    print glob_path
    files = glob(glob_path)
    if not files:
        raise RuntimeError("No files to process")
    for fil in files:
        with open(fil) as f:
            fixture.write(f.read())
    fixture.close()
    return True

def componentify(data_dump):
    data_dump = json.loads(data_dump)
    metadata_dict = {
            "name": data_dump["full_name"],
            "email": "fixme",
            "sortable_name": "fixme",
            "short_bio": data_dump["short_bio"],
            "position": data_dump["title"],
            "twitter_user": data_dump["twitter"]
            }
    fields_dict = {
         "schema_name": "author",
         "updated_at": "fixme",
         "content_type": "text/x-markdown",
         "slug": 'fixme',
         "current_metadata": metadata_dict,
         "created_at": "fixme"
         }
    entry_dict = {
        "model": "mirrors.component",
        "pk": data_dump["nid"],
        "fields": fields_dict
        }
    return json.dumps(entry_dict)
