---
title: Split console, pretty-print minified JS and more – Firefox Developer Tools
  Episode 28 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/12/split-console-pretty-print-minified-js-and-more-firefox-developer-tools-episode-28/
author: Jeff Griffiths
published: '2013-12-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Just in time for the holidays, the [Firefox Developer Tools](https://developer.mozilla.org/en/docs/Tools) teams has some excellent new surprises for you to enjoy as you hack on holiday projects! It’s a pretty long list, so let’s get started.

### App Manager

The [App Manager](https://developer.mozilla.org/en-US/Firefox_OS/Using_the_App_Manager) continues to be a priority for the Devtools team and with Firefox 28, in addition to many minor fixes and improvements the team has added two new major features to assist in mobile development. These two features consist of an additional manifest editor and an embedded toolbox.

The Manifest Editor allows a developer to edit their app manifest directly. Using this editor you can add, edit, or delete fields in your app’s manifest.webapp and save them back to disk. This feature provides the developer an integrated experience, as the user never has to leave the tools while debugging and improving an application.

Also new to the App Manager is the embedded toolbox. Now when you debug your app (either using the Simulator or on device) the toolbox will be opened in the App Manager in a separate vertical ‘tab’ that is easily distinguished by the app’s icon:

## Web Console

The biggest change in the Web Console is a feature we call ‘split console’; the web console can now be summoned from any other tool. Using split console mode is easy – if you’re working with any other tool and need access to the console, simply hit the Escape key or click on the button to toggle the split console, as you can see in this short screencast:

This isn’t the only improvement to the console though. In addition to split console we’ve also made the following changes:

- CSS warnings are off by default – CSS warnings can often add hundreds of messages to the console as a page loads.
- The console will now offer autocomplete suggestions for the current scope the debugger is in.
- Message timestamps can be toggled on/off (the default is off)
`console.exception()`

and`console.assert()`

have been added to the console api.- We added a dark theme for the console

## Debugger

In the debugger we’ve added two key features that developers have been asking for. First off we’ve added the ability to pretty-print minified JS files:

![](../../assets/8c1ab520b2d2ffba.png)


This feature is particularly handy if you minify your JavaScript or need to step through a minified library served from a remote site – just click on the minification button (picture above) to get a much more nicely formatted version of the file.

In addition to this we’ve added a feature to the debugger that allows you to inspect the value of a variable while debugging. For any variable, simply hover over it or click on it to bring up a pop-up that displays the current value:

![](../../assets/c5ed06ac4b9eb735.png)


The pop-up allows you to inspect not only simple types like the boolean picture above, but also objects and DOM nodes:

![](../../assets/05e1ed9aa4559049.png)


## Inspector

Following along from the addition of various tooltips to the Inspector in Firefox 27, we’ve added some additional features in the inspector:

- A Color picker tooltip in the rule view
- We updated style the style of tooltips to better match the dark and light themes
- The display timeout for tooltips was tuned based on your feedback

Here’s a screenshot to give you an idea what the color-picker tooltip looks like:

![](../../assets/1f1f352835332943.png)


## Wrapping up

That’s a huge list, but there were a couple of additional changes I’d like to call out as well:

- The Network Monitor now has a clear button, which should be of particular use to developers creating apps that make heavy use of web APIs:
![](../../assets/e630c56f4a42aa65.png)

- As a bonus for Add-on or Platform hackers, we’ve expanded the functionality of the Browser Debugger and re-named it the Browser Toolbox. When you open the toolbox you’ll see a full range of tools including not only the debugger but also the Console, Inspector, Style Editor, Profiler, Network Monitor and Scratchpad:

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 16 comments

Barry van OudtshoornDecember 17th, 2013 at 17:18ilyasDecember 18th, 2013 at 00:28ilyasDecember 18th, 2013 at 10:20Nick FitzgeraldDecember 18th, 2013 at 15:07Abhinav jagtapDecember 18th, 2013 at 04:27BryanDecember 18th, 2013 at 07:43Robert Nyman [Editor]December 18th, 2013 at 07:46SteveDecember 18th, 2013 at 08:32Robert Nyman [Editor]December 19th, 2013 at 06:41Axel RauschmayerDecember 18th, 2013 at 11:35Nick FitzgeraldDecember 18th, 2013 at 15:47Louis-RémiDecember 19th, 2013 at 01:18Panos AstithasDecember 19th, 2013 at 04:15Ken SaundersDecember 19th, 2013 at 07:34Panos AstithasDecember 19th, 2013 at 07:43JeanJanuary 15th, 2014 at 02:29