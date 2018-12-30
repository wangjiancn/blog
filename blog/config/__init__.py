from .DevelopmentConfig import DevelopmentConfig
from .ProductionConfig import ProductionConfig
from .TestingConfig import TestingConfig

config_map = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
