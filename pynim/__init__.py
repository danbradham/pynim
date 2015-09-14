# -*- coding: utf-8 -*-

__title__ = 'pynim'
__version__ = '0.0.1'
__author__ = 'Dan Bradham'
__email__ = 'danielbradham@gmail.com dan@brandnewschool.com'
__url__ = 'http://github.com/danbradham/pynim.git'
__license__ = 'MIT'
__description__ = 'NIM Python api'


import sys
platform = sys.platform.rstrip('123456789').lower()
if platform == 'darwin':
    platform = 'osx'


class Context(object):
    '''NIM Context'''

    base_uri = None
    user = None
    project = None
    asset = None
    show = None
    shot = None


def configure(hostname, port=80):
    '''Configure '''

    Context.base_uri = 'http://{0}:{1}/nimAPI.php?'.format(hostname, port)


def make_uri(uri, **kwargs):
    '''Create an uri for an HTTP request.

    usage::

        >> make_uri('q=getUserID', u='aUser')
        'http://hostname:port/nimAPI.php?q=getUserID&u=aUser'
    '''


    out_uri = Context.base_uri + uri

    if kwargs:
        for k, v in kwargs.iteritems():
            out_uri += '&{0}={1}'.format(k, v)

    return out_uri


from .models import *
