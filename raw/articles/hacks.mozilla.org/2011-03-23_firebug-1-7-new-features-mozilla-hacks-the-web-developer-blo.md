---
title: Firebug 1.7 New Features – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/03/firebug-1-7-new-features/
author: Jan Honza Odvarko
published: '2011-03-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Firebug 1.7](http://blog.getfirebug.com/) with full support for [Firefox 4](http://www.mozilla.com/en-US/firefox/fx/) is out of the door and I can’t miss this opportunity to describe some of the features introduced in this release.

![Firebug](../../assets/0ce0d0753630c881.png)


For those who don’t follow Firebug [blog](http://blog.getfirebug.com/) and/or are not familiar with Firebug too much/not at all, let’s start with some links leading to sources where you can start to dig more about Firebug world:

**Firebug**:[getfirebug.com](http://getfirebug.com/)**Blog**:[blog.getfirebug.com](http://blog.getfirebug.com/)**Wiki**:[getfirebug.com/wiki/index.php/Main_Page](http://getfirebug.com/wiki/index.php/Main_Page)**Forum**:[groups.google.com/group/firebug](http://groups.google.com/group/firebug)


### DOM Storage

DOM Storage is becoming an important part of many web applications and so, we made sure the DOM panel can be easily use to explore content of any [DOM Storage](https://developer.mozilla.org/en/DOM/Storage) object (global, session, local).

You can also use the Console panel to log any of these objects. For instance, executing `window.sessionStorage`

on the command line produces following output.

Of course, you can also log DOM storage object using standard `console.log`

API (from within the page) and you’ll get just the same result.

### Large Command Line History

As you might know there are two modes for Firebug [Command Line](http://getfirebug.com/wiki/index.php/Command_Line). Single line mode is called *Small Command Line* and a multiline mode called *Large Command Line*. The news is that if you switch into the Large Command Line mode – you still have a history of previously executed commands available.

It’s disabled if the history is empty, otherwise you can click and see a popup with entries. Another news is depicted on the next screenshot. You can see the same popup even in the *Small Command Line* mode. Just click the button on the left side.

### Date Object Logging

This is a small and pretty improvement of Firebug Console logging. If you log an instance of *Date()* object…

…you can see it’s actual value. I believe that all these small features keep Firebug the leader among in-browser dev tools.

### Sort Computed Styles

List of Computed styles (available in Computed side-panel in the HTML panel) can be sorted alphabetically now.

Note that the default is sorting by category.

### Break Notification messages

Break notification message UI is refactored and so, the notification message itself takes a lot less UI.

This helps the user to actually see the source code, *which is no doubt the important thing* when breaking into the debugger. As you can see on the screenshot (a little blurred but readable), the notification can be disabled. The UX should be intuitive and you should be able to quickly see where to enable again.

### Better Representation of Attributes

The way how element attribute list is presented in the DOM panel has been improved (this has been my personal wish for long time). See the following screenshot.

All what you usually want to know about a list of element attributes are names and values. And that’s exactly what this change is about (you don’t want to know how hard it was the get this information before). Of course if you are interested in all the DOM properties of an individual attribute (it’s also a DOM node) you can just click on it and inspect further.

### Firebug Start Button Redesign

One of the changes in Firefox 4 is no status bar. It’s actually replaced by an addon-bar, but… the trend is – not to have anything at the bottom of a browser window. Since Firebug’s entry point is there (the status bar icon) we were forced to create an alternative.

This button is appended into Firefox toolbar automatically just after installation. It has exactly the same functionality as the good old status bar icon. If you feel it’s a bit far from the Firebug UI, which is usually at the bottom, you can open the Addon-Bar and use the start button from there.

See [more info](http://www.softwareishard.com/blog/firebug/firebug-start-button-in-firefox-4/) about the start button.

### Quickly Scroll to a Script Line

Our feeling was that most of the users don’t know about a feature that allows to jump to a specific line within the Script panel and so, we made it a bit more visible.

All you need to do to scroll to specific line is writing `#`

+ *line number* (you don’t need to press enter).

The Script panel content will automatically scroll as you typing the line number and highlight the line for you.

### New Extension API

Firebug architecture has been well improved and there are two new extension points that are worth mentioning.

- New API for
[reusing Firebug Inspector](http://www.softwareishard.com/blog/firebug-tutorial/extending-firebug-inspector-part-x/)in other extensions - New API for
[reusing Firebug Infotips](http://www.softwareishard.com/blog/firebug-tutorial/extending-firebug-infotip-part-xi/)in other extensions.

Honza

## 16 comments

BuzuMarch 23rd, 2011 at 15:15MetasansanaMarch 23rd, 2011 at 15:23Ken SaundersMarch 23rd, 2011 at 17:08Steven RousseyMarch 23rd, 2011 at 22:01MatsMarch 23rd, 2011 at 23:10HonzaMarch 23rd, 2011 at 23:32Khaled Bin A QadirMarch 24th, 2011 at 00:18Gaurav MishraMarch 24th, 2011 at 01:50Jethro LarsonMarch 24th, 2011 at 18:21Jen SimmonsMarch 25th, 2011 at 05:31HonzaMarch 25th, 2011 at 06:07Larry BattleMarch 26th, 2011 at 03:52HonzaMarch 26th, 2011 at 03:59Emre YILMAZApril 3rd, 2011 at 14:22Web designer BangladeshJuly 14th, 2012 at 11:22Web designer BangladeshJuly 14th, 2012 at 11:26