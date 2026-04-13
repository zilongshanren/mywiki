---
title: 'Reintroducing the Firefox Developer Tools, part 2: the Scratchpad and the
  Style Editor – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/11/reintroducing-the-firefox-developer-tools-part-2-the-scratchpad-and-the-style-editor/
author: Robert Nyman Posted
published: '2013-11-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is part two, out of five, focusing on the built-in

[Developer Tools in Firefox], their features and where we are now with them. The intention is to show you all the possibilities available, the progress and what we are aiming for.

In the first post in the series [we discussed the Web Console and the JavaScript Debugger](https://hacks.mozilla.org/2013/09/reintroducing-the-firefox-developer-tools-part-1-the-web-console-and-the-javascript-debugger/). While these two tools are powerful and provide capabilities to interrogate and alter your web applications, additional tools are available to further enhance the developer experience while building and debugging your apps. In this post we briefly cover the Scratchpad and the Style editor.

As with the first post, we present each tool with a quick screencast demonstrating some of their capabilities.

## The Style Editor

The Style Editor is primarily used to edit, debug or create new stylesheets within the context of the current app. Changes made in the style editor are automatically reflected in the loaded page. If you are not familiar with Cascading Style Sheets (CSS), please be sure to take a look at the [CSS MDN documentation](https://developer.mozilla.org/en-US/docs/Web/CSS).

The Style Editor allows saving the changes made while using the editor. In addition you can also import existing stylesheets and apply them to the current page or individually disable specific stylesheets. The Style Editor is also linked to the Inspector allowing developers quick access to the stylesheet for the inspected element. The following screencast presents an overview of the Style Editor’s features.

For more detailed [information on the Style Editor](https://developer.mozilla.org/en-US/docs/Tools/Style_Editor) take a look at the MDN documentation.

## Scratchpad

The Scratchpad has many uses and is essentially a live JavaScript editor and prototyping tool. Using the Scratchpad, a developer can access the current page’s objects, variables and script. In addition, complete functions can be written and tested in the editor within the scope of the live page. These changes can then be attached and saved with the current application.

External JavaScript files can also be loaded and tested. Several run options are available to allow a developer to just execute the code, execute the code and inspect the returned object, or execute the code and print out the results as a comment within the Scratchpad. The following screencast illustrates some of the features of the Scratchpad. Note that Scratchpad script runs in the same

context as a script loaded into the page. In the screencast, the example uses the jQuery library and some custom script to illustrate this feature.

For more [information on the Scratchpad](https://developer.mozilla.org/en-US/docs/Tools/Scratchpad), see the MDN Debugger documentation.

If you are not very familiar with JavaScript, make sure to check out the [MDN documentation for a comprehensive list of resources on learning the language](https://developer.mozilla.org/en-US/docs/Web/JavaScript) and mechanics.

## Learn More

These screencasts give a quick introduction to the main features of these tools. For the [full details on all of the Developer Tools](https://developer.mozilla.org/en-US/docs/Tools), check out the full MDN Tools documentation.

## Coming Up

In the next post, we will focus on some Mobile design features including the Responsive Design View and Remote debugging using the App Manager. Please provide your suggestions on what features you would like to see explained in more detail in this upcoming post, by commenting below.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 22 comments

AdamNovember 4th, 2013 at 12:16Nick FitzgeraldNovember 4th, 2013 at 13:53ShmerlNovember 4th, 2013 at 13:04Nick FitzgeraldNovember 4th, 2013 at 13:54LukeNovember 5th, 2013 at 21:55J. Ryan StinnettNovember 5th, 2013 at 03:32ericNovember 4th, 2013 at 13:33LukeNovember 5th, 2013 at 21:58MaurizioNovember 4th, 2013 at 14:54Robert Nyman [Editor]November 5th, 2013 at 04:57Mindaugas J.November 5th, 2013 at 05:00Robert Nyman [Editor]November 5th, 2013 at 05:02Mindaugas J.November 5th, 2013 at 05:05Robert Nyman [Editor]November 5th, 2013 at 06:40MaurizioNovember 4th, 2013 at 15:00DelapouiteNovember 5th, 2013 at 15:41LukeNovember 5th, 2013 at 21:59nemoNovember 4th, 2013 at 16:30Mike RatcliffeNovember 8th, 2013 at 07:20Mike RatcliffeNovember 8th, 2013 at 07:22stripTMNovember 4th, 2013 at 18:08Mindaugas J.November 5th, 2013 at 03:17