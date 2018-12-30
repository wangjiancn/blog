from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length
from blog.models.category import Category
from flask_ckeditor import CKEditorField

from blog.models.tag import Tag


def category_list():
    return Category.query.filter_by()


def tag_list():
    return Tag.query.filter_by()


class ArticleForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(min=5, max=100, message='标题要求5~100字符')])
    body = CKEditorField('新文章', validators=[DataRequired(), Length(min=50, message='文章最少50字符')])
    summary = TextAreaField('摘要', validators=[DataRequired(), Length(min=5, max=200, message='摘要要求5~200字符')])
    category_field = QuerySelectField('分类', query_factory=category_list, get_label='name', allow_blank=True,
                                      blank_text='请选择文章分类', validators=[DataRequired(message='文章分类未选择')])
    submit_post = SubmitField('提交')


class MarkdownForm(ArticleForm):
    body = TextAreaField('文章HTML代码', validators=[DataRequired(), Length(min=50, message='文章最少50字符')])
    markdown = TextAreaField('Markdown源码', validators=[DataRequired(), Length(min=50, message='最好50字符')])
    tags = QuerySelectMultipleField('文章分类', query_factory=tag_list, get_label='name', allow_blank=True,
                                    blank_text='选择文章标签')
