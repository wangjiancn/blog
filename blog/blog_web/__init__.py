# coding = utf-8
from flask import Blueprint

blog_bp = Blueprint('blog', __name__)

# 导入模块进行初始化
from . import blog
from . import auth
from . import admin
from . import ajax
