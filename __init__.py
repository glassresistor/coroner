import os
import json
import pickle
import paramiko
import MySQLdb.cursors

import local_settings as settings
from sqlalchemy import *
from scp import SCPClient

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(settings.REMOTE_SERVER)
scp = SCPClient(ssh.get_transport())

def rebuild_engine():
    cursor = MySQLdb.cursors.SSCursor
    engine = create_engine(settings.MYSQL_CONNECTION_STRING, encoding='latin-1',
        connect_args={'cursorclass':cursor})
    connection = engine.connect()
    return (engine, connection, cursor)

"""
meta = MetaData()
meta.reflect(bind=engine)
meta = pickle.load(open('meta.pickle'))
for (such_meta, very_wow) in meta.tables.items():
    setattr(__import__(__name__), such_meta, very_wow)
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

def export_to_json_files(ctype, select, index_id, on_each):
    (engine, connection, cursor) = rebuild_engine()
    articles = connection.execution_options(
        stream_results=True).execute(select % index_id)
    try:
        for article in articles:
            if article:
                index_id = article.nid
                path = os.path.join('.', 'cached', ctype, str(article.nid))
                print path
                print article.nid
                if not os.path.exists(path):
                    os.makedirs(path)
                path = os.path.join(path, '%s.orig' % article.vid)
                json.dump(dict(article), open(path+'.json', 'w'), ensure_ascii=False, sort_keys=True, indent=4)
                on_each(article, path, scp)
    except Exception, e:
        print e
        articles.close()
        connection.close()
        export_to_json_files(ctype, select, index_id, on_each)

def build_articles(index_id=0):
    select = """
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

    master_image_file.filename as master_image_filename,
    master_image_file.filepath as master_image_filepath

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
    where article.nid >= %s
    order by article.nid
    """
    def copy_master_image(article, path, scp): 
        if article.master_image_filepath:
            from_path = os.path.join(settings.REMOTE_FILES, article.master_image_filepath[6:])
            index_id = article.nid
            try:
                scp.get(from_path,
                    path+'.master_image.'+article.master_image_filename)
            except Exception, e:
                print e
    export_to_json_files('articles', select, index_id, copy_master_image)


def build_authors():
    select = """
    select
    author.nid as nid,
    author.vid as vid,
    node.title as full_name,
    author.field_author_title_value as title,
    author.field_contrib_bio_value as data,
    author.field_author_bio_value as short_bio,
    author.field_author_bio_short_value as end_of_article_bio,
    author.field_twitter_user_value as twitter,
    files.filename as photograph_filename

    from content_type_author as author
    left join node on node.nid = author.nid and node.vid = author.vid
    left join files on author.field_photo_fid = files.fid
    """
    articles = connection.execution_options(stream_results=True).execute(select)
    def copy_photo(article, path):
        try:
            scp.get(os.path.join(settings.REMOTE_FILES, 'photo', article.photograph_filename),
            path+'.'+article.photograph_filename)
        except Exception, e:
            print article.photograph_filename
    export_to_json_files('authors', articles, copy_photo)
