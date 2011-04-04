# -*- coding:utf-8 -*-

from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.api.urlfetch_errors import DownloadError
from google.appengine.ext import db
from google.appengine.runtime import DeadlineExceededError

import datetime
import logging

class Profile(db.Model):
    """
    Someone who works on stuff
    """
    user = db.UserProperty(required = True)
    # wants_reports_by_email = db.BooleanProperty(default = True, required = True)
    # timezone = db.StringProperty(choices = TIMEZONE_CHOICES)
    name = db.StringProperty()
    email_hash = db.StringProperty()

    @classmethod
    def get_by_user(cls, user):
        p = Profile.all().filter('user =', user).get()
        if p:
            return p
        else:
            Profile(user = user).put()
            return Profile.get_by_user(user)



class Feed(object):
    """
    A podcast feed
    """
    feed_url = db.LinkProperty()
    featured = db.BooleanProperty(default = False)
    last_episode = db.DateTimeProperty()
    last_updated = db.DateTimeProperty()


class Episode(db.Model):
    """
    An episode of a feed
    """
    feed = db.ReferenceProperty(Feed)
    

    def add_reply(self, author, contents):
        """
        Adds a new comment as a top comment to this episode
        (without a parent)
        """
        r = Comment(episode = self,
                    author = author,
                    contents = contents)
        r.put()
        return r


class Comment(db.Model):
    """
    A comment about an episode
    """
    episode = db.ReferenceProperty(Episode)
    author = db.EmailProperty()
    contents = db.TextProperty()
    posted = db.DateTimeProperty(auto_now_add = True)
    karma = db.IntegerProperty()
    subtree_karma = db.IntegerProperty()

    def add_karma(self, value):
        """
        Adds value to the current post's karma.
        
        Recursively adds karma to the parents

        Returns a tuple of this post karma and its subtree karma
        """
        self.karma += value
        self.put()
        if self.parent:
            self.parent.add_karma(value)
        return (self.karma, self.subtree_karma)

    def add_reply(self, author, contents):
        """
        Adds a new comment as a reply of this comment

        Returns the reply added
        """
        r = Comment(parent = self, 
                    episode = self.episode, 
                    author = author, 
                    contents = contents)
        r.put()
        return r
        

    

        
        
