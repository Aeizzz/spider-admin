from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(config)
    # 初始化
    login_manager.init_app(app)
    with app.app_context():
        db.init_app(app)
    # 设置
    configure_blueprints(app)
    return app


# 设置蓝图
def configure_blueprints(app):
    from .api import api
    app.register_blueprint(api)
