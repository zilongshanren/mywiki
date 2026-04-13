---
title: 'Trainspotting: Firefox in 2015 – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/12/trainspotting-firefox-in-2015/
author: Sergi Mansilla
published: '2015-12-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

__Trainspotting__ is a series of articles highlighting features in the lastest version of Firefox. A new version of Firefox is shipped every six weeks- we at Mozilla call this pattern "release trains".

The year is coming to a close, and even as the coals of 2015 fade to a soft orange, we've got Firefox releases to talk about! Here's a run-down of a few new tricks up the browser's sleeve, as well as a few of my favorite new features from this year.

*Firefox 42 and 43 were released since our last Trainspotting post- you can check out 42's release notes here and 43's here.*

## "Use in Console" in Firefox 43

Let's start with something new and handy- sometimes it's useful to use Console to inspect or tweak an element you found in the Inspector. The traditional way is to use `querySelector`

to find the element, or, in some browsers, the special `$0`

variable which refers to the element currently being inspected. (If you didn't know about `$0`

, consider it a nice end-of-year bonus!). Starting in Firefox 43, you can now use the "Use in Console" command in the context menu to put that element into a temporary variable. Unlike `$0`

, you can create multiple temporary variables in the Console and highlight other elements without losing your reference. An iterative improvement, but one that makes life easier.

## New Privacy and Security Control Center in Firefox 42

![control-center](../../assets/a5a7c063304d295a.jpg)

You've always been able to check whether your connection to a website is secure by clicking in the address bar. Firefox 42 includes a redesign of this panel to make it easier to review the security of a website, as well as incorporate privacy settings and what permissions you've granted. It's a nice improvement to an interface that used to take many more clicks.

## Easier Element Screenshots in Firefox 41

![Right click on a node in the markup view.](../../assets/1d3eb2895633fde6.gif)

This feature proved to be very popular! Firefox 41 added the ability to capture a part of the page from the Inspector with the “Screenshot Node” menu command.

## BroadcastChannel in Firefox 38

A personal favorite API of mine- the ability for all open pages on a domain to broadcast messages to one another. Great for keeping app state in sync or event notifications.

```
// one tab
var ch = new BroadcastChannel('test');
ch.postMessage('this is a test');
// another tab
ch.addEventListener('message', function (e) {
alert('I got a message!', e.data);
});
// yet another tab
ch.addEventListener('message', function (e) {
alert('Avast! a message!' e.data);
});
```


## Wrapping up 2015

It’s been a great year, and I’ve had a blast writing about notable new features in Firefox. If you want to learn more about how Firefox has grown and improved this year, read through the [Trainspotting post archive](https://hacks.mozilla.org/category/trainspotting/).

**See you in 2016!**