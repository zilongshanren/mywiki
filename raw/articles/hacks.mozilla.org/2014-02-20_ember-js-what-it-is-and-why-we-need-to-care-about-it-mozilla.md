---
title: Ember.JS – What it is and why we need to care about it – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2014/02/ember-js-what-it-is-and-why-we-need-to-care-about-it/
author: Sourav Lahoti
published: '2014-02-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post by Sourav Lahoti and his thoughts about Ember.js*

Developers increasingly turn to client-side frameworks to simplify development, and there’s a big need for good ones in this area. We see a lot of players in this field, but for lots of functionality and moving parts, very few stand out in particular — Ember.js is one of them.

So what is [Ember.js](http://emberjs.com/)? Ember.js is a MVC (Model–View–Controller) JavaScript framework which is maintained by the Ember Core Team (including Tom Dale, Yehuda Katz, and others). It helps developers create ambitious single-page web applications that don’t sacrifice what makes the web great: URI semantics, RESTful architecture, and the write-once, run-anywhere trio of HTML, CSS, and JavaScript.

## Why do we need to care

Ember.js is tightly coupled with the technologies that make up the web today. It doesn’t attempt to abstract that away. Ember.js brings a clean and consistent application development model. If one needs to migrate from HTML to any other technology, Ember.js framework will evolve along with the current trends in web front end technology.

It makes it very easy to create your own “component” and “template views” that are easy to understand, create and update. Coupled with its consistent way of managing bindings and computed properties, Ember.js does indeed offer much of the boilerplate code that a web framework needs.

## The core concept

There are some nominal terms that you will find very common when you use ember.js and they form the basics of Ember.js:

- Routes
- A Route object basically represents the state of the application and corresponds to a url.
- Models
- Every route has an associated Model object, containing the data associated with the current state of the application.
- Controllers
- Controllers are used to decorate models with display logic.
- Views
- Views are used to add sophisticated handling of user events to templates or to add reusable behavior to a template.
- Components
- Components are a specialized view for creating custom elements that can be easily reused in templates.

## Hands-on with Ember.js

Data Binding:

```
```

`App = Ember.Application.create();`

### Final result when the user interacts with the web app

Ember.js does support data binding as we can see in the above example. What we type into the input is bound to name, as is the text after `Echo: `

. When you change the text in one place, it automatically updates everywhere.

But how does this happen? Ember.js uses Handlebars for two-way data binding. Templates written in handlebars get and set data from their controller. Every time we type something in our input, the name property of our controller is updated. Then, automatically, the template is updated because the bound data changed.

## A simple Visiting card demo using Handlebars

We can create our own elements by using Handlebars.

### HTML

```
```

### CSS

```
.vcard {
border: 1px solid #dcdcdc;
max-width: 12em;
padding: 0.5em;
}
.vcard li {
list-style: none;
}
.vcard .name {
font-weight: bold;
}
.vcard .email {
font-family: monospace;
}
label {
display: block;
margin-top: 0.5em;
}
```

### JavaScript

```
App = Ember.Application.create();
App.ApplicationController = Ember.Controller.extend({
name: 'Sourav',
address: '123 M.G Road.',
city: 'Kolkata',
zipCode: '712248',
email: 'me@me.com'
});
```

The component is defined by opening a new `<script type="text/x-handlebars">`

, and setting its template name using the `data-template-name`

attribute to be `components/[NAME]`

.

We should note that the web components specification requires the name to have a dash in it in order to separate it from existing HTML tags.

There is much more to it, I have just touched the surface. For more information, feel free to check out the [Ember.js Guides](http://emberjs.com/guides/).

## About Sourav Lahoti

A native of Kolkata, India, Sourav holds a Bachelor of Technology degree in Information Technology from the University of West Bengal with a large background of strong leadership and community advocacy. Sourav currently resides in Kolkata, India and has been active in app development and web development since 2012 when he became fascinated in technology. Became "FireFox OS Marketplace App Reviewer" in 2014.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 13 comments

RafaelFebruary 20th, 2014 at 02:51Robert Nyman [Editor]February 20th, 2014 at 05:59peperoneFebruary 20th, 2014 at 06:34Daniel FilhoFebruary 20th, 2014 at 09:38Sourav LahotiMarch 2nd, 2014 at 09:39HugoFebruary 20th, 2014 at 10:57NicoFebruary 21st, 2014 at 10:57HugoFebruary 21st, 2014 at 14:44Lucas HolmquistFebruary 21st, 2014 at 18:51PopcornFebruary 22nd, 2014 at 02:59Josh HabdasFebruary 22nd, 2014 at 09:18Josh HabdasFebruary 22nd, 2014 at 09:20JerzyFebruary 25th, 2014 at 17:15