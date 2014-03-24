#Tables that start with content


content_field_alternate_dek
content_field_alternate_title
content_field_art_byline
content_field_article_text
content_field_audiovideo_embed
content_field_byline
content_field_byline_override
content_field_css
content_field_defendant_documents
content_field_defendant_offsite_stories
content_field_dek
content_field_front_page_art_byline
content_field_front_page_image
content_field_google_standout
content_field_issue_date
content_field_javascript
content_field_links
content_field_master_image
content_field_master_image_caption
content_field_master_is_smaller
content_field_photo_reference
content_field_promote_date_topstories
content_field_related_articles
content_field_settings_excludefrompromo
content_field_short_body
content_field_slider_relateds
content_field_social_dek
content_field_social_title
content_field_suppress_master_image
content_field_teaser
content_field_top_of_content_art_byline
content_field_top_of_content_caption
content_field_top_of_content_image

content_group
content_group_fields

content_node_field
content_node_field_instance

#Content Types
This is going to be the main entry point for a 
```sql
mysql> describe content_type_article;
+------------------------------+------------------+------+-----+---------+-------+
| Field                        | Type             | Null | Key | Default | Extra |
+------------------------------+------------------+------+-----+---------+-------+
| vid                          | int(10) unsigned | NO   | PRI | 0       |       |
| nid                          | int(10) unsigned | NO   | MUL | 0       |       |
| field_audiovideo_embed_value | longtext         | YES  |     | NULL    |       |
| field_in_depth_value         | longtext         | YES  |     | NULL    |       |
+------------------------------+------------------+------+-----+---------+-------+
4 rows in set (0.00 sec)

mysql> select count(*) from content
Display all 324 possibilities? (y or n)
mysql> select count(*) from content_type_article;
+----------+
| count(*) |
+----------+
|    81617 |
+----------+
1 row in set (0.23 sec)

```

content_type_advpoll_binary
content_type_advpoll_ranking
content_type_article
content_type_audio
content_type_author
content_type_blogpost
content_type_defendant
content_type_external_article_link
content_type_feedback
content_type_image
content_type_link_list
content_type_mediakit
content_type_package
content_type_page
content_type_photoessay
content_type_poll
content_type_pressrelease
content_type_toc
content_type_webform


#Example Query
```sql
select * from content_type_article as article 
  left join node ON article.nid = node.nid and article.nid = node.nid

  left join content_field_dek as dek ON node.nid = dek.nid  and node.vid = dek.vid
  left join content_field_article_text as body ON node.nid = body.nid and node.vid = body.vid 

  left join content_field_alternate_dek as alt_dek ON node.nid = alt_dek.nid and node.vid = alt_dek.vid 
  left join content_field_alternate_title as alt_title ON node.nid = alt_title.nid  and node.vid = alt_title.vid 

  left join content_field_social_dek as social_dek ON node.nid = social_dek.nid  and node.vid = social_dek.vid
  left join content_field_social_title as social_title ON node.nid = social_title.nid  and node.vid = social_title.vid

  left join content_field_master_image as master_image ON node.nid = master_image.nid and node.vid = master_image.vid
  left join files as master_image_file ON master_image.field_master_image_fid = master_image_file.fid

  left join content_field_master_image as master_image ON node.nid = master_image.nid and node.vid = master_image.vid
  left join files as master_image_file ON master_image.field_master_image_fid = master_image_file.fid 

  where node.nid = 243141 and node.vid = 1254046;

