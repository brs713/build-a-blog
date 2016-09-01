#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import jinja2
import os

from google.appengine.ext import db
#import "google.golang.org/appengine/datastore"

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Blog(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    # """
    # Builds the homepage
    #     - should show 5 most recent blog posts?
    #     - has an area for text & title input
    #     - has a submit button that redirects to /newpost page
    # """

    def render_home(self, title="", body="", error=""):
        #blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        self.render("home.html", title=title, body=body, error=error)

    def get(self):
        self.render_home()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        #TODO Fix this - make it an appropriate self.redirect()...
        if title and body:
            entry = Blog(title = title, body = body)
            entry.put()
            self.redirect("/")
        else:
            error = "Please enter a valid title & body."
            self.render_home(title, body, error)

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
