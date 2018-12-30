# coding = utf-8

import click

import random
from blog import db
from blog.models.article import Article
from blog.models.category import Category
from blog.models.message import Message
from blog.models.user import User
from blog.models.comment import Comment
from blog.models.tag import Tag


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--count', default=20, help='Quantity of faker data, default is 20.')
    @click.option('--init', is_flag=True)
    def forge(count, init):
        """Generate fake messages."""
        click.echo('Working...')

        if init:
            db.drop_all()
            db.create_all()

        from faker import Faker
        fake = Faker('zh_CN')

        tag_background_fields = []
        category_background_field = []

        def fake_users(count):
            admin= User(
                username='admin',
                password='admin',
                email='hello@qq.com',
                create_time=fake.unix_time(),
                info=fake.text(20),
                nickname=fake.name(),
                phone_number=fake.phone_number()
            )

            db.session.add(admin)

            for i in range(int(count / 2)):
                username_test = fake.user_name()
                user = User(
                    username=username_test,
                    password=username_test,
                    email=fake.email(),
                    create_time=fake.unix_time(),
                    info=fake.text(20),
                    nickname=fake.name(),
                    phone_number=fake.phone_number()
                )
                db.session.add(user)
            db.session.commit()
            click.echo('Created {} users'.format(int(count / 2 + 1)))

        def fake_categorys():
            for i in range(5):
                background_field = 'fl' + str(i)
                name = '分类' + str(i)
                category_background_field.append(background_field)
                category = Category(
                    name=name,
                    background_field=background_field,
                    create_time=fake.unix_time()
                )
                db.session.add(category)
            db.session.commit()
            click.echo('Created 5 categorys')

        def fake_tags():
            for i in range(5):
                tag_background_filed = 'tag' + str(i)
                name = '标签' + str(i)
                tag_background_fields.append(tag_background_filed)
                tag=Tag(
                    name=name,
                    background_field=tag_background_filed,
                    # author_id=random.randint(1,9),
                    create_time=fake.unix_time()
                )
                db.session.add(tag)
            db.session.commit()
            click.echo('Created 5 tags')



        def fake_messages(count):
            for i in range(count*5):
                message = Message(
                    user_id=random.randint(1, 9),
                    body=fake.text(),
                    create_time=fake.unix_time()
                )
                db.session.add(message)
            db.session.commit()
            click.echo('Created {} messages'.format(count*5))

        def fake_comments(count):
            for i in range(count*20):
                comment= Comment(
                    user_id=random.randint(1, 9),
                    body=fake.text(),
                    create_time=fake.unix_time()
                )
                db.session.add(comment)
            db.session.commit()
            click.echo('created {} comments'.format(count*20))


        def fake_articles(count):
            for i in range(count * 12):
                article = Article(
                    title=fake.text(20),
                    body=fake.text(1000),
                    summary=fake.text(50),
                    category_field=random.randint(1,5),
                    tag_field=random.randint(1,5),
                    author_id=random.randint(1, 10),
                    create_time=fake.unix_time()
                )
                db.session.add(article)
            db.session.commit()
            click.echo('created {} articles'.format(count * 12))


        fake_users(count)
        fake_categorys()
        fake_tags()
        fake_messages(count)
        fake_articles(count)
        fake_comments(count)

        click.echo('finished...')
