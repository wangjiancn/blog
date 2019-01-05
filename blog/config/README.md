config/保存各种类型配置文件，生产配置不上传公开仓库，可自行创建

示例`ProductionConfig.py`:
```python
from .Config import BaseConfig

class ProductionConfig(BaseConfig):

    SECRET_KEY = "your secret key"
    # SQLAlchemy 配置
    SQLALCHEMY_DATABASE_URI = 'your sql url'

    # other config
    # ......
```