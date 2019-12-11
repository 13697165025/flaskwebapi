from flask import Flask
import os
from app import create_app, db
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()

migrate = Migrate(app, db)

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[测试数据]'
app.config['FLASKY_MAIL_SENDER'] = "1573572431@qq.com"


if __name__ == '__main__':
    app.run(debug=1)