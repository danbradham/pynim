# -*- coding: utf-8 -*-

__title__ = 'pynim'
__version__ = '0.0.1'
__author__ = 'Dan Bradham'
__email__ = 'danielbradham@gmail.com dan@brandnewschool.com'
__url__ = 'http://github.com/danbradham/pynim.git'
__license__ = 'MIT'
__description__ = 'NIM Python api'


import os
import sys
from types import ModuleType
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


platform = sys.platform.rstrip('123456789').lower()
if platform == 'darwin':
    platform = 'osx'


class Context(object):
    host = None
    port = None
    database = None
    user = None
    engine = None
    base = None
    session = None


def get_db_path():

    if not Context.host or not Context.user or not Context.database:
        raise Exception('API not yet configured...\n'
                        'pynim.configure(host=host, database=database)')

    return 'mysql://{user}@{host}/{database}'.format(**Context.__dict__)


def get_session():

    if not Context.engine or not Context.base:
        raise Exception('API not yet configured...\n'
                        'pynim.configure(host=host, database=database)')

    if not Context.session:
        metadata = Context.base.metadata
        Session = sessionmaker(bind=Context.engine)
        Context.session = Session()

    return Context.session


def configure(host=None, port=None, database=None, user=None):
    '''Configure API context'''

    if not host:
        host = os.environ.get('PYNIM_HOST')
    if not port:
        port = os.environ.get('PYNIM_PORT')
    if not database:
        database = os.environ.get('PYNIM_DATABASE', 'n_proj')
    if not user:
        user = os.environ.get('PYNIM_DATABASE_USER', 'root')

    Context.host = host
    Context.port = port
    Context.database = database
    Context.user = user
    Context.engine = create_engine(get_db_path())
    Context.base = declarative_base(Context.engine)

    _init_models()
    import models


_excluded_tables = ['phinxlog'] # Tables without primary key columns
_models = ModuleType('_models')
sys.modules['_models'] = _models

def _init_models(excluded_tables=_excluded_tables):
    '''Create Database ORM dynamically, then import model api wrapping ORM'''

    def _create_model(classname, tablename):
        bases = (Context.base,)
        attrs = {
            '__tablename__': tablename,
            '__table_args__': {'autoload': True}
        }
        return type(classname, bases, attrs)

    for table in Context.engine.table_names():

        if table in excluded_tables:
            continue

        tablename = str(table)
        classname = tablename.title()
        model = _create_model(classname, tablename)
        setattr(_models, classname, model)
