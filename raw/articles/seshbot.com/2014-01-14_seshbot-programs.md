---
title: Seshbot Programs
url: http://seshbot.com/blog/2014/01/14/learning-ruby-and-rails/
author: Paul Cechner
published: '2014-01-14'
source_blog: Seshbot Programs
source_site: http://seshbot.com/
category: game programming
fetched: '2026-04-13'
---

## Learning Ruby and Rails

*Note: The formatting of this article is not great, but I pumped it out quickly after going through the tutorials*

I dedicated this morning to learning some Ruby and Ruby on Rails (RoR). For my purposes, RoR provides the server-side API to a web application, like this:

![](../../assets/e0e8b976cd9df4b5.png)

To my delight, I quickly discovered that Ember (which I have been messing around with quite a bit) is modelled directly on Rails – not just in the generic they-are-both-MVC-architectures-way, but down to their usages being identical in many respects. I think many new webby techs follow this same style (Meteor seems to, for example.)

This post outlines the core concepts I have picked up from the various tutorials. I also included a RoR cheat-sheet I created while doing the Rails tutorial.

To get started on Windows/Mac, I’m guessing the easiest way is by downloading the [RailsInstaller](http://railsinstaller.org).

## Learning Ruby

For an absolute beginner, [Try Ruby](http://tryruby.org) takes about 30 minutes, and will show the very basics:

- basic syntax
- standard data structures (strings, arrays, hashes)
- defining methods
- defining classes (basics on attributes and
`initialize`

method)

It stays very high-level, but obviously that’s the intention. It avoids going into language features such as reflection, lambdas, string manipulation (`mystring = "var is #{my-var}"`

), and doesn’t talk about administration etc.

See the [Ruby core documentation](http://ruby-doc.org/core-2.1.0/) for reference material.

## Learning Rails

First, some language references: [Rails API docs](http://api.rubyonrails.org) or [API Dock](http://apidock.com/rails) or the other seachable [Rails API docs](http://railsapi.com) can be downloaded and used locally.

I chose to follow the [Rails for Zombies](http://railsforzombies.org) tutorial, as it is often quoted as being helpful as a fully interactive online tutorial. It takes a few hours, but does seem to cover all the fundamentals, namely:

- Rails conventions
- syntax for creation, read, update and delete of entities in the database
- naming conventions for database table, view, and controller lookup

- Models
- model class structure
- invoking CRUD operations on the models
- how relationships between entities are expressed, and how they map to the database structure

- Views
- syntax (
`<% %>`

and`<%= %>`

) - lookup from URL (searches
`app/assets`

folder before trying to run rails routes) - helpers (
`link_to`

,`edit_thing_path`

etc)

- syntax (
- Controllers
- controller class structure
- rendering alternative views
- rendering alternative formats (json, xml)
- session variables (used for basic auth checks)
- factoring out and configuring common code performed on all actions

- Routes
- defining RESTful resources (automatically direct requests to controllers/views)
- defining custom routes
- creating helpers for
`link_to`

when creating custom routes


The main thing it *doesn’t* cover is the administration (installation, deployment) and command-line usage (e.g., automatic generation of controllers and models.) This isn’t a big deal however, as the [standard getting started guide](http://guides.rubyonrails.org/getting_started.html) does this very well.

I think there are a few bugs in the programme however:

- the tutorial videos are a bit out of date (for pre-3.0 versions of RoR) but the practical exams use post-3.0 RoR it seems
- the last prac exam requires different syntax than that in the tutorial:
- redirect controller#action case is different (tut vids say
`Zombies#undead`

prac requires`zombies#undead`

) - redirect in prac requires prefix ‘/’ (‘/zombies => ’/undead’). Tutorial vids did not.

- redirect controller#action case is different (tut vids say

### Rails Cheat Sheet

I created this while going through the Zombies tutorial. There’s probably better cheat sheets out there, but I highly recommend creating your own as a learning experience.

#### RoR’s Ruby API syntax

- Entity creation syntax (note, Rails will generate an ID for you):
`t = Thing.new; t.status = "something"; t.save`

`t = Thing.new(:status => "something"); t.save`

`Thing.create(:status => "something")`


- Entity query syntax:
`Thing.find(1)`

(by ID)- many alternate query methods:
`first`

,`last`

,`all`

,`count`

,`order(:status)`

,`limit(n)`

,`where(:status => "good")`

- performance note: queries are performed on DB
- syntax note: may also chain methods

- Entity update syntax:
`t = Thing.find(id); t.status = "bad"; t.save`

`...; t.attributes = { :status => "bad"; ... }; save`

`...; t.update_attributes(:status => "bad"; ...}`

(no save)

- Entity deletion syntax:
`t = Thing.find(id); t.destroy`

`Thing.destroy_all`


- on
`save`

failure, try`t.errors`

to investigate what went wrong

#### Models

Default model definition goes in `app/models/thing.rb`


1 2 3 4 5 6 7 8 9 10 11 12 13 14 |
|

#### Views

`thing`

default view definition goes in`app/views/things/index.html.erb`

and`app/views/things/show.html.erb`

):- alternatives actions to
`show`

can be added as`myaction.html.erb`


- alternatives actions to
- evaluate code with
`<% ruby code %>`

, eval and print with`<%= ruby code %>`

- shared application stuff (header/footer) goes in
`app/views/layouts/application.html.erb`

(use`<%= yield %>`

for body placeholder)`<%= stylesheet_link_tag :all %>`

renders stylesheet links for all files in`app/assets/stylesheets/`

`<%= javascript_include_tag :defaults %>`

renders script tags for all files in`app/public/javascripts/`

- `<%= csrf_meta_tag %> adds some stuff to prevent cross-site-meta-request-forgery hacking (people injecting their own HTML into comments etc)
`<%= link_to thing.name, thing_path(thing) %>`

(first param is link text, second URL). Can use the entity itself instead of`thing_path(thing)`



Sample `index.html.erb`

(create a link to this with `things_path`

):

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 |
|

#### Controllers

`thing`

controller definition goes in`app/controllers/things_controller.rb`

_

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 |
|

#### Routes

- application routes defined in
`app/config/routes.rb`

`resources`

directive creates a full RESTful resource. This means that it will automatically create the following helpers and routes:`things_path`

(/things ‘index’ action)`thing`

(/thing/id ‘show’ action)`new_thing_path`

(/things/new ‘new’ action)`edit_thing_path(thing)`

(/things/[id]/edit ‘edit’ action)- … plus more


1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 |
|