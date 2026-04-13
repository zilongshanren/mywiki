---
title: Firefox 70 — a bountiful release for all – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2019/10/firefox-70-a-bountiful-release-for-all/
author: Chris Mills
published: '2019-10-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 70 is released today, and includes great new features such as secure password generation with Lockwise and the new Firefox Privacy Protection Report; you can read the full details in the [Firefox 70 Release Notes](https://www.mozilla.org/en-US/firefox/70.0/releasenotes/).

Amazing [user features and protections](https://blog.mozilla.org/blog/2019/10/22/latest-firefox-brings-privacy-protections-front-and-center-letting-you-track-the-trackers/) aside, we’ve also got plenty of cool additions for developers in this release. These include DOM mutation breakpoints and inactive CSS rule indicators in the DevTools, several new CSS text properties, two-value `display`

syntax, and JS numeric separators. In this article, we’ll take a closer look at some of the highlights!

For all the details, check out the following:

Note that the new [Mozilla Developer YouTube channel](http://youtube.com/mozilladeveloper) will have videos covering many of the features mentioned below. Why not subscribe, so you can get them when they come out?

## HTML forms and secure passwords

To enable the generation of secure passwords (as mentioned above) we’ve updated HTML `<input>`

elements; any `<input>`

element of type password will have an option to generate a secure password available in the context menu, which can then be stored in Lockwise.

For example, take the following:

`<input type=”password”>`


In the Firefox UI, you’ll then be able to generate a secure password like so:![Context menu showing password generation option](../../assets/690223fe9ec50fcb.png)


In addition, any `type="password"`

field with `autocomplete=”new-password”`

set on it will have an autocomplete UI to generate a new password in-context.

Note: It is advisable to use `autocomplete=”new-password”`

on password change and registration forms as a strong signal to password managers that a field expects a new password, not an existing one.

## CSS

Let’s turn our attention to the new CSS features in Firefox 70.

### New options for styling underlines!

Firefox 70 introduces three new properties related to text decoration/underline:

: sets the thickness of lines added via text-decoration.`text-decoration-thickness`

: sets the distance between a text decoration and the text it is set on. Bear in mind that this only works on underlines.`text-underline-offset`

: sets whether underlines and overlines are drawn if they cross descenders and ascenders. The default value, auto, causes them to only be drawn where they do not cross over a glyph. To allow underlines to cross glyphs, set the value to none.`text-decoration-skip-ink`


So, for example, the following code:

```
h1 {
text-decoration: underline red;
text-decoration-thickness: 3px;
text-underline-offset: 6px;
}
```


will give you this kind of effect:

![a heading with a thick, red, offset underline that isn't drawn over the heading's descenders](../../assets/690d40a6f69c43f8.png)


### Two-keyword display values

For years, the humble [ display](https://developer.mozilla.org/en-US/docs/Web/CSS/display) property has taken a single value, whether we are talking about simple display choices like

`block`

, `inline`

, or `none`

, or newer display modes like `flex`

or `grid`

.However, as [Rachel explains](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model#Aside_Inner_and_outer_display_types), the boxes on your page have an outer display type, which determines how the box is laid out in relation to other boxes on the page, and an inner display type, which determines how the box’s children will behave. Browsers have done this for a while, but it has only been specified recently. The new set of two-keyword values allow you to explicitly specify the outer and inner display values.

In supporting browsers (just Firefox at the time of writing), the single keyword values we know and love will map to new two-keyword values, for example:

`display: flex;`

is equivalent to`display: block flex;`

`display: inline-flex;`

is equivalent to`display: inline flex;`


Rachel will explain this in more detail in an upcoming blog post. For now, watch this space!

## JavaScript

Now let’s move on to the JavaScript.

### Numeric separators

[Numeric separators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#Numeric_separators) are now supported in JavaScript — underscores can now be used as separators in large numbers, so that they are more readable. For example:

```
let myNumber = 1_000_000_000_000;
console.log(myNumber); // Logs 1000000000000
let myHex = 0xA0_B0_C0
console.log(myHex); // Logs 10531008
```


Numeric separators are usable with any kind of numeric literal, including [BigInts](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt).

### Intl improvements

We’ve improved JavaScript i18n (internationalization), starting with the implementation of the [ Intl.RelativeTimeFormat.formatToParts()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RelativeTimeFormat/formatToParts) method. This is a special version of

[that returns an array of objects, each one representing a part of the value, rather than returning a string of the localized time value.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RelativeTimeFormat/format)

`Intl.RelativeTimeFormat.format()`

```
const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });
rtf.format(-2, "day"); // Returns "2 days ago"
rtf.formatToParts(-2, "day");
/*
Returns
[
{ type: "integer", value: "2", unit: "day" },
{ type: "literal", value: " days ago" }
]
*/
```


This is useful because it allows you to easily isolate the numeric value out of the string, for example.

In addition, [ Intl.NumberFormat.format()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NumberFormat/format) and

[now accept](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NumberFormat/formatToParts)

`Intl.NumberFormat.formatToParts()`

[BigInt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt)values.

### Performance improvements

JavaScript has got generally faster thanks to our new baseline interpreter! You can learn more by reading [The Baseline Interpreter: a faster JS interpreter in Firefox 70](https://hacks.mozilla.org/2019/08/the-baseline-interpreter-a-faster-js-interpreter-in-firefox-70/).


There is a whole host of awesome new things going on with Firefox 70 developer tools. Let’s find out what they are!

### Inactive CSS rules indicator in rules panel

Inactive CSS properties in the [Rules view](https://wiki.developer.mozilla.org/en-US/docs/Tools/Page_Inspector/UI_Tour#Rules_view) of the [Page Inspector](https://wiki.developer.mozilla.org/en-US/docs/Tools/Page_Inspector) are now colored gray and have an information icon displayed next to them. The properties are technically valid, but won’t have any effect on the element. When you hover over the info icon, you’ll see a useful message about why the CSS is not being applied, including a hint about how to fix the problem and a “Learn more” link for more information.

For example, in this case our [ grid-auto-columns](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-auto-columns) property is inactive because we are trying to apply it to an element that is not a grid container:

And in this case, our [ flex](https://developer.mozilla.org/en-US/docs/Web/CSS/flex) property is inactive because we are trying to apply it to an element that is not a flex item. (Its parent is not a flex container.):

To fix this second issue, we can go into the inspector, find the element’s parent (a `<div>`

in this case), and apply `display: flex;`

to it:

Our fix is shown in the [Changes panel](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#Track_changes), and from there can be copied and put into our code base. Sorted!

### Pause on DOM Mutation in Debugger

In complex dynamic web apps it is sometimes hard to tell which script changed the page and caused the issue when you run into a problem. DOM Mutation Breakpoints (aka DOM Change Breakpoints) let you pause scripts that add, remove, or change specific elements.

Try inspecting any element on your page. When you /ctrl + click it in the HTML inspector, you’ll see a new context menu item “Break on…”, with the following sub-items:

- Subtree modification
- Attribute modification
- Node removal

Once a DOM mutation breakpoint is set, you’ll see it listed under “DOM Mutation Breakpoints” in the right-hand pane of the Debugger; this is also where you’ll see breaks reported.

For more details, see [Break on DOM mutation](https://wiki.developer.mozilla.org/en-US/docs/Tools/Debugger/Break_on_DOM_mutation). If you find them useful for your work, you might find [Event Listener Breakpoints](https://developer.mozilla.org/en-US/docs/Tools/Debugger/Set_event_listener_breakpoints) and [XHR Breakpoints](https://developer.mozilla.org/en-US/docs/Tools/Debugger/Set_an_XHR_breakpoint) useful too!

### Color contrast information in the color picker!

In the [CSS Rules view](https://wiki.developer.mozilla.org/en-US/docs/Tools/Page_Inspector/UI_Tour#Rules_view), you can click foreground colors with the [color picker](https://wiki.developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Inspect_and_select_colors) to determine if their contrast with the background color meets accessibility guidelines.

### Accessibility inspector: keyboard checks

The [Accessibility inspector](https://wiki.developer.mozilla.org/en-US/docs/Tools/Accessibility_inspector)‘s [Check for issues](https://wiki.developer.mozilla.org/en-US/docs/Tools/Accessibility_inspector#Check_for_accessibility_issues) dropdown now includes keyboard accessibility checks:

Selecting this option causes Firefox to go through each node in the accessibility tree and highlight all that have a keyboard accessibility issue:

Hovering over or clicking each one will reveal information about what the issue is, along with a “Learn more” link for more details on how to fix it.

Try it now, on a web page near you!

### Web socket inspector

In Firefox DevEdition, the [Network monitor](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor) now has a new “Messages” panel, which appears when you are monitoring a web socket connection (i.e. a 101 response). This can be used to inspect web socket frames sent and received through the connection.

Read [Firefox’s New WebSocket Inspector](https://hacks.mozilla.org/2019/10/firefoxs-new-websocket-inspector/) to find out more. Note that this functionality was originally supposed to be in Firefox 70 general release, but we had a few more bugs to iron out, so expect it in Firefox 71! For now, you can use it in [DevEdition](https://www.mozilla.org/en-US/firefox/developer/) — [please share your constructive feedback](https://discourse.mozilla.org/c/devtools)!

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.