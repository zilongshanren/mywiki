---
title: New in Firefox DevTools 65 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/01/new-in-firefox-devtools-65/
author: Martin Balfanz
published: '2019-01-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We just released [Firefox 65](https://hacks.mozilla.org/2019/01/firefox-65-webp-flexbox-inspector-new-tooling/) with a number of new developer features that make it even easier for you to create, inspect and debug the web.

Among all the features and bug fixes that made it to DevTools in this new release, we want to highlight two in particular:

- Our brand new Flexbox Inspector
- Smarter JavaScript inspection and debugging

We hope you’ll love using these tools just as much as we and our community loved creating them.

## Understand CSS layout like never before

The Firefox DevTools team is on a mission to help you master CSS layout. We want you to go from “trying things until they work” to really understanding how your browser lays out a page.

### Introducing the Flexbox Inspector

Flexbox is a powerful way to organize and distribute elements on a page, in a flexible way.

To achieve this, the layout engine of the browser does a lot of things under the hood. When everything works like a charm, you don’t have to worry about this. But when problems appear in your layout it may feel frustrating, and you may really need to understand why elements behave a certain way.

That’s exactly what the [Flexbox Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_Flexbox_layouts) is focused on.

### Highlighting containers, lines, and items

First and foremost, the Flexbox Inspector highlights the elements that make up your flexbox layout: the container, lines and items.

Being able to see where these start and end — and how far apart they are — will go a long way to helping you understand what’s going on.

Once toggled, the highlighter shows three main parts:

- A dotted outline that highlights the flex container itself
- Solid lines that show where the flex items are
- A background pattern that represents the free space between items

One way to toggle the highlighter for a flexbox container is by clicking its “flex” badge in the inspector. This is an easy way to find flex containers while you’re scanning elements in the DOM. Additionally, you can turn on the highlighter from the flex icon in the CSS rules panel, as well as from the toggle in the new Flexbox section of the layout sidebar.

### Understanding how flex items got their size

The beauty of Flexbox is that you can leave the browser in charge of making the right layout decisions for you. How much should an element stretch, or should an element wrap to a new line?

But when you give up control, how do you know what the browser is actually doing?

The Flexbox Inspector comes with functionality to show how the browser distributed the sizing for a given item.

![Flexbox container panel showing a list of flexbox items](../../assets/b541f72d7caff304.png)


The layout sidebar now contains a **Flex Container** section that lists all the flex items, in addition to providing information about the container itself.

Clicking any of these flex items opens the **Flex Item** section that displays exactly how the browser calculated the item size.

![Overview of Flexbox Item panel showing sizing informatin](../../assets/71dae52dd883c9ae.png)


The diagram at the top of the flexbox section shows a quick overview of the steps the browser took to give the item its size.

It shows your item’s base size (either its minimum content size or its `flex-basis`

size), the amount of flexible space that was added (`flex-grow`

) or removed (`flex-shrink`

) from it, and any minimum or maximum defined sizes that restricted the item from becoming any shorter or longer.

*If you are reading this on *

**Firefox 65**, you can take this for a spin right now!

Open the **Inspector** on this page, and select the `div.masthead.row`

element. Look for the **Flex Container** panel in the sidebar, and click on the 2 items to see how their sizes are computed by the browser.

### After the bug fix, keep track of changes

Let’s suppose you have fixed a flexbox bug thanks to the Flexbox Inspector. To do so, you’ve made a few edits to various CSS rules and elements. That’s when you’re usually faced with a problem we’ve all had: “What did I actually change to make it work?”.

In Firefox 65, we’ve also introduced a new [Changes panel](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#Track_changes) to do just that.

It keeps track of all the CSS changes you’ve made within the inspector, so you can keep working as you normally would. Once you’re happy, open the **Changes** tab and see everything you did.

### What’s next for layout tools?

We’re really excited for you to try these two new features and let us know [what you think](https://hacks.mozilla.org#contribute). But there’s more in store.

You’ve been [telling us exactly](https://hacks.mozilla.org/2018/11/new-experimental-web-design-tools-feedback-requested/) what your biggest CSS challenges are, and we’ve been listening. We’re currently prototyping layout tools for debugging unwanted scrollbars, z-indexes that don’t work, and more tools like the Flexbox Inspector but for other types of layouts. Also, we’re going to make it even easier for you to extract your changes from the Changes panel.

## Smarter JavaScript inspection & debugging

When developing JavaScript, the Console and Debugger are your windows into your code’s execution flow and state changes. Over the past releases we’ve focused on making debugging work better for modern toolchains. Firefox 65 continues this theme.

### Collapsing Framework Stack Traces

If you’re working with frameworks and build tools, then you’re used to seeing really long error stack traces in the Console. The new smarter stack traces identify 3rd party code (such as frameworks) and collapse it by default. This significantly reduces the information displayed in the **Console** and lets you focus on *your* code.

![Before and after version of stack traces in console.](../../assets/073acd4cc69c3c76.png)


The **Collapsing** feature works in the Console stack traces for errors and logs, and in the Debugger call stacks.

### Reverse search your Console history

If you are tired of smashing the arrow key to find that awesome one-liner you ran one hour ago in the console, then this is for you. Reverse search is a well known command-line feature that lets you quickly browse recent commands that match the entered string.

To use it in the Console, press *F9* on Windows/Linux or *Ctrl+R* on MacOS and start typing. You can then use *Ctrl+R* to move to the previous or *Ctrl+S* to the next result. Finally, hit return to confirm.

### Invoke getters to inspect the return value

JavaScript [getters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get) are very useful for dynamic properties and heavily used in frameworks like [vue.js](https://vuejs.org/v2/guide/computed.html) for computed properties. But when you log an object with a getter to the Console, the reference to the method is logged, not its return value. The method does not get invoked automatically, as that could change your application’s state. Since you often actually want to see the value, you can now manually invoke getters on logged objects.

Wherever objects can be inspected, in the Console or Debugger, you’ll see `>>`

icons next to getters. Clicking these will execute the method and print the return value.

### Pause on XHR/Fetch Breakpoints

Console logging is just one aspect of understanding application state. For complex issues, you need to pause state at precisely the right moment. Fetching data is usually one of those moments, and it is now made “pausable” with the new XHR/Fetch Breakpoint in the Debugger.

![XHR Breakpoints panel in the debugger](../../assets/43a99c5d532404d0.png)


Kudos to Firefox DevTools code contributor [Anshul Malik](https://github.com/AnshulMalik) for [“casually” submitting](https://github.com/firefox-devtools/debugger.html/pull/6934#issuecomment-419260053) the patch for this useful feature and for his ongoing contributions.

### What’s next for JavaScript debugging?

You might have noticed that we’ve been heads down over recent releases to make the JavaScript debugging experience rock solid – for breakpoints, stepping, source maps, performance, etc. Raising the quality bar and continuing to polish and refine remains the focus for the entire team.

There’s work in progress on much requested features like **Column Breakpoints**, **Logpoints**, **Event** and **DOM Breakpoints**. Building out the authoring experience in the Console, we are adding an multi-line editing mode (inspired by [Firebug](https://hacks.mozilla.org/2017/10/saying-goodbye-to-firebug/)) and a more powerful autocomplete. Keep an eye out for those features in the latest release of [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/).

## Thank you

Countless contributors helped DevTools staff by filing bugs, writing patches and verifying them. Special thanks go to:

[Zameer Haque](https://github.com/zamhaq):[Improved contrast](https://bugzilla.mozilla.org/show_bug.cgi?id=1495971)for resource status in the Console.[Heng Yeow](https://github.com/tanhengyeow):[Added](https://bugzilla.mozilla.org/show_bug.cgi?id=1496742)the[Referrer-Policy to](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy)the resource[Headers](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor/request_details#Network_request_details)list in the Network panel (and[fixed](https://bugzilla.mozilla.org/show_bug.cgi?id=1340100)[other](https://bugzilla.mozilla.org/show_bug.cgi?id=1501674)[bugs](https://bugzilla.mozilla.org/show_bug.cgi?id=1459539)).[Adam Holm](https://github.com/ash-tamraz):[Updated](https://bugzilla.mozilla.org/show_bug.cgi?id=1340100)the design for the[Edit & Resend](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor/request_list#Edit_and_Resend)dialog in the Network panel.[Ariel Burone](https://bugzilla.mozilla.org/user_profile?user_id=613727):[Swapped](https://bugzilla.mozilla.org/show_bug.cgi?id=862851)the Domain and File column in the Network panel.

Also, thanks to [Patrick Brosset](https://twitter.com/patrickbrosset), [Nicolas Chevobbe](https://twitter.com/nicolaschevobbe/) and the whole DevTools team & friends for helping put together this article.

## Contribute

As always, we would love to hear your feedback on how we can improve DevTools and the browser.

- File bug reports in
[Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=DevTools&component=General) - Chat with us in the
[Firefox DevTools Slack](https://devtools-html-slack.herokuapp.com/) - Share ideas and questions in Mozilla’s
[Developer Tools Discourse](https://discourse.mozilla.org/c/devtools) - Tweet us at
[@FirefoxDevTools](https://twitter.com/FirefoxDevTools)

Download [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) to get early access to upcoming tooling and platform.

## About
[
Martin Balfanz ](http://martinbalfanz.com)

Martin is a Product Manager at Mozilla, working on Firefox DevTools.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

## 11 comments

James BlazzikeFebruary 1st, 2019 at 00:39Harald KirschnerFebruary 4th, 2019 at 13:16Daisuke NogamiFebruary 4th, 2019 at 12:44Harald KirschnerFebruary 5th, 2019 at 22:03Yan HuiFebruary 5th, 2019 at 01:31DavidFebruary 6th, 2019 at 09:25Harald KirschnerFebruary 6th, 2019 at 10:37Claudinei PerboniFebruary 7th, 2019 at 09:40Thomas KehneFebruary 8th, 2019 at 04:32J RedheadFebruary 10th, 2019 at 13:56Harald KirschnerFebruary 11th, 2019 at 11:29