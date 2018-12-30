import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig():
    # 每页显示文章数
    PER_PAGE_POST_COUNT = 20
    PER_PAGE_MESSAGE_COUNT = 10

    # REMEMBER_COOKIE_DURATION = 30

    CKEDITOR_FILE_UPLOADER = 'blog.upload'
    CKEDITOR_HEIGHT = 500
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_PKG_TYPE = 'standard'

    # 文章内图片上传路径
    UPLOADED_PATH = os.path.normpath(os.path.join(basedir, '..\\resource\\upload'))
