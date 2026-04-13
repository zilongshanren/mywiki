---
title: Webapplate – Maintainable web app template for Firefox OS and Chrome Apps –
  Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/09/webapplate-maintainable-web-app-template-for-firefox-os-and-chrome-apps/
author: Fred Lin
published: '2014-09-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There are many powerful tools and technologies surrounding the Web, and we can reuse them to develop cross platform mobile and desktop apps, especially in light of installable apps appearing on platforms such as Firefox OS. This article looks at the best way to do this, and presents Webapplate, a powerful new template to help facilitate this.

## Why invent the wheel (for the new frontier)

As is the nature of the whole web, web apps are simple to write but hard to get done right. Even though the Web doesn’t provide an SDK or simple ready-to-use templates like other mobile platforms, you can still come out with a workable web app from candidates like [Mozilla Open Web Apps](https://marketplace.firefox.com/developers/), [Chrome Apps](https://developers.google.com/chrome/apps/), or [Apache Cordova](http://cordova.apache.org). But developers who want to quickly build a web app usually take longer time than say, an iOS developer.

Here is the state of web app support by those candidates:

- Firefox (desktop), Firefox OS, Firefox for Android support hosted web apps. Those web apps could be hosted on a static or dynamic web server just like normal web sites. Hosted web apps don’t allow some certified web APIs such as the TCP socket API because of security concerns.
- Firefox OS and Chrome (desktop) support packaged web apps with different APIs for different purposes, because currently they focus on different types of devices.
- Cordova provides device adapters for many platforms, including Android, iOS and Firefox OS.
- Google has its Cordova variant to adapt Chrome App’s specific APIs to run on Android devices.

In quick summary, the web app concept is not totally unified yet, but powerful enough to compete with native apps. Currently packaged web apps are mainstream because of the security concerns with new web API’s. Mozilla is mainly focusing on exposing new web APIs to mobile devices, Google is developing new web APIs for desktop. Apache Cordova is a good container to expose web APIs to different platforms.

To make things harder, provided examples are often focused on teaching you how to pick up new web APIs rather than utilizing proper web app concepts with your development process.

I’ve had the chance to join the development of an evolving web app project called [Gaia](https://github.com/mozilla-b2g/gaia), the Firefox OS user interface. The Gaia project contains the very first Mozilla installable web app implementation, including apps for music, photo gallery, e-mail, calendar and much more. According to [GitHub’s pulse](https://github.com/gasolin/gaia/pulse/) monthly, there are about 850 commits per month to the Gaia web apps. In the Gaia project, Mozilla developers and community members devoted lots of time and effort to bring it from the prototype stage to a shippable product within 2 years, and iteratively make it a competitive option for smartphone consumers. As a living large web app project, there are many lessons that can be learned from it, and applied to general web app development.

## Introducing webapplate

Like other software projects, there are many things beside commiting code to develop a web app, such as:

- How to organize the source code
- How to handle library dependencies
- How to keep the coding style in convention
- How to optimize web app load performance
- How to unit/integrate test your web app
- How to localize your web app
- How to automate those processes

Those are topics that need to be resolved to develop a quality web app. In Gaia we have addressed these issues by utilizing a bunch of [build scripts (Makefiles)](https://leanpub.com/gaiafromabove/read#leanpub-auto-chapter-4---build-script).

You may wonder why we didn’t use [Grunt](http://gruntjs.com/) or [gulp](http://gulpjs.com/) for building? The answer: at the time Firefox OS was started, these tools didn’t exist. And the module owner wanted to make the core build process run in a Firefox extension one day.

For general web app development, we didn’t have to follow those constraints. And we could do some experiments rapidly by reusing 3rd-party tools and libraries. From 2013, I’ve initiated a side project called [webapplate](http://webapplate.github.io/), the open-sourced web app template that attempts to make Gaia’s solutions compatible with emerging toolkits like [npm](http://npmjs.org/), [Grunt](http://gruntjs.com/) and [Bower](http://bower.io/). It also tries to transport good practices from Gaia to make new web apps more maintainable.

## How to setup webapplate

Webapplate utilizes many powerful tools. With [node.js](http://www.nodejs.org/), Grunt, Bower, [Karma](http://karma-runner.github.io/0.12/index.html), [Mocha](http://visionmedia.github.io/mocha/) and [l20n](http://l20n.org/), we come out with a maintainable *full stack* and self-contained web app template with JavaScript. So you could just [copy or download the webapplate from Github](https://github.com/webapplate/webapplate), and develop and deploy to a hosting server or correspondent web app store.

You need to install node.js in your desktop first. With Node.js installed, you’ll have the `npm`

tool to manage Node.js modules. Now run this command:

```
$ npm install -g grunt-cli bower karma
```

to install the primary tools.

`Grunt`

is a JavaScript task runner tool (like Make) and `grunt-cli`

is its command interface. [Gruntfile.js](https://github.com/webapplate/webapplate/blob/master/Gruntfile.js) file is similar to Makefile, but written in Javascript.

`Bower`

is a management tool for the front-end libraries. It helps developer manage different library versions. In webapplate, Bower will download client side libraries into the `public/vendor`

folder when you run

```
$ bower install
```

command.

`Karma`

is the test runner that runs test code for each of the browsers. [karma.conf.js](https://github.com/webapplate/webapplate/blob/master/karma.conf.js) defines the detail settings to specify how the test runner goes.

Next, enter the webapplate folder and run:

```
$ npm install
```

`npm`

will reference [package.json](https://github.com/webapplate/webapplate/blob/master/package.json) to install all dependent node modules. The command will trigger `Bower`

to install client-side library dependencies as well.

Then you are all set! What you get is:

- Pre-commit lint checking
- Firefox and Chrome web app-compatible templates
- Library dependency management
- Client-side localization framework
- Unit test and mock framework
- Deployable web server

If you use Firefox nightly, you could open the `webapplate/public`

folder as a packaged app in the [WebIDE developer tool](https://developer.mozilla.org/en-US/docs/Tools/WebIDE).

WebIDE allows you to edit, debug or execute your web app in the Simulator or on the device, with your favorite Firefox Developer Tools.

With the [Chrome Apps & Extensions developer tool](https://chrome.google.com/webstore/detail/chrome-apps-extensions-de/ohmmkhmmmpcnpikjeljgnaoabkaalbgc), you can import the `webapplate/public`

folder as a Chrome App and check the UI on desktop.

## Pre-commit lint checking

The very first good practice that Gaia and webapplate provide is git pre-commit lint checking.

Since in Gaia every commit needs to get reviewed and verified by the module owner before the code is checked in, we have followed the [Google JavaScript style](https://google-styleguide.googlecode.com/svn/trunk/javascriptguide.xml) conventions. At that time we used [gjslint](https://developers.google.com/closure/utilities/docs/linter_howto) to test it. It sounds good but actually forcing people to follow the exact same discipline manually is hard; asking the reviewer to pick through those style errors is another waste of time. So some genius introduced a git pre-commit hook to check several kinds of lint errors when the developer tries to commit their code, and provide a [whitelist](https://github.com/mozilla-b2g/gaia/blob/master/build/jshint/xfail.list) for the code that isn’t fully lint-free but should be allowed. Currently in Gaia we have pre-commit checks for JavaScript, CSS and JSON! This is a big relief.

Currently webapplate utilizes code quality and style checking for JavaScript, JSON via [JSHint](http://www.jshint.com/docs/), [JSCS](https://github.com/jscs-dev/node-jscs) and [JSONLint](https://github.com/zaach/jsonlint).

It has exactly the same settings as Gaia for JSHint and also comes with the [whitelist](https://github.com/webapplate/webapplate/blob/master/.jshintignore). Gaia is also planning to migrate to *jscs* to replace *gjslint*. If you use `git`

for version control, run:

```
$ grunt githooks
```

to bind the git pre-commit code style check to your development process.

## Firefox OS- and Chrome App- compatible templates

Webapplate uses [HTML5 mobile boilerplate](https://github.com/h5bp/mobile-boilerplate) as the template base, and adds web app install helpers, icon links and usemin annotation for web app optimization on top. The main web app source is located in the [public/](https://github.com/webapplate/webapplate/blob/master/public/) folder. You could check the [webapplate wiki](https://github.com/webapplate/webapplate/wiki/Structure) to see the full webapplate structure.

Currently, Firefox web apps use [manifest.webapp](https://developer.mozilla.org/en-US/Apps/Build/Manifest) and Chrome Apps use [manifest.json](http://developer.chrome.com/apps/manifest.html) as the manifest file. The syntaxes are mutually compatible, except the localization part (we’ll address this issue later).

After you edit one of these files, use:

```
# firefox to chrome
$ grunt f2c
```

or

```
# chrome to firefox
$ grunt c2f
```

to overwrite `manifest.webapp`

with `manifest.json`

, or viceversa.

To generate a Firefox OS packaged app or Chrome App, run this command:

```
$ grunt pack
```

to package your web app to an uploadable zip file. With the default settings, webapplate-generated packaged web apps could be uploaded to the [Firefox Marketplace](http://marketplace.firefox.com/) and the [Chrome App store](https://chrome.google.com/webstore/category/apps).

## Library dependency management

For Gaia we manage development tools via `npm`

and generally don’t use many 3rd-party client side libraries. We host commonly-used libraries between apps in a `shared/`

folder, and then copy them in at build time via a build script.

webapplate defines these libraries in [package.json](https://github.com/webapplate/webapplate/blob/master/package.json), uses `npm`

to require build tools, and doesn’t assume any app framework (e.g. [Backbone](http://backbonejs.org/) or [Angular.js](https://angularjs.org/), or a UI framework such as [Bootstrap](http://getbootstrap.com/).) Client-side libraries could be managed via Bower in [bower.json](https://github.com/webapplate/webapplate/blob/master/bower.json).

## Client side localization framework

Since web apps might be run without an Internet connection, we can’t count on the server to detect multiple languages. Currently Firefox OS uses [navigator.mozL10n](https://developer.mozilla.org/en-US/docs/Web/API/Navigator.mozL10n) and Chrome Apps uses [chrome.i18n](https://developer.chrome.com/extensions/i18n) for localization. Both of them are non-standard.

In webapplate we take the [l20n](http://l20n.org/) library to address the client-side localization issue. l20n is crafted by Mozilla and the developers are currently working on enhancing the Firefox OS localization framework as well.

Check out [index.html](https://github.com/webapplate/webapplate/blob/master/public/index.html); the localization syntax looks exactly like what we used in Gaia:

```
```# Hello WebApplate


The locale file however is in a different format, [locales.en.l20n:](https://github.com/webapplate/webapplate/blob/master/public/locales/locales.en.l20n)

```
```

Also, check out the [Multiple Language Support Framework](https://github.com/webapplate/webapplate/wiki/Structure#4-multiple-language-support-framework) section for how l20n is integrated with webapplate.

## Unit test and mock framework

Gaia uses its own test-agent to trigger unit tests on Firefox. Gaia uses the [Mocha](http://visionmedia.github.io/mocha/) test framework, [Chai](http://chaijs.com/) assertion library and the [Sinon](http://sinonjs.org/) test helper library for unit tests.

Webapplate uses the above unit test libraries plus the [Karma](http://karma-runner.github.io/0.12/index.html) test runner to run unit tests on all mainstream browsers.

## Deployable web server

For developing Firefox OS hosted web apps, we need a working web server and maybe some dynamic web server support. Now that’s what we call the 21st century: it is possible to write server-side code in JavaScript as well.

Running the command:

```
$ grunt server
```

will trigger the [Express](http://www.expressjs.com/)-powered server with [django-like Swig](http://paularmstrong.github.io/swig/) template support. It’s been pre-configured for performance. Measure with [YSlow](http://developer.yahoo.com/yslow/) and you’ll get a pretty good grade for your web site.

Webapplate has been tested on some free dynamic web page hosting providers such as openshift, heroku and appfog. Check the [deployment](https://github.com/webapplate/webapplate/wiki/Deployment) section to find out more details.

If you like to host your web apps on a static web server, run:

```
$ grunt static
```

to generate optimized web pages for hosting.

If you want to deploy your web app on a GitHub page (as a free static hosting server), run:

```
$ grunt github
```

## Start your new web app project with webapplate!

Webapplate is the web app template that borrows good practices for web app maintenance from the Gaia project. It provides ready-to-use Firefox OS and Chrome App support, an integrated toolbox to optimize your web app and maintain quality, and uses JavaScript through client/server side build/test frameworks. If you are about to make a web app or want to see how to maintain a web app, webapplate is a good start.

## References

## About
[
Fred Lin ](http://www.gasolin.idv.tw)

Fred Yu-Min Lin, a.k.a. "gasolin", is a front-end web developer working on "Gaia", the user interface for Firefox OS. He is also the book author of Android and FIrefox OS Gaia development. He regularly blogs at [http://blog.gasolin.idv.tw](http://blog.gasolin.idv.tw) and gives presentations to share open web and mobile technologies.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 14 comments

Ivan DejanovicSeptember 5th, 2014 at 01:48Robert Nyman [Editor]September 5th, 2014 at 06:35AdamSeptember 5th, 2014 at 05:29Robert Nyman [Editor]September 5th, 2014 at 06:15AdamSeptember 5th, 2014 at 10:17AdamSeptember 5th, 2014 at 10:18Fred LinSeptember 5th, 2014 at 19:00Doug ReederSeptember 5th, 2014 at 12:23Fred LinSeptember 5th, 2014 at 19:13VincentSeptember 6th, 2014 at 05:26Fred LinSeptember 8th, 2014 at 01:35M. Edward (Ed) BoraskySeptember 29th, 2014 at 16:09Fred LinSeptember 29th, 2014 at 19:37M. Edward (Ed) BoraskySeptember 29th, 2014 at 22:21