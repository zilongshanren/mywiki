---
title: 'New Features of Firefox Developer Tools: Episode 25 – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2013/08/new-features-of-firefox-developer-tools-episode-25/
author: Nick Fitzgerald
published: '2013-08-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 25 was just uplifted to the [Aurora release channel](http://www.mozilla.org/en-US/firefox/channel/#aurora) which means we are back to report about new features in Firefox Developer Tools.

Here’s a summary of some of the most exciting new features, and to get the whole picture you can check the [complete list of resolved bugzilla tickets](https://bugzilla.mozilla.org/buglist.cgi?list_id=7492061&resolution=FIXED&classification=Client%20Software&chfieldto=2013-08-05&query_format=advanced&chfieldfrom=2013-06-25&bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&component=Developer%20Tools&component=Developer%20Tools%3A%203D%20View&component=Developer%20Tools%3A%20App%20Manager&component=Developer%20Tools%3A%20Console&component=Developer%20Tools%3A%20Debugger&component=Developer%20Tools%3A%20Framework&component=Developer%20Tools%3A%20Graphic%20Commandline%20and%20Toolbar&component=Developer%20Tools%3A%20Inspector&component=Developer%20Tools%3A%20Netmonitor&component=Developer%20Tools%3A%20Object%20Inspector&component=Developer%20Tools%3A%20Profiler&component=Developer%20Tools%3A%20Responsive%20Mode&component=Developer%20Tools%3A%20Scratchpad&component=Developer%20Tools%3A%20Source%20Editor&component=Developer%20Tools%3A%20Style%20Editor&product=Firefox).

## Black box libraries in the Debugger

In modern web development, we often rely on libraries like [JQuery](http://jquery.com/), [Ember](http://emberjs.com/), or [Angular](http://angularjs.org/), and 99% of the time we can safely assume that they “just work”. We don’t care about the internal implementation of these libraries: we treat them like a [black box](http://en.wikipedia.org/wiki/Black_box). However, a library’s abstraction leaks during debugging sessions when you are forced to step through its stack frames in order to reach your own code. To alleviate this problem, we introduced black boxing: a feature where you can tell the debugger to ignore the details of selected sources.

To black box a source, you can either mark them one at a time by disabling the little eyeball next to it in the sources list:

![eyeball](../../assets/f7f0e1e69fc10e0e.png)


Or you can black box many sources at once by bringing up the developer toolbar with Shift+F2 and using the `dbg blackbox`

command:

![dbg blackbox --glob *-min.js[source]](https://hacks.mozilla.org/wp-content/uploads/2013/08/command.png)


When a source is black boxed:

- Any breakpoints it may have are disabled.
- When
[“pause on exceptions”](https://developer.mozilla.org/en-US/docs/Tools/Debugger#Debugger_settings)is enabled, the debugger won’t pause when an exception is thrown in the black boxed source; instead it will wait until (and if) the stack unwinds to a frame in a source that isn’t black boxed. - The debugger will skip through black boxed sources when stepping.

To see this in action and learn more about the details, check out the [black boxing screencast on YouTube](http://www.youtube.com/watch?v=uaFBvItTJrE).

## Replay and edit requests in the Network Monitor

You can now debug a network request by modifying headers before resending it. Right-click on an existing request and select the “resend” context menu item:

![resend request](../../assets/05dba92148e737be.png)


Now you can tweak the HTTP method, URL, headers, and request body before sending the request off again:

![tweak](../../assets/fa62136a791bc995.png)


## CSS Autocompletion in the inspector

Writing CSS in the inspector is now much easier as we enabled autocompletion of CSS properties and values.

![autocomplete](../../assets/e2e3971fca993067.png)


What’s more, it even works on inline style attributes

![inline](../../assets/71f10554ca0174c5.gif)


Aside: this feature was implemented by contributors [Girish Sharma](http://grssam.com/) and Mina Almasry. If you want to take your tools into your own hands too, check out our wiki page on [how to get involved with developer tools](https://wiki.mozilla.org/DevTools/GetInvolved).

## Execute JS in the current paused frame

One request we’ve heard repeatedly is the ability to execute JS from the webconsole in the scope of the current paused frame in the debugger rather than the global scope. This is now possible. Using the webconsole to execute JS in the current frame can make it much easier to debug your apps.

**Edit:** The webconsole has actually been executing in the current frame since Firefox 23, in Firefox 25 the scratchpad will execute in the current frame as well.

## Import and export profiled data in the Profiler

Hacking on a shared project and think you found a performance regression in some bit of code owned by one of your friends? Don’t just file a github issue with steps to reproduce the slowness, export and attach a profile of the code that shows exactly how much slowness there is, and where it occurs. Your friend will thank you when he or she is trying to reproduce and debug the regression. Click the “import” button next to the start profiling button to load a profile from disk, and hit “save” on an existing profile to export it.

![profileimport](../../assets/eb8b786bb2e2d169.png)


## When can I use these features?

All of these features and more are available in the [Aurora release channel](http://www.mozilla.org/en-US/firefox/channel/#aurora). In another 12 weeks, these features will roll over into Firefox stable.

Have some feedback about devtools? Ping [@FirefoxDevTools](http://twitter.com/FirefoxDevTools) on Twitter, or swing by [#devtools on irc.mozilla.org](irc://irc.mozilla.org/devtools).

## About
[
Nick Fitzgerald ](http://fitzgeraldnick.com)

I like computing, bicycles, hiphop, books, and pen plotters. My pronouns are he/him.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 37 comments

phi2xAugust 14th, 2013 at 01:46Nick FitzgeraldAugust 14th, 2013 at 03:01Niloy MondalAugust 14th, 2013 at 03:04Bradley MeckAugust 14th, 2013 at 05:24Nick FitzgeraldAugust 15th, 2013 at 10:39Markus KollerAugust 14th, 2013 at 05:50Markus KollerAugust 14th, 2013 at 05:51LinAugust 14th, 2013 at 09:50Kevin NewmanAugust 14th, 2013 at 10:46Ken SaundersAugust 15th, 2013 at 04:43Nick FitzgeraldAugust 15th, 2013 at 10:40Blaise KalAugust 14th, 2013 at 08:28Nick FitzgeraldAugust 15th, 2013 at 10:42Blaise KalAugust 18th, 2013 at 09:53Ken SaundersAugust 15th, 2013 at 05:12Jingyu WangAugust 15th, 2013 at 10:30Nick FitzgeraldAugust 15th, 2013 at 11:24PostmodernAugust 15th, 2013 at 13:54Nick FitzgeraldAugust 15th, 2013 at 13:58Chris HeilmannAugust 15th, 2013 at 16:10Jeremy WaltonAugust 15th, 2013 at 16:05BrandonAugust 15th, 2013 at 19:27pdAugust 16th, 2013 at 20:02Niloy MondalAugust 19th, 2013 at 00:42pdAugust 19th, 2013 at 03:16Niloy MondalAugust 20th, 2013 at 05:03MauroSeptember 11th, 2013 at 00:09MauroSeptember 10th, 2013 at 23:58Misha ReyzlinAugust 19th, 2013 at 03:25Nick FitzgeraldAugust 19th, 2013 at 10:38CynthiaAugust 20th, 2013 at 08:15MarkAugust 23rd, 2013 at 18:39Gene VayngribAugust 23rd, 2013 at 22:56Gene VayngribAugust 23rd, 2013 at 23:00MarkAugust 24th, 2013 at 15:58leandrwAugust 27th, 2013 at 09:01紫云飞September 4th, 2013 at 17:50