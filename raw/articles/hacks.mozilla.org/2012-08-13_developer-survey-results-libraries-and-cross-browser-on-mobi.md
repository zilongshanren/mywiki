---
title: 'Developer survey results: libraries and cross-browser on mobile? – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/08/developer-survey-results-libraries-and-cross-browser-on-mobile/
author: Chris Heilmann
published: '2012-08-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

At Mozilla, we are dedicated to keep the web open and independent of a single company or technology. This means that users should have a choice of browsers and technology to use to go online and should not be blocked out because they can’t afford a certain device or are forbidden to change their browser.

In the world of mobile web development there is currently a massive debate going on about the need for support of various browsers seeing that the most successful phone systems both use the same browser engine. This is good, and we need this debate. It is not good though when developers block out users because they concentrate on targetting a browser. Sometimes this is not by choice of the developer – they are simply using tools that do that blocking for them and the usefulness of the tool outweighs the qualms developers have about that.

We are currently talking to library and tool developers and help them support more than one browser engine to prevent this. As a start of that process we wanted to get a glimpse of what people are using right now so we make sure we have the most impact when we help. This is why we conducted an online survey asking developers about their tools for mobile development.

590 developers took the survey and we are thankful for them spending their time giving us a lot to ponder and think about.

We are very aware that this is *not* a scientifically clean research and should be taken with a grain of salt (we haven’t asked how many times people used the tools or how much of their work is building mobile apps) but it gives us a good idea of what is going on.

So without further ado, here are the numbers as charts with a quick commentary:

## Platforms

A lot of developers showed their love for the web in this survey, but then again it was a survey initiated by Mozilla. Most likely an Apple-lead survey would have different results. iOS and Android are the follow-up and Windows Phone and Blackberry are less of a concern for the developers who filled the survey. This, of course, could differ greatly were we do to this survey targetted to different markets. Interesting that in the case of Android the amount of “must have” is higher than “focus” – the only platform showing this.

You can compare the results dynamically [here](http://jsfiddle.net/codepo8/EcuJG/5/).

What platforms are you targeting with your apps – Web |
|||||||||||||||||||||
|

What platforms are you targeting with your apps – iOS |
|||||||||||||||||||||
|

What platforms are you targeting with your apps – Android |
|||||||||||||||||||||
|

What platforms are you targeting with your apps – Windows phone |
|||||||||||||||||||||
|

What platforms are you targeting with your apps – Blackberry |
|||||||||||||||||||||
|

People may select more than one checkbox, so percentages may add up to more than 100%.

## Libraries

In the world of libraries jQuery and jQuery mobile very much took the lead with more than 200 more uses than the next follower Zepto.js. A lot of feedback was that developers don’t like libraries and use their own hand-rolled solutions on mobile instead. While it is good to see that libraries that work cross-browser are the most used ones (jQuery just [announced that they happily support Firefox mobile](http://jquerymobile.com/blog/2012/08/01/announcing-jquery-mobile-1-2-0-alpha/)), the high number of Sencha users is worrying and we’ll see how we can help make their cross-browser support better. Sencha was also mentioned a lot in the “why webkit only” question which shows that it is an important tool for developers.

What libraries do you use to build mobile web apps/sites? |
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|

People may select more than one checkbox, so percentages may add up to more than 100%.

All in all we collected 66 libraries (in order of popularity): jQuery, jQuery mobile, Zepto.js, Sencha Touch, JQTouch, XUI.js, Backbone, Mootools mobile, Lime.js, Sproutcore, Angular JS, Underscore, Bootstrap , Enyo, Modernizr, Dojo, handlebars, JO, Closure, Dojo Toolkit, GWT, Hammer.js, iScroll, require.js, YUI, Chibi, Ember.js, Kendo, Kinetic, Lungo.js, Nimblekit, Prototype, Wink, Adobe Air, Atto, Box2D, ChesterGL, Cobra, Crafty, Cujo, d3.js, Dart , Dojo Mobile, Dojo Mini, enhance.js, Eyebrow.js, fitml, gl-matrix, H5BP, JQMobi, Javelin, Jukebox, Knockout, MProject, Mootools, Openlayers, Path , Playcanvas, pointer.js, Raphael, Sugar.js, TerrificJS, Thorax, Titanium Mobile, Uxebu bikeshed, Wakanda

## Conversion frameworks

There is no doubt that Phonegap / Cordova rules this segment of the market followed by Appcelerator. Quite a lot of feedback was also people claiming that native apps should be coded natively. Being a web evangelist, I disagree as you can not convert from native to web but the other way around, but it is interesting to see that developers felt the need to have their say here.

Which frameworks do you use to convert apps to native apps? |
|||||||||||||||||
|

People may select more than one checkbox, so percentages may add up to more than 100%.

All in all we collected 13 conversion tools (in order of popularity): Phonegap, Adobe Air, Apache Cordova, Cocoon.js, Brightcove App Cloud, Mosync, Sencha Native SDK, appMobi, Flex Mobile, Mobileweb, Monotouch and backbone.

## Visual editors

Not many developers seem to use visual editors, which is probably because most of them are still in a “beta” or “alpha” stage. It would be interesting to do the same survey with Flash developers who are moving towards HTML5 and see if the numbers are higher. As it stands, Adobe Edge and Sencha Animator are the clear winners, and some of the entries were interesting including one “you got to be kidding me” :).

Do you use any visual tools/converters to build apps? If so, which? |
|||||||||||||
|

People may select more than one checkbox, so percentages may add up to more than 100%.

All in all we collected 17 editors (in order of popularity): Adobe Edge, Sencha Animator, Adobe Dreamweaver, Adobe Flash, Adobe Photoshop, Codiqua, Construct 2, Hype, Playcanvas , Radi, Rhodes, Telrik, Tiggzi, Tiler, Wakanda, Web Developer Add-on, WebMatrix

## Webkit only?

71% of developers filling out the survey said they test for more than Webkit browsers and in the general feedback section of the survey we had a lot of information as to how people are testing and what would make things much easier for them. This makes us happy of course.

Do you test on non-Webkit browsers? |
|||||||||
|
|
|

## Reasons to test for webkit only

The main reason here is a lack of time to test on other platforms which is understandable – we can assume that a lot of projects from a planning perspective have 99% iOS/Android written all over them. The “lack of incentive” number is high, too, which is understandable – if you can’t show the numbers, you don’t get the time to support. The high number of “not supported on hardware” is of course another very understandable reason and we wished there would be a way to change this.

## 5 comments

Bill KingAugust 14th, 2012 at 23:52ChrisAugust 15th, 2012 at 08:46ChrisAugust 15th, 2012 at 08:53Kyle HayesAugust 18th, 2012 at 08:09GeorgeAugust 20th, 2012 at 13:36