---
title: Seshbot Programs
url: http://seshbot.com/blog/2014/01/15/creating-a-rails-plus-ember-app-from-scratch/
author: Paul Cechner
published: '2014-01-15'
source_blog: Seshbot Programs
source_site: http://seshbot.com/
category: game programming
fetched: '2026-04-13'
---

## Creating and Deploying a Rails + Ember App

Today I decided to wield my new Rails and Ember knowledge and… look into yet another new technology. I thought it would be helpful to have an online app to demonstrate the fruits of my labours, so am deploying a new app to ** Heroku**.

Heroku is an ‘application platform’ in the cloud, meaning that you can push certain kinds of apps (written in Ruby, Python, Java and Node.js) and it will ensure all the correct infrastructure is in place. When you sign up you get to host one app for free so it’s easy to try out.

Later I will probably move to [Amazon Web Services](http://aws.amazon.com), which provides a basic virtual machine in the cloud that you can do anything with. This will allow me to host multiple applications without having to worry about paying money. Heroku *does* offer some pretty nice scaling, monitoring and deployment tools though (the admin panel literally has a slider to allow you to spin up new application instances.)

This post shows how I went through all steps, including setting up the PostgreSQL database on OSX, creating a skeleton Rails app, and deploying to Heroku. It is a culmination of having gone through several sources:

- much was taken from this useful step-by-step ‘
[Rails + Ember blog post](http://www.devmynd.com/blog/2013-3-rails-ember-js)’ and this[follow up post](http://www.devmynd.com/blog/2013-10-live-on-the-edge-with-rails-ember-js)that incorporates changes for newer versions of the frameworks. - when I got to the part involving installing the ‘ember-rails’ gem, I found that the
[ember-rails documentation](https://github.com/emberjs/ember-rails)was pretty useful. - some of the Heroku stuff came from the
[Heroku Code School lesson](https://www.codeschool.com/code_tv/heroku)summary.

## Choosing a database

By default Rails will use sqlite3 for its database, and this isn’t by default available in Heroku. As I’m going to have to do some configuration anyway, I might as well choose a nicer database.

I was deciding between MongoDb and PostgreSQL. MongoDb offers flexibility when it comes to managing file assets in your database, while PostgreSQL is much more well established in existing hosting infrastructures (AWS and Heroku), so can make initial deployment much simpler. Mongo is also more amenable to schema changes because it’s a NoSQL schema-less document database, but I think Rails is supposed to make schema changes easy anyway with the various `db:`

commands.

As Heroku comes with PostgreSQL support out of the box, for now I’ll go with Postgres. I’m as yet not very familiar with Heroku and want to make things easier on myself.

The following installation instructions came from a blog entry on [installing PostgreSQL on OSX with HomeBrew](http://ricochen.wordpress.com/2012/07/20/install-postgres-on-mac-os-x-lion-with-homebrew-howto/):

1 2 3 4 5 6 7 8 9 10 11 12 13 14 |
|

*Notes:*

*the*`createuser`

command can replace the`psql`

command stuff:`createuser -d myapp`

*if the DB username is different to the application name (below) you’ll need to change the rails configuration later so it knows which username to use**I assume Heroku doesn’t require you to manage the database at all*

## Creating a simple Rails app

Creating a Rails app is really simple *once you know the commands*. So from scratch, if you include all the learning involved behind each command, it’s actually not very simple. But these steps make it simple for me.

TIPS: I read somewhere that you should always run `bundle exec`

before running a rails command to ensure that you’re only working with gems in your Gemfile. Technically you could run all the commands below without prepending `bundle exec`

however.

1 2 3 4 5 6 7 |
|

*Note: I had to uncomment the ‘local’ setting from my *database.yml* file because rails couldn’t connect due to permission problems on the local socket file. I could have reconfigured postgres instead but meh.*

OSX users can also use [POW!](http://pow.cx/) or [Anvil](http://anvilformac.com/) (which uses POW! under the covers) to set up a fake URL pointing to their local rails app directories, so in my case I can visit [http://myapp.dev](http://myapp.dev) and it will actually show me the app running on my local machine. It makes the testing cycle a lot quicker.

Add some simple static content:

1 2 3 4 |
|

Now you should be able to visit `localhost:3000`

and see a generic ‘home’ page message.

### Check in to git

This creates a local git repository, but during the heroku deployment step I’ll push it over there too. I’ll also push it to GitHub when it looks like more of an app. So in git parlance, this is what I’ll have on my local machine:

![](../../assets/809609f1f0e764d2.png)

1 2 3 4 |
|

I regularly run those `git`

commands to make it easier to revert any mistakes I happen to make.

### Adding ember framework

I have tried two alternative approaches to creating a new rails app for ember.

#### Alternative 1: use the ember ‘edge template’

I think this one is probably the best as it was demonstrated by Yehuda Katz (main Ember guy) in [this live demonstration video](http://www.youtube.com/watch?v=BpQj9_qEUAc). I ran a diff on projects created with and without and it seems to:

- adds some ember gems to the Gemfile:
`active_model_serializers`

,`ember-rails`

and`ember-source`

- remove the rails ‘application view layout’ (
*app/views/layouts/application.html.erb*) - create an ember ‘application template’ (
*app/assets/javascripts/templates/application.handlebars*) - creates a ‘view asset’ that generates an index.html with the ember application.js in it (
*app/views/assets/index.html.erb*) - sets up a rails route pointing to the assets controller ‘index’ action (
*config/routes.rb*) - create empty assets controller and helper files (not sure why)
- create a rails ActiveModel ‘application serializer’ (
*app/serializers/application_serializer.rb*) that does a few things ember requires

Installing using the edge template is simple. Just replace the `rails new`

step above with the following:

1 2 3 4 |
|

*Note: I had problems using the remote edge template, so downloaded it and used my local copy instad.*

#### Alternative 2: add ember to an existing rails app

You could also just add the `ember-rails`

gem directly to your Gemfile, then run `rails generate ember:bootstrap`

and you get a basic Ember framework in your `app/assets`

directory. I also prefer to use javascript directly (as opposed to CoffeeScript, which is the default), so add `-g --javascript-engine js`


1 2 |
|

Following this approach I believe you’ll have to manually set up the [Ember ActiveModel Serializer](https://github.com/rails-api/active_model_serializers) which was written by the Ember guys, and ensures your Ember app understands the format of your Rails app’s JSON data. The first alternative does this for you.

#### Common to both approaches

After you have created and updated your Gemfile, you still need to bootstrap the ember environment, and then ensure Ember is running in ‘development’ mode when Rails is.

*Note: you can Set ‘developer mode’ (which enables developer-centric error messages and is apparently quite useful) by updating your *config/environments/development.rb* with: config.ember.variant = :development. By default running locally will run in dev mode, and running on Heroku will run production mode however.*

1 2 3 4 5 |
|

## Deploying to Heroku

Heroku requires a few rails settings to be modified to work properly:

1 2 3 4 5 |
|

I have already gone through the Heroku sign up process and installed the toolbelt appropriate for OSX (the toolbelt provides the `heroku`

command line tool), so I won’t outline that here.

Installing my rails application on Heroku was then a simple matter of:

1 2 3 4 5 6 7 8 9 |
|

This creates an image with a particular configuration of applications and adds a `heroku`

git remote to the git configuration.

Now you can visit the heroku app online (in my case at [http://seshbot.herokuapp.com/](http://seshbot.herokuapp.com/)).

TODO: use `gem rails_12factor`

? This alters the rails app a little to make it [12 factor](http://12factor.net/), which is a set of guidelines for how one should build an application to make it easier to administer and deploy. Not really important right now though.

## Troubleshooting and administering Heroku

1 2 3 |
|

1 2 3 4 |
|

`heroku config`

sets environment variables for things you don’t want to commit to git (e.g., passwords). Configure your Rails apps to use `ENV['MY_VAR']`

instead of your super secret key, then run `heroku config:add MY_VAR=blahblah`

.

There are also various `heroku pg:`

commands for updating the application database. The application itself doesn’t have full admin access to the database so you can’t for example write `heroku run rake db:drop`

. Instead you should run `heroku pg:reset`

if you want to clear the database.