import os
import json
import logging
import MySQLdb.cursors
from sqlalchemy import create_engine
import local_settings as settings
# import paramiko
# from scp import SCPClient


# ssh = paramiko.SSHClient()
# ssh.load_system_host_keys()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(settings.REMOTE_SERVER)
# scp = SCPClient(ssh.get_transport())


def build_component(c_type, number, node_ids):
    if c_type == 'article':
        export_to_json_files(ArticleBuilder(number, node_ids))
    elif c_type =='author':
        export_to_json_files(AuthorBuilder(number, node_ids))
    elif c_type == 'debug':
        debug()
    else:
        return "All?"


class ComponentBuilder(object):
    select = ""
    def __init__(self, bounds, node_ids):
        if node_ids:
            where_clause = "BETWEEN {} AND {}".format(*article_ids)
            self.select = self.select.format(where_clause)
        else:
            self.select = self.select.format(">= 0")
        if bounds and isinstance(bounds[1], int):
            self.select += "LIMIT {}, {}".format(*bounds)

    def ctype(self):
        name_str = self.__class__.__name__
        return name_str[:(len(name_str) - 7)].lower()

    def serialize(self, node):
        return unicodify(dict(node))


class ArticleBuilder(ComponentBuilder):
    select = """
    SELECT
    article.nid as nid, article.vid as vid,
    body.field_article_text_value as data,
    body.field_article_text_format as data_format,
    node.title as title, dek.field_dek_value as description,
    alt_title.field_alternate_title_value as alt_title,
    alt_dek.field_alternate_dek_value as alt_description,
    social_title.field_social_title_value as social_title,
    social_dek.field_social_dek_value as social_description,
    master_image_file.filename as master_image_filename,
    master_image_file.filepath as master_image_filepath,
    GROUP_CONCAT(byline.field_byline_nid) byline_ids

    FROM content_type_article as article

    LEFT JOIN node ON article.nid = node.nid and article.vid = node.vid
    LEFT JOIN content_field_dek as dek ON node.nid = dek.nid  and node.vid = dek.vid
    LEFT JOIN content_field_article_text as body ON node.nid = body.nid and node.vid = body.vid

    LEFT JOIN content_field_alternate_dek as alt_dek ON node.nid = alt_dek.nid and node.vid = alt_dek.vid
    LEFT JOIN content_field_alternate_title as alt_title ON node.nid = alt_title.nid  and node.vid = alt_title.vid

    LEFT JOIN content_field_social_dek as social_dek ON node.nid = social_dek.nid  and node.vid = social_dek.vid
    LEFT JOIN content_field_social_title as social_title ON node.nid = social_title.nid  and node.vid = social_title.vid

    LEFT JOIN content_field_master_image as master_image ON node.nid = master_image.nid and node.vid = master_image.vid
    LEFT JOIN files as master_image_file ON master_image.field_master_image_fid = master_image_file.fid

    LEFT JOIN content_field_byline byline ON node.nid = byline.nid AND node.vid = byline.vid

    WHERE article.nid {}
    GROUP BY article.nid
    """

    def copy_master_image(article, path, scp):
        if article.master_image_filepath:
            from_path = os.path.join(settings.REMOTE_FILES, article.master_image_filepath[6:])
            try:
                scp.get(from_path,
                        path+'.master_image.'+article.master_image_filename)
            except Exception, e:
                print e

    def serialize(self, node):
        article_dict = unicodify(dict(node))
        if article_dict.has_key("byline_ids") and article_dict["byline_ids"] is not None:
            byline_ids = article_dict["byline_ids"].split(',')
            article_dict["byline_ids"] = [int(x) for x in byline_ids]
        return article_dict


class AuthorBuilder(ComponentBuilder):
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

    def copy_photo(article, path):
        try:
            scp.get(os.path.join(settings.REMOTE_FILES, 'photo', article.photograph_filename),
            path+'.'+article.photograph_filename)
        except Exception, e:
            print article.photograph_filename



def rebuild_engine():
    cursor = MySQLdb.cursors.SSCursor
    engine = create_engine(settings.MYSQL_CONNECTION_STRING,
                           encoding='latin-1',
                           connect_args={'cursorclass': cursor})
    connection = engine.connect()
    return (engine, connection, cursor)

def export_to_json_files(builder):
    (engine, connection, cursor) = rebuild_engine()
    nodes = connection.execution_options(
            stream_results=True).execute(
            builder.select)
    for node in nodes:
        if node:
            try:
                path = os.path.join('.', 'cached', builder.ctype(), str(node.nid))
                logging.debug("Path: %s" % path)
                logging.debug("Node: %s" % node.nid)
                if not os.path.exists(path):
                    os.makedirs(path)
                path = os.path.join(path, '%s.orig' % node.vid)
                json.dump(
                    builder.serialize(node),
                    open(path+'.json', 'w'),
                    ensure_ascii=False, sort_keys=True, indent=4)
                # on_each(article, path, scp)
            #except (KeyboardInterrupt, SystemExit):
            #    connection.close()
            except Exception, e:
                logging.warning(e)
                next
                #articles.close()
                #connection.close()
                #export_to_json_files(ctype, select, index_id, on_each)

    connection.close()

def unicodify(dicti):
    for k, value in dicti.iteritems():
        if isinstance(value, str):
            dicti[k] = value.encode('utf-8')
    return dicti

def debug():
    pass
