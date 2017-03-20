# -*- coding: utf8 -*-
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db, creat_app
from app.models import Role, User
import config


flask_app = creat_app(config.DevelopmentConfig)
manager = Manager(flask_app)
migrate = Migrate(flask_app, db)


def make_shell_context():
    return dict(flask_app=flask_app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# 运行网站
manager.add_command('runserver',
                    Server(host='127.0.0.1', port=5000, use_debugger=True))


@manager.command
def deploy(deploy_type):
    from flask_migrate import upgrade

    # upgrade database to the latest version
    upgrade()

    if deploy_type == 'develop':
        db.create_all()  # 创建数据表
        Role.insert_roles()  # 创建角色
        User.insert_users()  # 创建默认用户帐号

    # 重置数据库
    if deploy_type == 'reset':
        db.drop_all()
        db.create_all()
        Role.insert_roles()
        User.insert_users()


if __name__ == '__main__':
    manager.run()
