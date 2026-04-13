---
title: Time to get hacking – Introducing Rec Room – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/08/time-to-get-hacking-introducing-rec-room/
author: Matthew Riley MacPherson
published: '2014-08-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It’s no secret that the best frameworks and tools are extracted, not created out of thin air. Since launching Firefox OS, Mozilla has been approached by countless app developers and web developers with a simple question: “How do I make apps for Firefox OS?” The answer: “It’s the web; use existing web technologies.” was—and still is—a good answer.

But if you don’t already *have* an existing toolchain as a web developer, I’ve been working on extracting something out of the way I’ve been creating web apps at Mozilla that you can use to write your next web app. From project creation to templating to deployment, [Mozilla’s Rec Room](https://github.com/mozilla/recroom) will help you create awesome web apps in less time with more ease.

Rec Room is a Node.js utility belt you can wear to build client side web apps. It includes:

**Brick**to add components like appbars and buttons to your UI.**Ember**for your app’s controllers, models, and views.**Handlebars**to write your app’s templates.**Grunt**to run the tasks for your app, including building for production.**I18n.js**to localize your app.**Mocha**to test your app.**Stylus**to write your CSS.**Yeoman**to scaffold new code for your app’s models and templates.

In this post I’ll walk through how to create a simple world clock web app with Rec Room, how to deploy it, and how you can try out Rec Room for yourself.

## Where Does Rec Room Come From?

Much of Rec Room came from a recent rewrite of the [HTML5 podcast app](https://github.com/mozilla/high-fidelity/). I started working on this app [well over a year ago](https://github.com/mozilla/high-fidelity/commit/6f023aa399b3d7b773d0f41c182d9f7b328a6184), but its original version wasn’t as easy to work on; it had a *lot* of global state and a lot of by-hand data-binding. I liked the look of Ember for app development, but back when I started it didn’t quite feel mature enough. These days it’s much better, and I’ve tweaked it in Rec Room to work perfectly without a server.

I tried to take the best from that system and extract it into a set of tools and documentation that anyone can use.

## Create your own Rec Room app

Rec Room has just recently been extracted from my experiences with Podcasts; it hasn’t been tested by more than a handful of developers. That said: we’d love your help trying to build your own app for Firefox OS using these tools. They integrate well with tools you probably already know and use–like Node.js and Firefox’s own Web IDE.

To get started, install Rec Room using Node.js:

```
npm install -g recroom
```

## Clock App

We’ll create a simple clock app with (minimal) time zone support for our example. The app will let you have a clock and compare it with a few time zones.

The `recroom`

binary is your entry point to all of the cool things Rec Room can do for you. First, create your app using `recroom new world-clock`

. This creates the basic app structure. To see the basic app skeleton that Rec Room creates we can now enter that directory and run our app: `cd world-clock`

and then type `recroom run`

. The app will open in your default browser.

First, we’ll add the current time to the main tab. Rec Room supports Ember’s MVC app structure, but also offers simple “pages” for a controller without a 1:1 relationship to a model. We’ll generate a new page that will show our actual clock:

```
recroom generate page Clock
```

We can edit its template by opening `app/templates/clock.hbs`

. Let’s change `clock.hbs`

to include the variable that will output our local time:

```
```## Local Time: {{localTime}}


That won’t do much yet, so let’s add that variable to our `ClockController`

, in `app/scripts/controllers/clock_controller.js`

:

```
WorldClock.ClockController = Ember.ObjectController.extend({
localTime: new Date().toLocaleTimeString()
});
```

You can see that any property inside the controller is accessible inside that controller’s template. We define the `1ocalTime`

property and it gets carried into our template context.

Now our clock app will show the current local time when we navigate to `http://localhost:9000/#clock`

. Of course, it just shows the time it was when the controller was initialized; there is no live updating of the time. We should update the time every second inside the controller:

```
WorldClock.ClockController = Ember.ObjectController.extend({
init: function() {
// Update the time.
this.updateTime();
// Run other controller setup.
this._super();
},
updateTime: function() {
var _this = this;
// Update the time every second.
Ember.run.later(function() {
_this.set('localTime', new Date().toLocaleTimeString());
_this.updateTime();
}, 1000);
},
localTime: new Date().toLocaleTimeString()
});
```

Now we can go to our clock URL and see our clock automatically updates every second. This is thanks to Ember’s data-binding between controllers and templates; if we change a value in a controller, model, or view that’s wired up to a template, the template will automatically change that data for us.

### Adding Timezones

Next, we want to add a few timezones that the user can add to their own collection of timezones to compare against local time. This will help them schedule their meetings with friends in San Francisco, Buenos Aires, and London.

We can create a timezone model (and accompanying controllers/routes/templates) with the same `generate`

command, but this time we’ll generate a model:

```
recroom generate model Timezone
```

We want each timezone we’re to include in our app to have a name and an offset value, so we should add them as model attributes. We use [Ember Data](https://github.com/emberjs/data) for this, inside `app/scripts/models/timezone_model.js`

:

```
WorldClock.Timezone = DS.Model.extend({
name: DS.attr('string'),
offset: DS.attr('number')
});
```

Next we’ll want a list of all timezones to offer the user. For this we’ll grab a copy of [Moment Timezone](http://momentjs.com/timezone/). It’s an awesome JavaScript library for dealing with dates and times in JavaScript. We’ll install it with [bower](http://bower.io/):

```
bower install moment-timezone --save
```

And then add it to our app inside `app/index.html`

:

```
```

Adding that tag will automatically add `moment-timezone-with-data-2010-2020.js`

to our built app. We’ll add a tab to the page that lets us edit our timezones, on a different screen than the clocks. To add a tab, we just need to open `app/templates/application.hbs`

and add a tab. While we’re there, we’ll change the main tab from the useless `{{#linkTo 'index'}}`

and point it to `{{#linkTo 'clock'}}`

. The new `application.hbs`

should look like this:

```
```
{{outlet}}

Side note: notice the root URL points to a useless welcome page? We probably want the default route to be our `ClockController`

, so we can set the index route to redirect to it. Let’s do that now, in `app/scripts/routes/application_route.js`

:

```
WorldClock.ApplicationRoute = Ember.Route.extend({
redirect: function() {
this.transitionTo('clock');
}
});
```

### Interacting with Timezone models

We’ll keep things simple for our example and allow users to select a timezone from a `<select>`

tag and add it with a button. It will show up in their list of timezones, and they can delete it if they want from there. The clock tab will show all times. First, we’ll add our timezone data from Moment.js into our `TimezonesController`

in `app/scripts/controllers/timezones_controller.js`

. We’re also going to implement two actions: “add” and “remove”. These will be used in our template:

```
WorldClock.TimezonesController = Ember.ObjectController.extend({
init: function() {
var timezones = [];
for (var i in moment.tz._zones) {
timezones.push({
name: moment.tz._zones[i].name,
offset: moment.tz._zones[i].offset[0]
});
}
this.set('timezones', timezones);
this._super();
},
selectedTimezone: null,
actions: {
add: function() {
var timezone = this.store.createRecord('timezone', {
name: this.get('selectedTimezone').name,
offset: this.get('selectedTimezone').offset
});
timezone.save();
},
remove: function(timezone) {
timezone.destroyRecord();
}
}
});
```

So we create a list of *all* available timezones with offsets. Then we add methods that allow us to add or remove timezones from our offline data store. Next we modify the timezones template in `app/templates/timezones.hbs`

to use the actions and variables we created. All we need to utilize these variables is the Ember `SelectView`

and the `{{action}}`

helper to call our `add`

and `remove`

methods:

```
```## Add Timezone

{{view Ember.Select content=timezones selection=selectedTimezone
optionValuePath='content.offset' optionLabelPath='content.name'}}

## My Timezones


-
{{#each model}}
- {{name}} {{/each}}

Now we have a Timezones tab that allows us to add and remove Timezones we want to track. This data persists between app refreshes. The last thing we need to do is show these times relative to our local time in our clock tab. To do this we need to load all the `Timezone`

models in the `ClockRoute`

. They’re automatically loaded in the `TimezonesRoute`

, but it’s easy to add them in the `ClockRoute`

(in `app/scripts/routes/clock_route.js`

):

```
WorldClock.ClockRoute = Ember.Route.extend({
model: function() {
return this.get('store').find('timezone');
}
});
```

Because of the way our Ember app is wired up, we load all our models in the route and they are sent to the controller once the data store has asynchonously loaded all of the models. The request to `find('timezone')`

actually returns a `Promise`

object, but Ember’s router handles the Promise resolving for us automatically so we don’t have to manage callbacks or Promises ourselves.

Now we have access to all the user’s Timezones in the `ClockController`

, so we can make times in each timezone the user has requested and show them in a list. First we’ll add each Timezone’s current time to our `ClockController`

in `app/scripts/controllers/clock_controller.js`

using Moment.js:

```
WorldClock.ClockController = Ember.ObjectController.extend({
updateTime: function() {
var _this = this;
// Update the time every second.
Ember.run.later(function() {
_this.set('localTime', moment().format('h:mm:ss a'));
_this.get('model').forEach(function(model) {
model.set('time',
moment().tz(model.get('name')).format('h:mm:ss a'));
});
_this.updateTime();
}, 1000);
}.on('init'),
localTime: moment().format('h:mm:ss a')
});
```

Our final `app/templates/clock.hbs`

should look like this:

```
```## Local Time: {{localTime}}

{{#each model}}

### {{name}}: {{time}}

{{/each}}

And that’s it! Now we have an offline app that shows us time zones in various places, saves the data offline, and updates every second without us having to do much work!

### Command Line Tools

The old Podcasts app used a [(rather awful) Makefile](https://github.com/mozilla/high-fidelity/blob/f73b8b4bde0753512a2c905e66c8a84fafb56e5e/Makefile). It wasn’t very useful, and I don’t think it ran on Windows without some *serious* effort. The new build system uses Node so it runs comfortably on Windows, Mac, and Linux. Commands are proxied via the `recroom`

binary, also written in Node, so you don’t have to worry about the underlying system if you don’t need to modify build steps. `recroom new my-app`

creates a new app; `recroom serve`

serves up your new app, and `recroom generate model Podcast`

creates a new model for you.

To build your app, you just need to run `recroom build`

and a version with minified CSS, JS, and even HTML will be created for you in the `dist/`

folder. This version is ready to be packaged into a packaged app or uploaded to a server as a hosted app. You can even run `recroom deploy`

to deploy directory to your git repository’s GitHub pages branch, if applicable.

## See the app in action!

This entire sample app is available at [worldclock.tofumatt.com](http://worldclock.tofumatt.com/) and the [source code is available on GitHub](https://github.com/tofumatt/tout-le-temps).

## Try Using Rec Room for Your Next Web App

You can try out [Rec Room on Github](https://github.com/mozilla/recroom). Right now some docs and tools are still being abstracted and built, but you can start building apps today using it and filing bugs for missing features. We’d really love it if you could give it a try and let us know what’s missing. Together we can build a cohesive and polished solution to the all-too-common question: “How do I build a web app?”

## About
[
Matthew Riley MacPherson ](http://lonelyvegan.com)

Matthew Riley MacPherson (aka tofumatt) is a Rubyist living in a Pythonista's world. He's from Canada, so you'll find lots of odd spelling (like "colour" or "labour") in his writing.
He has a serious penchant for pretty code, excellent coffee, and very fast motorcycles. Check out his [code on GitHub](https://github.com/tofumatt) or [talk to him about motorcycles on Twitter](https://twitter.com/tofumatt).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 23 comments

Mario ValenteAugust 18th, 2014 at 11:05Fawad HassanAugust 18th, 2014 at 11:30Nick DesaulniersAugust 18th, 2014 at 16:11No ThanksAugust 18th, 2014 at 15:22Robert Nyman [Editor]August 19th, 2014 at 01:14sudarshanAugust 19th, 2014 at 05:43tofumattAugust 19th, 2014 at 05:45WMAugust 19th, 2014 at 23:12tofumattAugust 20th, 2014 at 06:40Michael NiemannAugust 19th, 2014 at 15:04tofumattAugust 19th, 2014 at 15:24Michael NiemannAugust 20th, 2014 at 08:19Andrew FallowsAugust 21st, 2014 at 10:17Robert Nyman [Editor]August 22nd, 2014 at 00:26LucasAugust 20th, 2014 at 13:39LucasAugust 20th, 2014 at 16:43gasolinAugust 24th, 2014 at 15:49Robert Nyman [Editor]August 25th, 2014 at 00:19MartinAugust 25th, 2014 at 00:27Robert Nyman [Editor]August 25th, 2014 at 01:22tofumattAugust 26th, 2014 at 10:29AdamAugust 28th, 2014 at 15:01maitreyaSeptember 6th, 2014 at 10:44