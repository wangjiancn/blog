# coding = utf-8
import os
import time
import uuid

from flask import current_app, send_from_directory, request, url_for, flash, render_template, redirect
from flask.json import jsonify
from flask_login import login_required, current_user

from blog import db
from blog.forms.article import ArticleForm, MarkdownForm
from blog.models.article import Article
from . import blog_bp


@blog_bp.route('/personal')
@login_required
def personal():
    r = request.args.get('i', default='info')
    if r == 'post':
        post = Article.query.filter_by(author_id=current_user.id).all()
        return render_template('admin/personal.html', post=post)
    return render_template('admin/personal.html')


@blog_bp.route('/new/post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category_field.data
        summary = form.summary.data
        body = form.body.data
        article = Article(title=title, body=body, summary=summary, category_field=category)
        db.session.add(article)
        db.session.commit()
        flash('上传成功')
        return redirect(url_for('blog.post'))
    return render_template('admin/newpost.html', form=form)


@blog_bp.route('/markdown/<int:postID>', methods=['GET', 'POST'])
@login_required
def edit_post_markdown(postID):
    post = Article.query.filter_by(id=postID).first_or_404()
    if request.method == 'GET':
        form = MarkdownForm(obj=post)
    else:
        form = MarkdownForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category_field = form.category_field.data.id
        post.summary = form.summary.data
        post.markdown = form.markdown.data
        post.body = form.body.data
        from blog.helpers.common import find_dup
        remove_items, add_items = find_dup(form.tags.data, post.tags)
        if add_items:
            for tag in add_items:
                post.tags.append(tag)
        if remove_items:
            for tag in remove_items:
                post.tags.remove(tag)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.view_post_md', post_id=postID))
    return render_template('admin/markdown_new_post.html', form=form)


@blog_bp.route('/markdown/post', methods=['POST', 'GET'])
@login_required
def new_post_markdown():
    form = MarkdownForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category_field.data.id
        summary = form.summary.data
        markdown = form.markdown.data
        body = form.body.data
        author_id = current_user.id
        article = Article(title=title,
                          body=body,
                          summary=summary,
                          category_field=category,
                          author_id=author_id,
                          markdown=markdown,
                          )
        if form.tags.data:
            for tag in form.tags.data:
                article.tags.append(tag)
        db.session.add(article)
        db.session.commit()
        last_post_id = Article.last_article_id(current_user.id)
        return redirect(url_for('blog.view_post_md', post_id=last_post_id))
    return render_template('admin/markdown_new_post.html', form=form)


@blog_bp.route('/files/<path:filename>')
def uploaded_files(filename):
    path = current_app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


@blog_bp.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('editormd-image-file')
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        r = {
            'success': 0,
            'message': '图片格式不允许',
            'url': '',
        }
        return jsonify(r)
    filename = uuid.uuid4().hex + '.' + extension
    f.save(os.path.join(current_app.config['UPLOADED_PATH'], filename))
    url = url_for('blog.uploaded_files', filename=filename)
    r = {
        'success': 1,
        'message': '上传成功',
        'url': url,
    }
    return jsonify(r)
