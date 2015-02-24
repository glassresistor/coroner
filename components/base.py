import os
import json
import paramiko
import MySQLdb.cursors
from sqlalchemy import *
from scp import SCPClient
import logging
import local_settings as settings

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(settings.REMOTE_SERVER)
scp = SCPClient(ssh.get_transport())


def rebuild_engine():
    cursor = MySQLdb.cursors.SSCursor
    engine = create_engine(settings.MYSQL_CONNECTION_STRING,
                           encoding='latin-1',
                           connect_args={'cursorclass': cursor})
    connection = engine.connect()
    return (engine, connection, cursor)


def export_to_json_files(ctype, select, index_id, on_each):
    (engine, connection, cursor) = rebuild_engine()
    articles = connection.execution_options(stream_results=True).\
        execute(select % index_id)
    # import pdb; pdb.set_trace()
    try:
        for article in articles:
            if article:
                index_id = article.nid
                path = os.path.join('.', 'cached', ctype, str(article.nid))
                logging.debug("Path: %s" % path)
                logging.debug("Article: %s" % article.nid)
                if not os.path.exists(path):
                    os.makedirs(path)
                path = os.path.join(path, '%s.orig' % article.vid)
                json.dump(
                    dict(article),
                    open(path+'.json', 'w'),
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4)
                on_each(article, path, scp)
    except Exception, e:
        logging.warning(e)
        articles.close()
        connection.close()
        export_to_json_files(ctype, select, index_id, on_each)


class ArticleBuilder:
    # section = StringSchema(enum=['politics', 'culture', 'environment'])
    # title = StringSchema(required=True)
    # description = StringSchema()
    # alternate_title = StringSchema()
    # alternate_description = StringSchema()
    # social_title = StringSchema()
    # social_description = StringSchema()
    # social_cue = StringSchema() #TODO: should have max length set
    # master_image = Attribute('canon-image', required=True)
    # byline = AttributeList('author', required=True)
    # byline_override = StringSchema()
    # inline_components = AttributeList('canon-image')
    # TODO remove `desc` since it's for debugging.
    query = """
        select
        article.nid as nid,
        article.vid as vid,
        body.field_article_text_value as data,
        body.field_article_text_format as data_format,

        node.title as hed,
        dek.field_dek_value as dek,

        alt_title.field_alternate_title_value as alt_hed,
        alt_dek.field_alternate_dek_value as alt_dek,

        social_title.field_social_title_value as social_hed,
        social_dek.field_social_dek_value as social_dek,

        master_image_file.filename as master_image_filename,
        master_image_file.filepath as master_image_filepath

        from content_type_article as article
        left join node ON article.nid = node.nid and article.vid = node.vid

        LEFT JOIN content_field_dek as dek ON node.nid = dek.nid  and node.vid = dek.vid
        LEFT JOIN content_field_article_text as body ON node.nid = body.nid and node.vid = body.vid

        LEFT JOIN content_field_alternate_dek as alt_dek ON node.nid = alt_dek.nid and node.vid = alt_dek.vid
        LEFT JOIN content_field_alternate_title as alt_title ON node.nid = alt_title.nid  and node.vid = alt_title.vid

        LEFT JOIN content_field_social_dek as social_dek ON node.nid = social_dek.nid  and node.vid = social_dek.vid
        LEFT JOIN content_field_social_title as social_title ON node.nid = social_title.nid  and node.vid = social_title.vid

        LEFT JOIN content_field_master_image as master_image ON node.nid = master_image.nid and node.vid = master_image.vid
        LEFT JOIN files as master_image_file ON master_image.field_master_image_fid = master_image_file.fid
        WHERE article.nid >= %s
        ORDER by article.nid DESC
        """
    def copy_master_image(article, path, scp):
        if article.master_image_filepath:
            from_path = os.path.join(settings.REMOTE_FILES, article.master_image_filepath[6:])
            try:
                scp.get(from_path,
                        path+'.master_image.'+article.master_image_filename)
            except Exception, e:
                print e


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

def build_component(component_type, bounds):
    select = ArticleBuilder.query
    if bounds:
        select += "LIMIT %s" % bounds
    logging.debug(select)
    export_to_json_files('articles', select, 0, ArticleBuilder.copy_master_image)
