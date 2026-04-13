---
title: Localize Your Node.js Service, part 1 of 3 – A Node.js holiday season, part
  9 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/04/localize-your-node-js-service-part-1-of-3-a-node-js-holiday-season-part-9/
author: Austin King
published: '2013-04-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is episode 9, out of a total 12, in the

[A Node.JS Holiday Season series]from Mozilla’s Identity team. Now it’s time to delve into localization!

![](../../assets/26882a5a31e3404b.png)


Did you know that Mozilla’s products and services are localized into into as many as 90 languages?

The following are just a few examples of localization:

- Text translated into a regional language variations
- A screen rendered right to left for a given language
- Bulletproof designs that accommodate variable length prose
- Label, heading, and button text that resonates with a locale audience

In this series of posts, I’m going to cover some technical aspects of how to localize a Node.js service.

Before we start, I’ll be using the acronyms L10n (**L**ocalizatio**n**) and I18n **I**nternationalizatio**n**. I18n is the technical plumbing needed to make L10n possible.

Mozilla Persona is a Node.js based service localized into X locales. Our team has very specific goals that inhibit us from using existing Node L10n libraries.

## Goals

We created these modules, to meet the following goals

- Work well with existing Mozilla L10n community
- Let developers work with a pure JS toolkit

The resulting toolkit contains several new Node modules:

- i18n-abide
- jsxgettext
- po2json.js
- gobbledygook

i18n-abide is the main module you’ll use to integrate translations into your own service. Let’s walk through how to add it.

In these examples, we’ll assume your code uses [Express](http://expressjs.com/) and [EJS templates](https://github.com/visionmedia/ejs).

## Installation

```
npm install i18n-abide
```

## Preparing your codebase

In your code

```
var i18n = require('i18n-abide');
app.use(i18n.abide({
supported_languages: ['en-US', 'de', 'es', 'zh-TW'],
default_lang: 'en-US',
translation_directory: 'static/i18n'
}));
```

We will look at the configuration values in detail during the third installment of this L10n series.

The i18n `abide`

middleware sets up request processing and injects various functions which We’ll use for translation. Below, we will see these are available in the request object and in the templating context.

Okay, you next step is to work through all of your code where you have user visible prose.

Here is an example template file:

```
```<%= gettext('Mozilla Persona') %>

The key thing abide does, is it injects into the Node and express framework references to the `gettext`

function.

Abide also provides other variables and functions, such as `lang`

, `lang_dir`

.

`lang`

is the language code based on the user’s browser and preferred language settings.`lang_dir`

is for[bidirectional text](http://en.wikipedia.org/wiki/Bi-directional_text)support.

It will be either`ltr`

or`rtl`

. The English language is rendered`ltr`

or left to right.`gettext`

is a JS function which will take an English string and return a localize string, again based on the user’s preferred region and language.

When doing localization, we refer to **strings** or Gettext strings: these are pieces of prose, labels, button, etc. Any prose that is visible to the end user is a string.

Technically, we don’t mean JavaScript String, as you can have strings which are part of your program, but never shown to the user. String is overloaded to mean, stuff that must get translated.

Here is an example JavaScript file:

```
app.get('/', function(req, res) {
res.render('homepage.ejs', {
title: req.gettext('Hello, World!')
});
});
```

We can see that these variables and functions (like `gettext`

) are placed in the `req`

object.

So to setup our site for localization, we must look through all of our code and templates and wrap **strings** in calls to `gettext`

.

## Language Detection

How do we know what the user’s preferred language is?

At runtime, the middleware will detect the user’s preferred language.

The i18n-abide module looks at the `Accept-Language`

HTTP header. This is sent by the browser and includes all of the user’s preferred languages with a preference order.

i18n-abide processes this value and compares it with your app’s `supported_languages`

configuration. It will make the best match possible and serve up that language.

If a good match cannot be found, it will use the strings you’ve put into your code and templates, which are typically English strings.

## Wrapping Up

In our next post, we’ll look at how strings like “Hello, World!” are extracted, translated, and prepared for use.

In the third post, we’ll look more deeply at the middleware and configuration options. We’ll also test out our localization work.

## Previous articles in the series

This was part nine in [a series with a total of 12 posts about Node.js](https://hacks.mozilla.org/category/a-node-js-holiday-season/as/brief/). The previous ones are:

[Tracking Down Memory Leaks in Node.js](https://hacks.mozilla.org/2012/11/tracking-down-memory-leaks-in-node-js-a-node-js-holiday-season/)[Fully Loaded Node](https://hacks.mozilla.org/2012/11/fully-loaded-node-a-node-js-holiday-season-part-2/)[Using secure client-side sessions to build simple and scalable Node.JS applications](https://hacks.mozilla.org/2012/12/using-secure-client-side-sessions-to-build-simple-and-scalable-node-js-applications-a-node-js-holiday-season-part-3/)[Fantastic front-end performance Part 1 – Concatenate, Compress & Cache](https://hacks.mozilla.org/2012/12/fantastic-front-end-performance-part-1-concatenate-compress-cache-a-node-js-holiday-season-part-4/)[Building A Node.JS Server That Won’t Melt](https://hacks.mozilla.org/2013/01/building-a-node-js-server-that-wont-melt-a-node-js-holiday-season-part-5/)[Fantastic front-end performance, part 2: caching dynamic content with etagify](https://hacks.mozilla.org/2013/02/fantastic-front-end-performance-in-node-part-2-a-node-js-holiday-season-part-6/)[Taming Configurations with node-convict](https://hacks.mozilla.org/2013/03/taming-configurations-with-node-convict-a-node-js-holiday-season-part-7/)[Fantastic front end performance, part 3 – Big performance wins by optimizing fonts](https://hacks.mozilla.org/2013/03/fantastic-front-end-performance-part-3-big-performance-wins-by-optimizing-fonts-a-node-js-holiday-season-part-8/)

## About
[
Austin King ](http://ozten.com)

Seattle based non-dogmatic Artist / Programmer type human. Rogue web developer with the Apps Engineering team. Spell check is for the week.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

Manuel StrehlApril 2nd, 2013 at 10:22Austin KingApril 4th, 2013 at 00:53