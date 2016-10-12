# -*- coding: utf8 -*-

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

# 自定义装饰器

# 检查用户权限


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):  # 需要管理员
    return permission_required(Permission.ADMINISTER)(f)


def root_required(f):  # 需要root
    return permission_required(Permission.ROOT)(f)
