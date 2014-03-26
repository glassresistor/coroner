import os
import json
import pickle
import MySQLdb.cursors

import local_settings as settings
from sqlalchemy import *


engine = create_engine(settings.MYSQL_CONNECTION_STRING, encoding='latin-1',
    connect_args={'cursorclass': MySQLdb.cursors.SSCursor})
connection = engine.connect()

"""
meta = MetaData()
meta.reflect(bind=engine)
"""

meta = pickle.load(open('meta.pickle'))
for (such_meta, very_wow) in meta.tables.items():
    setattr(__import__(__name__), such_meta, very_wow)

"""
articles_select = select([
    content_type_article.c.nid, 
    node.c.title, 
    content_field_dek.c.field_dek_value, 
    content_field_article_text.c.field_article_text_value, 
    content_field_alternate_dek.c.field_alternate_dek_value,
    content_field_alternate_title.c.field_alternate_title_value,
    content_field_social_dek.c.field_social_dek_value,
    content_field_social_title.c.field_social_title_value, 
    content_field_master_image.c.field_master_image_data,
    files.c.filepath])
"""
articles_select = """
select
  article.nid as nid,
  article.vid as vid,
  body.field_article_text_value as data,
  body.field_article_text_format as data_format,
  
  node.title as title,
  dek.field_dek_value as description, 

  alt_title.field_alternate_title_value as alt_title,
  alt_dek.field_alternate_dek_value as alt_description,

  social_title.field_social_title_value as social_title,
  social_dek.field_social_dek_value as social_description,

  master_image_file.filename

  from content_type_article as article 
  left join node ON article.nid = node.nid and article.vid = node.vid

  left join content_field_dek as dek ON node.nid = dek.nid  and node.vid = dek.vid
  left join content_field_article_text as body ON node.nid = body.nid and node.vid = body.vid 

  left join content_field_alternate_dek as alt_dek ON node.nid = alt_dek.nid and node.vid = alt_dek.vid 
  left join content_field_alternate_title as alt_title ON node.nid = alt_title.nid  and node.vid = alt_title.vid 

  left join content_field_social_dek as social_dek ON node.nid = social_dek.nid  and node.vid = social_dek.vid
  left join content_field_social_title as social_title ON node.nid = social_title.nid  and node.vid = social_title.vid

  left join content_field_master_image as master_image ON node.nid = master_image.nid and node.vid = master_image.vid
  left join files as master_image_file ON master_image.field_master_image_fid = master_image_file.fid
"""
articles = connection.execution_options(stream_results=True).execute(articles_select)


for article in articles:
    path = os.path.join('.', 'articles', str(article.nid))
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, '%s.orig.json' % article.vid)
    print path
    json.dump(dict(article), open(path, 'w'), ensure_ascii=False, sort_keys=True, indent=4)
