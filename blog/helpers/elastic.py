from math import ceil

from elasticsearch_dsl import Document, Text, Date, Integer, Keyword, Boolean, InnerDoc, Nested, connections
from flask import request, abort

connections.create_connection(hosts=['localhost'])


class ESTag(InnerDoc):
    id = Integer()
    name = Keyword()


class ESCategory(InnerDoc):
    id = Integer()
    name = Keyword()


class ESArticle(Document):
    id = Integer()
    title = Text()
    summary = Text()
    content = Text(analyzer="body_analyzer")
    author = Keyword()
    status = Boolean()
    create_time = Date()
    create_datetime = Text(analyzer="keyword")
    tags = Nested(ESTag)
    category = Nested(ESCategory)

    class Index:
        name = 'es_article'
        settings = {
            "number_of_shards": 3,
            "number_of_replicas": 1,
            "analysis": {
                "analyzer": {
                    "body_analyzer": {
                        "type": "custom",
                        "tokenizer": "ik_smart",
                        "filter": ["lowercase"],
                        "char_filter": ["markdown_map"]
                    },
                    "default": {
                        "type": "custom",
                        "tokenizer": "ik_smart",
                        "filter": ["my_edge_ngram"],
                        "char_filter": ["markdown_map"]
                    }
                },
                "char_filter": {
                    "markdown_map": {
                        "type": "mapping",
                        "mappings": ["# =>  ", "- =>  "]
                    }
                },
                "filter": {
                    "my_edge_ngram": {
                        "type": "edgeNGram",
                        "min_gram": 1,
                        "max_gram": 10
                    }
                }
            }

        }

    def add_tag(self, id, name):
        self.tags.append(ESTag(id=id, name=name))

    def add_category(self, id, name):
        self.category.append(ESCategory(id=id, name=name))

    def from_sql(self, article):
        for tag in article.tags:
            self.add_tag(tag.id, tag.name)
        self.add_category(article.category.id, article.category.name)
        self.meta.id = article.id
        self.id = article.id
        self.summary = article.summary
        self.title = article.title
        self.content = article.markdown
        self.status = article.status
        self.author = article.author.username
        self.create_datetime = article.create_datetime
        self.create_time = article.create_time
        self.save()

    @classmethod
    def turn_es(cls, article):
        post = cls.get(article.id, ignore=404)
        if post:
            return post
        else:
            return cls(meta={'id': article.id})


class ESPagination(object):
    """Internal helper class returned by :meth:`BaseQuery.paginate`.  You
    can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.
    """

    def __init__(self, page, per_page, total, items):
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = total
        #: the items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def prev_num(self):
        """Number of the previous page."""
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        if not self.has_next:
            return None
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
                    (num > self.page - left_current - 1 and \
                     num < self.page + right_current) or \
                    num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def paginate(search, page=None, per_page=None, error_out=True, max_per_page=None):
    """Returns ``per_page`` items from page ``page``.

    If ``page`` or ``per_page`` are ``None``, they will be retrieved from
    the request query. If ``max_per_page`` is specified, ``per_page`` will
    be limited to that value. If there is no request or they aren't in the
    query, they default to 1 and 20 respectively.

    When ``error_out`` is ``True`` (default), the following rules will
    cause a 404 response:

    * No items are found and ``page`` is not 1.
    * ``page`` is less than 1, or ``per_page`` is negative.
    * ``page`` or ``per_page`` are not ints.

    When ``error_out`` is ``False``, ``page`` and ``per_page`` default to
    1 and 20 respectively.

    Returns a :class:`Pagination` object.
    """

    if request:
        if page is None:
            try:
                page = int(request.args.get('page', 1))
            except (TypeError, ValueError):
                if error_out:
                    abort(404)

                page = 1

        if per_page is None:
            try:
                per_page = int(request.args.get('per_page', 20))
            except (TypeError, ValueError):
                if error_out:
                    abort(404)

                per_page = 20
    else:
        if page is None:
            page = 1

        if per_page is None:
            per_page = 20

    if max_per_page is not None:
        per_page = min(per_page, max_per_page)

    if page < 1:
        if error_out:
            abort(404)
        else:
            page = 1

    if per_page < 0:
        if error_out:
            abort(404)
        else:
            per_page = 20

    start = (page - 1) * per_page
    end = start + per_page
    i = search[start: end]
    items = i.execute().hits

    if not items and page != 1 and error_out:
        abort(404)

    total = items.total

    return ESPagination(page, per_page, total, items)
