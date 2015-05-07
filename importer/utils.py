import os
import json
from datetime import datetime
from glob import glob
from unidecode import unidecode
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
            "email": data_dump["email"],
            "sortable_name": sortified_name(data_dump["full_name"], data_dump["last_name"]),
            "short_bio": data_dump["short_bio"],
            "position": data_dump["title"],
            "twitter_user": data_dump["twitter"]
            }
    fields_dict = {
         "schema_name": "author",
         "updated_at": datetime.today().isoformat(),
         "content_type": "text/x-markdown",
         "slug": slugify(data_dump["full_name"]),
         "current_metadata": metadata_dict,
         "created_at": data_dump["created_at"]
         }
    entry_dict = {
        "model": "mirrors.component",
        "pk": data_dump["nid"],
        "fields": fields_dict
        }
    return json.dumps(entry_dict)

def sortified_name(full_name, last_name):
    stop = full_name.rfind(last_name)
    return "{} {}".format(last_name.lower(), full_name[0:stop].strip().lower())

def slugify(full_name):
    return unidecode(full_name).replace(' ', '-').lower()
