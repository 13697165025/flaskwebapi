from flask import Flask, current_app
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = 'main.LoginView'

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


# 建立一个工厂模式
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1/')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app


