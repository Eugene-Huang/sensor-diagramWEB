# -*- coding: utf8 -*-
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db, creat_app
from app.models import Role, User
import config
# from .extra import analogySensor
# inser_temperature, insert_humidity, insert_luminous_Intensity, insert_smoke, insert_fire, insert_human_infrared

app = creat_app(config.DevelopmentConfig)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


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

    if deploy_type == 'reset':
        db.drop_all()


if __name__ == '__main__':
    manager.run()
