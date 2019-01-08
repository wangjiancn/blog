# coding = utf-8
from elasticsearch_dsl import Search
from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user

from blog import db, cache
from blog.forms.comment import CommentForm
from blog.forms.message import MessageForm
from blog.models.article import Article
from blog.models.category import Category
from blog.models.comment import Comment
from blog.models.message import Message
from blog.models.tag import Tag
from blog.helpers.elastic import paginate
from blog.helpers.common import custom_cache_key
from . import blog_bp


@blog_bp.route('/')
@cache.cached(key_prefix=custom_cache_key)
def index():
    return redirect(url_for('blog.post'))
    # return render_template('blog/home.html')


@blog_bp.route('/about')
@cache.cached(key_prefix=custom_cache_key)
def about():
    article = Article.query.get(1)
    return render_template('blog/about.html', article=article)


@blog_bp.route('/message', methods=['GET', 'POST'])
@cache.cached(key_prefix=custom_cache_key)
def message():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.order_by(Message.create_time.desc()).paginate(page, per_page=current_app.config[
        'PER_PAGE_MESSAGE_COUNT'], error_out=False)
    messages = pagination.items
    messageform = MessageForm()
    if messageform.validate_on_submit():
        body = messageform.body.data
        message1 = Message(body=body)
        db.session.add(message1)
        db.session.commit()
        flash('留言成功')
        return redirect(url_for('blog.message'))
    return render_template('blog/message.html', pagination=pagination, form=messageform, messages=messages)


@blog_bp.route('/post')
@cache.cached(key_prefix=custom_cache_key)
def post():
    q = request.args.get('q')
    category_id = request.args.get('category', type=int)
    tag_id = request.args.get('tag', type=int)
    categoryList = Category.query.filter_by().all()
    page = request.args.get('page', 1, type=int)
    tagList = Tag.query.filter_by().all()
    if q:
        s = Search(index='es_article').query("multi_match",
                                             query=q,
                                             fields=['title^8', 'labels.name^10', 'summary^5', 'content',
                                                     'category.name^10'])
        pagination = paginate(s, page, per_page=current_app.config['PER_PAGE_POST_COUNT'])
    elif category_id:
        pagination = Article.query.filter_by(category_field=category_id). \
            order_by(Article.id.desc()).paginate(page,
                                                 per_page=current_app.config['PER_PAGE_POST_COUNT'],
                                                 error_out=False)
    elif tag_id:
        pagination = Article.query.filter(Article.tags.any(id=tag_id)).paginate(page,
                                                                                per_page=current_app.config[
                                                                                    'PER_PAGE_POST_COUNT'],
                                                                                error_out=False)
    else:
        pagination = Article.query.filter_by(). \
            order_by(Article.id.desc()).paginate(page,
                                                 per_page=current_app.config['PER_PAGE_POST_COUNT'],
                                                 error_out=False)
    articles = pagination.items
    return render_template('blog/post.html', pagination=pagination,
                           articles=articles, category=categoryList,
                           tags=tagList)


@blog_bp.route('/category/<int:category_field>')
def category(category_field):
    categoryList = Category.query.filter_by().all()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter_by(category_field=category_field) \
        .order_by(Article.id.desc()).paginate(
        page, per_page=current_app.config['PER_PAGE_POST_COUNT'],
        error_out=False
    )
    articles = pagination.items
    return render_template('blog/post.html', pagination=pagination, articles=articles, category=categoryList,
                           category_field=category_field)


@blog_bp.route('/faq')
def faq():
    return render_template('blog/faq.html')


@blog_bp.route('/post/<int:post_id>')
@cache.cached(key_prefix=custom_cache_key)
def view_post(post_id):
    # article = Article.query.get_or_404(post_id)
    return redirect(url_for('blog.view_post_md', post_id=post_id))
    # return render_template('blog/view_post.html', article=article)


@blog_bp.route('/md/<int:post_id>', methods=['GET', 'POST'])
@cache.cached(key_prefix=custom_cache_key)
def view_post_md(post_id):
    article = Article.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(article_id=post_id).order_by(Comment.create_time.desc()).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment_body = form.body.data
        comment_user_id = current_user.id
        comment_article_id = post_id
        comment = Comment(body=comment_body,
                          user_id=comment_user_id,
                          article_id=comment_article_id)
        db.session.add(comment)
        db.session.commit()
        flash('评论成功')
        return redirect(url_for('blog.view_post_md', post_id=post_id, _anchor='comment'))
    return render_template('blog/view_post.html', article=article, form=form, comments=comments)
