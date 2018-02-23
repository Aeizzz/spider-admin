from celery import Celery
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
from .config import Config

db = SQLAlchemy()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app():
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(Config)
    # 初始化
    login_manager.init_app(app)
    db.init_app(app)
    celery.conf.update(app.config)
    # 设置
    configure_blueprints(app)
    return app


# 设置蓝图
def configure_blueprints(app):
    from .api import api
    app.register_blueprint(api)
