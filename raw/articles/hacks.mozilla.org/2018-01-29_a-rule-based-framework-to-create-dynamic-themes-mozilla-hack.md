---
title: A rule-based framework to create dynamic themes – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2018/01/a-rule-based-framework-to-create-dynamic-themes/
author: Tim Nguyen
published: '2018-01-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In December, I gave [an introduction](https://hacks.mozilla.org/2017/12/using-the-new-theming-api-in-firefox/) to the theming API in Firefox. While it allows you to do many things like [animated themes](https://github.com/hellosct1/theme-animation), [macOS-style overscroll](https://github.com/nt1m/theming-api-content-blurring) or [interactive theme editors](https://github.com/lmorchard/ThemesRFun), the API has some limitations. One issue with dynamic theming API compared to traditional CSS theming is that it requires familiarity with JavaScript and WebExtension APIs to make a basic dynamic theme.

To address this problem, I have experimented with a simple system that enables dynamic theming using simple theming “rules”. A “rule” consists of a JavaScript condition string paired with a theme name. Here it is: [https://github.com/nt1m/theming-rules](https://github.com/nt1m/theming-rules)

This boilerplate takes care of all the heavy-lifting needed by dynamic themes in order to set up WebExtension listeners, hooking with other APIs — to let you focus on the dynamic theming part.

To get started, clone the repository above locally. All the configuration is located in the `config.js`

file of the boilerplate. Once you’ve opened this file, you should see the code below:

```
// The default theme: used when no rule is matched
const DEFAULT_THEME = "bright";
// The theming rules: priority is given to the bottom-most rule
const RULES = [
["privatebrowsing", "shady"],
["(hour >= 21) || (hour < 9)", "shady"]
];
```


In this case, the “shady” theme is used at night from 9pm to 9am and on private tabs. In all the other cases, the “bright” default theme is used.

Let’s edit the `config.js`

file with a more complicated example:

```
// The default theme: used when no rule is matched
const DEFAULT_THEME = "bright";
// The theming rules: priority is given to the bottom-most rule
const RULES = [
["privatebrowsing", "shady"],
["(hour >= 21) || (hour < 9)", "shady"],
["privatebrowsing && ((hour >= 21) || (hour < 9))", "bright"]
];
```


Can you guess what this does?

Here is a clue: rules have the concept of “priority”, if more than 1 rule matches, the bottom-most rule is used.

In this case, the “bright” theme is used during daytime and on private windows during nighttime. The “shady” theme is used during nighttime, and on private windows during daytime. Phew!

There are several properties you can use, here is a list:

- inactive_window
- privatebrowsing
- container
- domain
- protocol
- year
- month
- date
- day
- hour
- minutes
- seconds

Later on in this article, I’ll show how you can define your own properties.

As for the “bright” and the “shady” themes used in previous examples, they’re defined in the standard WebExtension theme format, also in the `config.js`

file:

```
const THEMES = {
bright: {
colors: {
frame: "#dedede",
tab_background_text: "#000",
toolbar_text: "#000",
toolbar: "#f8f8f8",
}
},
shady: {
colors: {
frame: "#000",
tab_background_text: "#ddd",
toolbar_text: "#ccc",
toolbar: "#3a3a3a"
}
}
};
```


## Use case: Style the browser based on the protocol

Now that you’ve been introduced to the system, let’s build an useful example: let’s style the browser based on whether the current tab is an HTTP or HTTPS page.

First we’ll define the look of the HTTP and HTTPS themes, we’ll use red for HTTP sites and green for HTTPS sites:

```
insecure: {
colors: {
frame: "red",
tab_background_text: "black",
toolbar: "pink",
toolbar_text: "black"
}
},
secure: {
colors: {
frame: "green",
tab_background_text: "white",
toolbar: "lightgreen",
toolbar_text: "black"
}
}
```



Now let’s define the rules:

```
// The default theme: used when no rule is matched
const DEFAULT_THEME = "bright";
// The theming rules: priority is given to the bottom-most rule
const RULES = [
["protocol == 'http:'", "insecure"],
["protocol == 'https:'", "secure"]
];
```


…and that’s it! Notice how “bright” was kept as default theme. This is because other protocols like `file://`

exist, in which case the extension applies a neutral theme.

Here is what the example looks like:

## Adding more properties

You may have noticed the special `privatebrowsing`

, `hour`

and p`rotocol`

keywords. They’re built-in properties and are defined as such:

```
privatebrowsing: {
type: "boolean",
async get(tab) {
return tab.incognito;
}
},
protocol: {
type: "string",
async get(tab) {
return new URL(tab.url).protocol;
}
},
hour: {
type: "integer",
async get(tab) {
return (new Date(Date.now())).getHours();
}
}
```


Each property definition takes a [WebExtension Tab object](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs/Tab) (which you can choose to ignore), and returns a value out of it.

All of the built-in property definitions can be found in the [ properties.js file](https://github.com/nt1m/theming-rules/blob/master/properties.js).

What if you want to add your own? Adding a property is as simple as adding a property definition. Here is an example that uses the [cookies API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/cookies) to return the number of cookies for the current tab domain:

```
cookies: {
type: "integer",
async get(tab) {
let cookies = await browser.cookies.getAll({
domain: new URL(tab.url).hostname
});
return cookies.length;
}
}
```


It can potentially be used to style tabs differently depending on the number of cookies.

Property definitions are pretty flexible, some ideas could be having a property that returns the current weather via an XHR, or the number of trackers on a page. The only limit is your imagination :)

## Give it a try!

Whether you need a very simple way to create dynamic themes that doesn’t require deep knowledge in WebExtension APIs, or simply a way to quickly prototype contextual UI features, this is the right tool for you!

There are many possibilities using this system, it would be great to see what you can come up with.

Here is the repository: [https://github.com/nt1m/theming-rules](https://github.com/nt1m/theming-rules).

Feel free to share your experience in comments here, or via Github issues.

Edit (July 21st 2019): Updated code samples to remove [deprecated theme properties](https://bugzilla.mozilla.org/show_bug.cgi?id=1472740)

## About Tim Nguyen

I work on web browsers.

## 2 comments

djordgeJanuary 30th, 2018 at 06:01Alexandre SheroziaFebruary 1st, 2018 at 23:01