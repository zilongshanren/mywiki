---
title: Debugger, Responsive Design View and more in Firefox Aurora 15 – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2012/07/debugger-responsive-design-view-and-more-in-firefox-aurora-15/
author: Kdangoor
published: '2012-07-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 15 is now in the [Aurora channel](http://mozilla.org/aurora) and has some big new features and improvements to the built-in tools for web developers.

## JavaScript Debugging

Firefox now ships with a Debugger (available via the Web Developer menu, or with the ctrl-shift-S/cmd-opt-S keyboard shortcut). Use this tool to quickly hunt down problems in your JavaScript code.

### Quickly Get to the Source

When you open the Debugger, all of the page’s scripts are listed in a menu. Using the search box, you can quickly jump to a file by typing part of its filename. Even better, we’ve taken some inspiration from [Sublime Text](http://www.sublimetext.com/): add “:<line number>” or “#<search string>” to immediately jump to a part of the file. For example, the screenshot above is from the [Backbone.js version of the TodoMVC demo](http://addyosmani.github.com/todomvc/architecture-examples/backbone/index.html). Typing “dovi” will jump to the “todoView.js” file. “dovi:20” will jump to line 20. “dovi#togglecom” will search for “togglecom” in the file. Press the enter key to move on to the next match, and you’ll be in roughly the same spot shown in the screenshot.

Of course, there are two other easy ways to get to the source you care about. One is to add a “debugger” keyword to your JavaScript. That’s a signal to start debugging at that line of the file. Another is to use the “Pause on exceptions” feature. If your code is encountering an unhandled exception, you just need to check that box in the toolbar and the Debugger will pause when it hits the exception.

Once you are looking at the source you care about, you can set a breakpoint by clicking to the left of the line number in the view of the JavaScript source.

### When the Debugger has Paused Your Script

Once your script has been paused by the Debugger, the stack frames are listed in the pane on the left and the in-scope variables are displayed in the pane on the right. The toolbar features the standard set of debugger controls: resume, step over, step in and step out. Use these to control how execution of your JavaScript proceeds so that you can watch how your program works.

As you step through your program, you’ll see variables displayed in the variables pane flash as their values change. You can even change the value of a variable by clicking on the value. Whatever you enter for the value of the variable is evaluated as JavaScript, so you can put `[1,2,3,4]`

in as the value, and the variable will be set to an array. The debugger also tells you whether the variable has a [property descriptor](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Object/defineProperty) controlling its behavior. You can see this information in the tooltip in the screenshot above.

### Under the Hood

This new Debugger is not just a new user interface over the functionality that Firefox’s JavaScript engine (SpiderMonkey) has been providing to tools like Firebug for years. The entire [debugging interface in SpiderMonkey](https://wiki.mozilla.org/Debugger) has been completely redesigned. There are two big things that web developers get because of the new debugger backend:

**It’s fast!**JavaScript applications running with the Debugger open will run nearly as fast as they do without the Debugger.**It’s remotable!**You can connect the debugger user interface to a debugger backend running somewhere else.

The second point above is exciting, because it means that you’ll be able to debug JavaScript that is running in [Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox&hl=en) or [Firefox OS](http://www.mozilla.org/en-US/b2g/), all from the comfort of Firefox on your desktop or laptop computer.

In a future article, we’ll show you how to do that.

## Responsive Design View

These days, powerful web devices come in many shapes and sizes and people have turned to [responsive web design](http://en.wikipedia.org/wiki/Responsive_Web_Design) as one way to accommodate these many different screens. The new Responsive Design View in Firefox makes it easy to resize just the page you’re viewing.

With the Responsive Design View, you can work on your designs without constantly pulling out your mobile phone to see how it looks. *And, *you can try out your designs without shrinking your browser’s tools, toolbars and other tabs.

Chris Heilmann put together [a video showing the Responsive Design View](http://www.youtube.com/watch?v=t07cLJhJkjQ) (and the Layout view, discussed below) in action.

## Layout View

Ever since [we first introduced the Style Inspector](http://hacks.mozilla.org/2011/11/developer-tools-in-firefox-aurora-10/) it has been possible to use the built-in tools to see how the margins, padding and border are set for a node. When working on a layout, however, having those values all together in one view is a big help. Now, that view is available as part of the Style Inspector.

By default, the Layout view is collapsed to a single line showing you the size of the element. Click the triangle to see the whole view which shows margins on the outside, border width, and then padding on the inside of the box.

## Other Improvements

We’ve had a lot of feedback on the Page Inspector since it was introduced a few months back. Many people like the attractive way it highlights the element you’re working on. On the other hand, there are times when you need the tool to move aside so that you can see just your page as it is presented to your users. Now, it’s easy to turn off the fancy highlighting behavior using the new options menu on the toolbar:

Finally, the [Web Console](https://developer.mozilla.org/en/Using_the_Web_Console) has gotten a major boost in performance. Whether you have the Web Console open or not, every console.log() call is now much, much faster. Give it a try and see!

## Where to Learn More

We have lots more in development and still more planned for the future. Here on Hacks, we’ll let you know about releases, but you can get in touch directly with the developers if you’re interested in sharing your opinion or hacking on the code. Check out our [Get Involved](https://wiki.mozilla.org/DevTools/GetInvolved) page for some of the contact points that are available.

## 23 comments

13xforeverJuly 6th, 2012 at 06:17Kevin DangoorJuly 6th, 2012 at 06:38MartinJuly 6th, 2012 at 13:35Hossein zolfiJuly 6th, 2012 at 14:23Jason LotitoJuly 7th, 2012 at 07:01WebUserJuly 7th, 2012 at 08:30UsefJuly 8th, 2012 at 05:38KrisJuly 10th, 2012 at 02:20KalleDecember 2nd, 2012 at 09:06Kevin DangoorDecember 3rd, 2012 at 06:14KalleDecember 3rd, 2012 at 10:40Jeff SchwartzJuly 10th, 2012 at 06:23GregorJuly 11th, 2012 at 08:40Kevin DangoorJuly 12th, 2012 at 00:35Ed SAugust 28th, 2012 at 11:18Hossein zolfiJuly 11th, 2012 at 13:36Kevin DangoorJuly 12th, 2012 at 00:32KeithAugust 28th, 2012 at 13:47BastianAugust 11th, 2012 at 12:53MarcOctober 9th, 2012 at 10:09Kevin DangoorOctober 9th, 2012 at 11:09markOctober 13th, 2012 at 07:03Kevin DangoorOctober 14th, 2012 at 09:11