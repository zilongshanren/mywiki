---
title: The Missing SDK For Hybrid App Development – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/10/the-missing-sdk-for-hybrid-app-development/
author: Adam Bradley
published: '2014-10-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Hybrid vs. native: The debate has gone on, and will go on, for ages. Each form of app development has its pros and cons, and an examination of the key differences between the two methods reveals that a flat correlation is like comparing apples to oranges. Many hybrid app developers understand that they’re not starting on a level playing field with native developers, but it’s important for them to understand exactly how that field fails to be level. We should analyze the differences at the app development framework level, instead of simply comparing hybrid to native.

## Native App Development

Native software development kits (SDKs) come prepackaged with the required tools to compile and sign apps–all that boring stuff that “just works.” Their canned templates and the common code they provide determines “how” an app works, which are hugely beneficial features hiding in plain sight.

For example, Apple’s own development environment, Xcode, is a suite of tools that make it easier to develop software for Apple platforms. As soon as you launch Xcode, it provides a list of templates for a new project. Let’s create an iOS tabbed application and see just how many tools native app developers have available to them from the start.

After plugging in a few settings, I quickly have a working tabbed app that can be run within a minute of Xcode’s launch. Awesome! The easy part is done, and now it’s time to sport the hoodie and headphones and focus on my goal of creating a best-selling iOS app.

![](../../assets/16705be856dc18a1.png)


Let’s drill into this a little further and take a look at what Xcode built for me, without me even having to give it a second thought. The app fills 100% of the device’s display; the tabs are aligned to the base with a gray background; one tab is highlighted blue, the other one gray, with icons on top of the tab’s title. Event listeners are added to the tab buttons, and when I click the second tab, it then turns blue, and the other one turns gray, along with switching out the content for the second view.

After a little more development, my app will have a separate navigation stack for each tab; the back button will show when needed; the title of each view will switch out in the header; and smooth transitions will happen as I navigate between different views. Fonts, colors, gradients, and styles will all follow what an app should look like on that platform. By expanding folders in Xcode’s project navigator, I notice the ridiculous amount of files that were placed there for me. I have no clue what they do and honestly don’t really care, but they’re actually extremely important: They’re the files that made the development of my app so seamless.

## Hybrid App Development

Honestly, though, I’m a web developer. My organization isn’t filled with Objective-C and Java developers ready to build multiple apps with the ultimate goal of just trying to be the same app (but built entirely differently, from the ground up). I have existing HTML/CSS/JS skills, and I want my app to hit not only Apple’s App Store, but Google’s Play Store and all the others. Instead of locking myself into each platform and having to learn and maintain multiple proprietary languages, hybrid app development makes more sense, given my skill set and my time constraints.

Don’t let hybrid app development scare you. In its simplest form, a hybrid app is still just a web browser, but without the URL bar and back button. This means you can build a full-fledged app using HTML/CSS/JS but still have it work like a native app, with all the same superpowers, like accessing bluetooth, GPS, camera, files, device motion, etc. Hybrid apps offers the best of both worlds.

## Let’s Build A Hybrid App

For my use-case, I’ve decide a hybrid app is perfect, so let’s fire up….wait, there is no Xcode for hybrid apps! Where do I get all those files that makes my app do app things? Where’s the built-in UI, cool animations, and smooth transitions? The disadvantage to hybrid app development is that those starting with the web platform have to start from scratch. It’s the Wild West, and each developer is on his or her own.

I absolutely love the web platform. It provides a core set of tools to not only share information but consume it. However, the web platform offers only the basic building blocks for structuring content; styling and interacting with that content; and navigating between documents. The core of the web platform does not provide pre-packaged libraries like those in iOS and Android. At the lowest level, a web browser represents one “view” and one navigation/history stack. This is another area in which native apps have an advantage, and hybrid devs burn up time generating code to give browsers the ability to handle multiple views with multiple stacks.

Hybrid app developers quickly find themselves dealing with countless issues just to get their heads above water: figuring out the CSS to fill 100% of the viewport, sticking the tabs on the bottom and hovering content, adding event listeners, switching active states for icons and views, keeping track of navigation stacks of each tab, implementing touch gestures, generating a common way to navigate and transition between view, using hardware accelerated animations for the transitions, removing 300ms delays, knowing when to show or hide the back button, updating and animating the header title, interacting with Android’s back button, smooth scrolling through thousands of items, etc. All of these things come with native SDKs. And as an app grows, it’ll seem as though recreating natural, native interactions is a constant uphill battle–all of which native developers rarely think about, because for them it was baked in from the start.

I believe the solution is to use a framework/library that levels the playing field, giving hybrid developers a toolkit similar to that of native developers. Most developers have a sense of pride in writing everything themselves, and there are certainly plenty of use-cases in which frameworks and/or libraries are not required. But when it comes to hybrid app development, there is a whole world of common code being recreated by each developer, for each app, and that’s a lot of work and time to invest in something that native developers already get.

[Cordova](https://cordova.apache.org/) (the guts to [Phonegap](http://phonegap.com/)) is the predominant open-source software to morph the web platform into a native app. But just like the web platform, it only offers the basic building blocks, rather than a built-in framework to start with.

Frameworks and libraries amplify app development and allow devs to focus on how their apps work, not the logic of how apps work.

## Hybrid Development Frameworks: Hybrid’s Missing SDK

I define frameworks and libraries as any software package that increases productivity. In my experience, hybrid developers’ main frustration lies not in creating their app, but rather in getting their app to work like an app, which is a subtle, yet significant difference.

With the advent of development frameworks focused on hybrid app development, developers finally have that missing SDK that levels the playing field with native. Cross-platform frameworks that embrace HTML/CSS/JS allow web developers to take their skills to app development. To increase productivity, hybrid app development frameworks should not only stick to the standards with pretty CSS and markup; they should also provide a MVC for serious, large-scale app development by a team.

Frameworks like the [Ionic Framework](http://ionicframework.com/) provide a common set of logic used to create apps, which isn’t already baked into the web platform *(full disclosure: I am a co-creator of Ionic and a core contributor to AngularJS Material Design)*. Rather than inventing yet another MVC, Ionic chose to build on top of

[AngularJS](https://angularjs.org/), which has proven itself to be a leader among popular front-end frameworks in the last few years. Ionic is backed by a

[large and active community](http://forum.ionicframework.com/),

[solid documentation](http://ionicframework.com/docs/), and its own

[command-line tool](http://ionicframework.com/getting-started/)to increase productivity

*(the CLI isn’t required but is highly recommended)*.

Ionic’s use of AngularJS directives to create the user-interface allows for fast development, but most importantly, it’s highly customizable, through its use of [Sass](http://sass-lang.com/) and simple markup. If you’re unfamiliar with AngularJS, Ionic offers a great way to learn it quickly, via numerous [examples](http://codepen.io/ionic/public-list/) and [templates](https://github.com/driftyco/ionic-cli#starting-an-ionic-app).

Google’s [Polymer project](http://www.polymer-project.org/) and [Mozilla Brick](http://brick.mozilla.io/) are built on top of the cutting-edge [Web Components](http://www.w3.org/TR/components-intro/) specification. As with AngularJS directives, Web Components offer a great way to abstract away complex code with simple HTML tags.

Other proven hybrid development frameworks that have been around longer and offer their own powerful MVC/MVVM include [Sencha Touch](http://www.sencha.com/products/touch) and [Kendo UI](http://www.telerik.com/kendo-ui). Both frameworks come with a large list of built-in components and widgets that enable developers to build powerful apps that work on iOS, Android, BlackBerry, Windows Phone, and more.

I do not consider front-end frameworks, such as [AngularJS](https://angularjs.org/), [Ember](http://emberjs.com/), and [Backbone](http://backbonejs.org/) to be hybrid app development frameworks. While I highly recommend front-end frameworks for large-scale app development, they’re focused on the logic, rather than the user interface.

Frameworks like [Twitter Bootstrap](http://getbootstrap.com/) and [Foundation](http://foundation.zurb.com/) offer a great user interface and responsive design capabilities. However, CSS frameworks focus on the UI and a responsive design pattern; but a UI alone still requires each developer to recreate the way a native app “works.”

App frameworks abstract away the complexity of building an app and offer developers both the core logic and the UI, similar to what iOS and Android provide. I believe it is important to embrace the web standards and the web platform at the core, so it can be easily run from Cordova and built for multiple platforms (including a standard web browser).

## Software Engineering: Still Required

Hybrid app development frameworks have come a long way in the last few years, and they have a bright future ahead of them. However, [Developing Hybrid Apps Still Requires Actual Software Engineering](http://blog.devgeeks.org/post/97524150749/developing-hybrid-apps-still-requires-actual-software), just as developing native apps does. As in any form of web development, if only a few hours are put into a project, the result is rarely a highly polished and production-ready piece of work.

Hybrid fans sometimes offer the impression that frameworks create a unicorn and rainbow filled wonderland during development, which may mislead new developers. Just because you can write once and deploy everywhere doesn’t mean you’re exempt from the rules of software development. Hybrid offers many benefits, but as with so many things in life, cutting corners does not produce quality results, so please don’t claim all is lost after minimal effort.

## Making An Accurate Comparison

The comparison of a hybrid app without a framework to a native app isn’t a fair one. To accurately examine hybrid vs. native development, we need to analyze each method at the framework level (hybrid with a framework vs. native, like Ionic Framework vs. iOS or Polymer vs. Android). As for hybrid vs. native: It’s a matter of studying your use-case first, rather than a choosing a definitive level of abstraction over everything else. It all ends up as 1s and 0s anyway, so jumping up another level of abstraction (HTML/CSS/JS) may be the right fit for your use-case and organization.

I often feel that opinions regarding hybrid app development were formed well before hybrid was ready for prime time. The world has quickly been transitioning to faster devices and browsers, as well as improved web standards, and there’s no signs of either one slowing down. There is no better time than now to leverage your existing web development skills and build quality apps by standing on the shoulders of hybrid SDKs.

## About Adam Bradley

Co-creator of [Ionic Framework](http://ionicframework.com/) and [AngularJS Material Design](https://material.angularjs.org/#/) team member. Regularly writes and speaks about hybrid development. Proud dad, husband, veteran, and dog's best friend. Based in beautiful Madison, WI.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 7 comments

BrentOctober 1st, 2014 at 14:12Ben bakerOctober 1st, 2014 at 14:57FredOctober 3rd, 2014 at 00:30niutechOctober 4th, 2014 at 15:28MatthewOctober 8th, 2014 at 09:27tysonOctober 10th, 2014 at 10:57Robert Nyman [Editor]October 13th, 2014 at 02:07