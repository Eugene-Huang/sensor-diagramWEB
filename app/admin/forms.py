# -*- coding: utf8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Role


class AddUserForm(Form):
    email = StringField(u'Email', validators=[Required(), Length(1, 64),
                                              Email()])
    username = StringField(u'Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    role = RadioField(u'Role', choices=[('Admin', 'admin'), ('Student', 'student'),
                                        ('Teacher', 'teacher')],
                      validators=[Required()])
    password = PasswordField(u'Password', validators=[
        Required(), EqualTo('password2', message='Password must be match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField(u'Add')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_role(self, field):
        roles = []
        for row in Role.query.all():
            roles.append(row.name)
        if field.data not in roles:
            raise ValidationError('Role is not existed')


# class SearchNodeForm(Form):
#     search_text = StringField(u'搜索节点',
#                               validators=[Required(), Length(1, 64), Regexp('^[0-9]*$', 0, '传感器节点号必须是数字')])
#     submit = SubmitField(u'Search')

#     def validate_search(self, field):
#         fires = fire.query.filter_by(node=field.data).first()
#         smokes = smoke.query.filter_by(node=field.data).first()
#         human = humanInfrared.query.filter_by(node=field.data).first()
#         if not fires or smokes or human:
#             raise ValidationError('没有此节点号的传感器')
