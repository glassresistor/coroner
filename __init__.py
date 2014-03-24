from sqlalchemy import *

from . import local_settings as settings

engine = create_engine(settings.MYSQL_CONNECTION_STRING)
connection = engine.connect()

meta = MetaData()
meta.reflect(bind=engine)
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

articles = connection.execute(articles_select.order_by(node.c.nid).limit(100))
