# -*- coding: utf8 -*-

from app import create_app, celery

app = create_app()
app.app_context().push()