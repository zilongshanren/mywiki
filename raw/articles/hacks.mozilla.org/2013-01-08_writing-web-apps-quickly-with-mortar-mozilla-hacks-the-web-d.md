---
title: Writing Web Apps Quickly With Mortar – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/01/writing-web-apps-quickly-with-mortar/
author: James Long
published: '2013-01-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With the introduction of [Firefox OS](http://www.mozilla.org/en-US/firefoxos/), development of an [open apps marketplace](http://www.mozilla.org/en-US/apps/), and a push to implement powerful [web APIs](https://wiki.mozilla.org/WebAPI) for closer hardware integration, Mozilla is serious about web apps. We believe that the web can deliver an experience similar to native apps, even on mobile.

We can’t forget about the most important piece, however: a good developer ecosystem. We need to provide various tools to make it easy for both beginners and experts to write web apps and deploy them.

This is why we’ve created [mortar](https://github.com/mozilla/mortar/), a collection of app templates that provide starting points for different kinds of apps and tools to manage and deploy them.

A few weeks ago, Pierre Richard [wrote a post](https://hacks.mozilla.org/2012/12/fxosstub-a-minimalists-working-example-of-the-design-guide-rules-for-firefox-os/) here about his experiences getting started writing apps for Firefox OS. There’s some good stuff in his post, including his critiques of mortar. He felt mortar was too complex and introduced a different [starting point](https://github.com/Jaxo/fxosstub) for writing web apps for Firefox OS.

This post will loosely respond to some of his points, introduce mortar, and explain why I think it is a valuable starting point for writing web apps for both beginners and experts. A detailed walkthrough of mortar is provided at the end in a screencast.

## Why Are Templates Useful?

Mortar is more than just a bunch of HTML, CSS, and JavaScript. As described later in this post, it comes with various other tools for automating tasks, such as deployment and minifying and concatenating JavaScript and CSS. These tools are necessary when you want to release your app and maintain it.

If you’re someone who really enjoys simplicity, you might initially find mortar too complex. I’m definitely someone who wants to boil things down to its simplest form, rejecting unnecessary complexity. We’ve worked hard to make sure that we only include things in mortar that prove to be very useful when building and deploying a web app.

So I encourage you to learn about the tools mortar comes with, especially if you think you don’t need it. Mortar is our expression of good web development practices, so it’s also a chance to learn about modern tools and good ways to build web apps. Just as Django or Ruby on Rails may seem complex at first, you pay off your initial investment later on.

## The Technology Within Mortar

Mortar templates are pre-built to help you write web apps quickly. These aren’t specifically Firefox OS apps. We want you to build web apps that can run anywhere the web is. Firefox OS is a good place for a web app, but the mortar templates aren’t specifically targeting Firefox OS (even if some of the more advanced templates borrow a few styles from it).

All of the mortar templates come with the following:

- A project structure (folders for css, js, etc)
- Some initial well-formed HTML, JavaScript, and files like manifest.webapp
[require.js](http://requirejs.org/)to manage javascript[volo](http://volojs.org/)for a development server, css/js optimizations, deployment, and other tasks- Some initial js libs: zepto, mozilla’s
[receipt verifier library](https://github.com/mozilla/receiptverifier#readme), and a cross-platform library to[install web apps](https://github.com/wavysandbox/install)

In addition, an installation button is provided (but commented out by default) in case you want to test your app as an installed app (or let users install it outside of an app store). All you have to do is uncomment one line of HTML. This, in combination with the pre-built manifest.webapp file, makes it easy to build an app.

Here’s what your app looks like when you start it from a template:

All of the static files, like HTML, CSS, and JavaScript, are under the `www`

directory. We live one level up from this so that we can use tools like [volo](http://volojs.org/) and [grunt](http://gruntjs.com/), and if you need to add a server-side component it’s easier. The `node_modules`

and `tools`

directories are only for volo, and you can ignore them.

We chose to use [require.js](http://requirejs.org/), a JavaScript module system, because it’s good practice to write JavaScript in modules. It’s not an obscure library; it implements the [Asynchronous Module Definition](http://requirejs.org/docs/whyamd.html) standard for writing modules which is extremely well-known in the javascript community. The module you should start writing JavaScript in is at `www/js/app.js`

.

Besides managing your Javacript dependencies, modules let us easily compress and concatenate all your JavaScript into one minified file, with zero extra work on your part. In fact, it’s so easy that it’s wrapped up in a [volo](http://volojs.org/) command for you. Just type `volo build`

in your project and all your JavaScript is concatenated into one file and minified (it also does this with your CSS).

[Volo](http://volojs.org/) is a tool much like [grunt](http://gruntjs.com/) which simply automates tasks at the command line. We use volo because it integrates nicely with require.js. An example command is `volo serve`

, which fires up a development server for your app. [View this documentation](https://developer.mozilla.org/en-US/docs/Apps/App_templates#What_Now.3F) for more volo commands available.

Volo lets you easily deploy your site to github. After customizing `www/manifest.webapp`

for your app, simply do:

`volo build`

`volo ghdeploy`


Your optimized app is now running live on github, and is ready to submit to the marketplace!

## Games and Layouts

Everything described above is applicable to all apps, but we also want to help people who want to write specific kinds of apps. This is why we’ve created multiple templates, each catering to a specific need:

[mortar-app-stub](https://github.com/mozilla/mortar-app-stub): a minimal template that only has a little pre-built HTML (a blank canvas for any type of app)[mortar-game-stub](https://github.com/mozilla/mortar-game-stub): a minimal template that comes with some basic game components[mortar-list-detail](https://github.com/mozilla/mortar-list-detail): a template like app-stub but also includes a layouts library and a basic list-detail type interface[mortar-tab-view](https://github.com/mozilla/mortar-tab-view): a template like list-detail but the default interface is a tabbed view

We have a blank canvas (app-stub), a game template (game-stub), and two other templates that come with pre-built layouts.

This is what the game template looks like. It looks pretty boring, but it’s rendered using requestAnimationFrame and you can control the box with the arrow keys or WASD. In the future, we might include image loading and basic collision detection.

The list-detail template is below. It comes with a pre-built layout that implements a list-detail interaction where you can touch a list item and drill down into the details. You can also add new items. This data-driven functionality is powered by [backbone.js](http://backbonejs.org/). We are still improving the design. (The tab-view template looks similar to the list-view shown here.)

The layouts library is [mortar-layouts](https://github.com/mozilla/mortar-layouts), and it’s something we came up with to make it really easy to build application UIs. To me, this might be the most exciting part of mortar. I won’t go into too much detail here, but it uses [x-tags](http://www.x-tags.org/) and other new HTML5/CSS3 features to bring a native-feeling application UI to the web. View [documentation](https://github.com/mozilla/mortar-layouts#mortar-layouts) and a [live demo](http://mozilla.github.com/mortar-list-detail/) (and the [source for the demo](https://github.com/mozilla/mortar-list-detail/blob/master/www/index.html)).

The layouts library and the two templates that come with layouts are in beta, so keep in mind there are minor bugs. The biggest problem is the lack of design, and we will be working on integrating better styles that reflect Firefox OS (but are easily customizable with CSS!).

## Future Work for Mortar

Mortar is relatively new, and it needs time to be fully documented and fleshed out. We are working on this actively.

We are also fine-tuning our templates to figure out what the best starting points are for each one. Admittedly, having the big blue install button be the default screen for the app-stub was a mistake, which has been fixed. Now you get a [short helpful message](http://mozilla.github.com/mortar-app-stub/) with links of what else you can do.

Most of the work we have left is with the list-detail and tab-view templates, and figuring out how to deliver useful layouts to developers. We don’t want to force a big framework on them, but feel strongly that we need to help them develop application UIs.

We love feedback, so feel free to [file an issue](https://github.com/mozilla/mortar/issues) to get a conversation started!

## Screencast

I made a screencast which walks through mortar in detail and shows you how to use require.js, volo, and other things that it comes with. Watch this if you are interested in more details!

## 11 comments

Schalk NeethlingJanuary 8th, 2013 at 10:44AndrewJanuary 11th, 2013 at 05:13Fabricio C ZuardiJanuary 11th, 2013 at 16:24James LongJanuary 11th, 2013 at 22:52SokratisJanuary 13th, 2013 at 05:03James LongJanuary 14th, 2013 at 09:01SokratisJanuary 14th, 2013 at 09:31SokratisJanuary 13th, 2013 at 09:50James LongJanuary 14th, 2013 at 09:02SokratisJanuary 16th, 2013 at 12:39James LongJanuary 17th, 2013 at 08:15