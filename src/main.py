#!/usr/bin/env python2.5
# -*- coding:utf-8 -*-

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import users, xmpp

from google.appengine.ext.webapp import template

import logging

import debug_tools 
try:
    import ipdb as pdb
except ImportError:
    import pdb

from models import *
from forms import *

USERBAR_TEMPLATE = '<p>Logged in as %s - <a href="/account_settings">settings</a> <a href="%s">logout</a></p>'
USERBAR_ANON_TEMPLATE = '<p><a href="%s">login</a></p>'

class MainHandler(webapp.RequestHandler):
    def get(self):
        """
        The home
        """
        user = users.get_current_user()
        
        if user:
            profile = Profile.get_by_user(user)
            # debug_tools.setup()
            # pdb.set_trace()

            # TODO: Use the profile's email hash to generate Gravatar avatars
            userbar_text = USERBAR_TEMPLATE % (user.nickname(), users.create_logout_url('/')) 
        else:
            userbar_text = USERBAR_ANON_TEMPLATE % users.create_login_url('/')

        template_values = {'userbar_text': userbar_text,
                           'featured': ['a', 'list', 'of', 
                                        'featured', 'episodes'],
                           'latest': ['a', 'list', 'of', 
                                      'latest', 'episodes']}
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        raise NotImplementedError

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
