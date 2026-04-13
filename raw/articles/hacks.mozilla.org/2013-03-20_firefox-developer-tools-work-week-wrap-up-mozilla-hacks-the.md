---
title: Firefox Developer Tools work week wrap-up – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/03/firefox-developer-tools-work-week-wrap-up/
author: Jeff Griffiths
published: '2013-03-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last week in Sunnyvale we had the first Developer Tools work week to include the recently-integrated Jetpack team ( for a slightly different take on the week, see [Paul’s post](http://paulrouget.com/e/devtoolsnext/). ). And what a week! I was a bit shocked by how many things I thought were just interesting ideas suddenly became real things that actually worked. By Friday morning we had some amazing demos from the team, which I will try to group together according to theme:

### Remote everything, everywhere.

Within the next 3 months we will land remote protocol support for all of the development tools we ship. The remote protocol is a network client/server protocol that exposes the developer tools to each other external tools like editors as well as Firefox on Android and Firefox OS. We had some awesome demos that leverage or extend these capabilities:

- Based on Heather Arthur’s work on implementing remote style editing, Paul Rouget amazed us and soon many others with remote CSS editing from popular editor Sublime Text 2: (
[Tweet](https://twitter.com/paulrouget/status/312250120307613696),[Youtube](https://www.youtube.com/watch?v=UrnB8lZnx4I&feature=player_embedded),[Github](https://github.com/paulrouget/firefox-remote-styleEditors)). - Joe Walker showed off how to run gcli commands remotely between different instances of Firefox Desktop.
- Jim Blandy walked us through some important platform fixes that will enable content process debugging on Firefox OS. This will allow us to support remote on-device debugging of B2G apps.

### Revolutionary Dev Tools hacks

Many team members got a ton of work done on their existing projects and showed us some great enhancements by the end of the week:

- Mihai Sucan showed off progress on the Global Console, which now understands all network requests and also supports stdin/stdout and some handy timing utilities.
- Anton Kovalyov showed off an initial integration of Codemirror as the source editor for the devtools, replacing the current Orion editor.
- Nick Fitzgerald got sourcemaps working with the debugger and gave us a demo of Coffeescript debugging.
- Joe Walker re-factored gcli commands to de-couple processing from presentation, making it much easier to implement multiple commands that use a common data formatter.
- Last but not least, Victor Porov walked us through a fully-operational Network Panel that is nearly ready to land!
- Stephen Shorlander showed off some great first steps on defining what
[in-browser web app development](https://www.dropbox.com/sh/zhpdcuwh2f1mz87/CVHwJWjW0C)might look like.

### Developer tools + Jetpack == Super Powers!

On Tuesday Paul Rouget walked us through the fledgling developer tools API and challenged the Jetpack team to see how working with the developers could be made simpler. By Friday Irakli answered the challenge by showing us a Jetpack add-on called ‘Add-on Pad’ for live-coding SDK-based add-ons.

Dave Camp had a slightly different take on Jetpack’s possibilities and by the end of the week was able to show off a version of the Developer Tools code-base that could be dynamically re-loaded from disk using Jetpack’s CommonJS loader, without the need to re-build or even restart Firefox.

Not to be outdone, Dave Townsend made some [tweaks to tilt mode](http://www.oxymoronical.com/blog/2013/03/Hacking-on-Tilt) to expose it to add-ons and even scratchpad hacks to change how tilt visualizes a page based on arbitrary code that could be injected either via an add-on or from scratchpad.

Paul also released a new version of his excellent Firefox Terminal add-on recently which you should [go install it immediately](http://paulrouget.com/e/fxterminalv3/)! Right now! I’ll still be here when you get back.

### Add-on developer love

The developer tools team has been focused like a laser on improving life for web developers, but Firefox itself is created and extended with web technologies like JS and CSS. At this first Devtools work week that included the Jetpack team we saw some really promising work:

- Eddy Bruel
[tackled several bugs](https://blog.mozilla.org/ejpbruel/2013/03/18/what-i-worked-on-during-the-devtools-work-week/)I don’t completely understand and by the end of the week showed us debugging*for almost all browser chrome and add-on Javascript code*. There are still some known limitations to work through ( not all add-ons or content scripts can be debugged currently ) but the Browser is already very useful to developers as of today’s Nightly build. - Mihai Sucan and Alexandre Poirot made changes to both the SDK and the Global Console that will pipe any calls to console.log in Jetpack code to the Global Console, greatly improving ‘printf’-style debugging for add-on developers.

Some of these hacks landed last week during the work week, many will be landing over the next couple weeks. If you’d like to get involved in driving these features home, find us in #devtools and #jetpack on irc.mozilla.org or the Developer Tools project mailing list at mozilla.dev.developer-tools.

## About
[
Jeff Griffiths ](http://canuckistani.ca/)

Jeff is Product Manager for the Firefox Developer Tools and occasional Open Web hacker, based in Vancouver, BC.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 21 comments

Michael BashkirovMarch 20th, 2013 at 07:04Jeff GriffithsMarch 20th, 2013 at 09:18Omega XMarch 20th, 2013 at 12:49Jeff GriffithsMarch 20th, 2013 at 13:32Omega XMarch 23rd, 2013 at 03:34WebDevMarch 20th, 2013 at 20:44Jeff GriffithsMarch 20th, 2013 at 20:59aL3xaMarch 21st, 2013 at 06:29Jeff GriffithsMarch 21st, 2013 at 15:48ArasMarch 21st, 2013 at 15:47Jeff GriffithsMarch 21st, 2013 at 15:51River Cities MediaMarch 22nd, 2013 at 01:36Brant WatsonMarch 25th, 2013 at 07:16Jeff GriffithsMarch 25th, 2013 at 10:46Brant WatsonMarch 25th, 2013 at 11:42Pablo Olmos de Aguilera C.April 8th, 2013 at 17:35Costa MichailidisMarch 25th, 2013 at 10:28Jeff GriffithsMarch 25th, 2013 at 10:31RugbyMarch 29th, 2013 at 07:21Jeff GriffithsMarch 29th, 2013 at 11:05RobertCZApril 11th, 2013 at 00:37