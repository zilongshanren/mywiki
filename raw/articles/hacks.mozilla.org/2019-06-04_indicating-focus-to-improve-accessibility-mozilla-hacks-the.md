---
title: Indicating focus to improve accessibility – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2019/06/indicating-focus-to-improve-accessibility/
author: Hidde de Vries
published: '2019-06-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It’s a common, but fairly easy-to-fix accessibility issue: lack of indicating focus. In this post I will explain what we mean by focus and show you how focus outlines make your site easier to use.

## What is focus?

*Focus indicators* make the difference between day and night for people who rely on them. Let’s first look at what they are, and which people find them useful.

Focus is something that happens between the *interactive* *elements* on a page. That’s the first thing you should know. (See the [focusable elements compatibility table](https://allyjs.io/data-tables/focusable.html) for a more detailed and nuanced definition.) [Interactive elements](https://html.spec.whatwg.org/multipage/dom.html#interactive-content-2) are elements like links, buttons and form fields: things that users can interact with.

![menu links; one is outlined, the outline moves between the links](../../assets/97f8ee30fbd0a263.gif)


On a page, at any given time, there is *one* element that has focus. If you’ve just loaded a page, it is probably the document, but once you start to click or tab, it will be one of the aforementioned interactive elements. The currently focused element can be found with `document.activeElement`

.

By default, browsers convey which element currently has focus by drawing an outline around that element. The defaults vary between browsers and platform. With CSS, you can override these defaults, which we’ll get to in a bit.

### Who benefits

Focus outlines help users figure out where they are on a page. They show which form field is currently filled in, or which button is about to be pressed. People who use a mouse, might use their cursor for this, but not everyone uses a mouse. For instance, there are many keyboard users: a person with a baby on one arm, people with chronic diseases that prevent the use of a mouse, and of course… developers and other power users. Beyond keyboards, there are other tools and input devices that rely on clearly indicated focus, like [switches](https://axesslab.com/switches/).

It is not just keyboard users that benefit, though. Focus indication also helps people who have limited attention spans or issues with short term memory, for example if they are filling out a lengthy form.

If the idea of indicating the current element in a website seems weird, consider TV interfaces. Most people use them with a remote control or game controller, and therefore rely on the interface to convey what’s currently selected.

### Never remove them

Not everyone likes how focus outlines look, some find them ugly. But then that’s the case with street lights, too. They are unlikely to win design awards, but if you have to walk home in the dark, you are glad they help you see where you are.

Removing focus styles, as some websites do, is as detrimental for keyboard users as removing the mouse cursor would be for mouse users.

Nobody would override the browser’s default cursor, effectively removing the cursor altogether:

```
body {
cursor: none; /* you wouldn't do this */
}
```


So we shouldn’t do this either, which removes the browser’s default outline:

```
:focus {
outline: none; /* so, please don't do this */
}
```


Or, as Laura Carvajal [put it at Fronteers 2018](https://vimeo.com/309897241):

*Laura Carvajal with slide: You wouldn’t steal their cursor*

Even if you provide an alternative with something like `box-shadow`

, best set `outline`

to `solid transparent`

, because `box-shadow`

does not play well with high contrast modes.

## Good focus indicators

One way to indicate focus is to rely on browser defaults. It works, but I would recommend designing your own focus outlines. This gives you maximum control over how easy they are to see, and lets you integrate them with brand colours or the style of your site. Usually, thicker outlines (from 2px onwards) are better, as they are simply easier to see.

The `:focus`

pseudo class takes CSS rules like any other selector, so you could style it however you like. In some cases a background color or underline could indicate that something is active.

### Examples

Below are focus outlines as seen on Schiphol.nl and the City of The Hague websites. They make it easy to distinguish in a list of links which one is currently active.

### Transitions

Focus outlines do not have to be boring. The `outline`

property can be [transitioned](https://developer.mozilla.org/en-US/docs/Web/CSS/transition) with CSS, so why not add a subtle animation? Make it pop!

### Contrast

In [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/?versions=2.1), focus indicators are bound to the same contrast rules as other parts of the content, as per [1.4.11: Non-text contrast](https://www.w3.org/WAI/WCAG21/quickref/?versions=2.1&showtechniques=324%2C331#non-text-contrast). This means a contrast of 3:1 between the outlines and their background is required.

On websites that have both light and dark parts, it is quite common to have a dark and a light focus style. For example, if your focus outline is blue for parts with a white background (for instance, the main content area), you could make it white for parts with a black background (for instance, the footer).

## Special cases

### Focusing non-interactive elements

As mentioned earlier, focus works on interactive elements. In special cases, it makes sense to focus a non-interactive element, like a `<div>`

, if that element is a piece of expanded content or a modal overlay that was just opened.

Any element can be added to focus order with the `tabindex`

attribute in HTML. Best use it with `0`

or `-1`

:

`tabindex="0"`

: element can be focused with keyboard and through JavaScript`tabindex="-1"`

: element can be focused through JavaScript, but cannot be tabbed to

A `tabindex`

with a number larger than 0 is best avoided, as this sets a preference of where the element goes in the tab order. If you set it for one element, you will have to set and maintain (!) a `tabindex`

value on all interactive elements on the page. See also: [It rarely pays to be positive](https://www.scottohara.me/blog/2019/05/25/tabindex.html) by Scott O’Hara.

### Only for keyboard users

If you are a developer and the design team is unwilling to apply bold focus styles, you could propose to show them to users who need them, for instance only to keyboard users.

There are two caveats to this notion of “users who need them”:

- Not all people who rely on focus styles use a keyboard. We mentioned
[switches](https://axesslab.com/switches/)earlier, but that’s only one use case. As a general rule, keep in mind that you can’t predict all the ways your visitors choose to browse the web. - Making focus styles keyboard-only takes away an affordance for mouse users too, as focus also indicates that something is interactive.

For these reasons, we should be careful making decisions about when and how to show focus styles. Luckily, there is a CSS property invented to help us out here: [focus-visible](https://drafts.csswg.org/selectors-4/#the-focus-visible-pseudo). According to the spec, it lets us:

provide clearly identifiable focus styles which are visible when a user is likely to need to understand where focus is, and not visible in other cases


In other words: it aims to let you indicate focus only for people that need it. This is [supported](https://caniuse.com/#search=focus-visible) in Firefox (with prefix), but not yet in Chromium (they [intend to implement](https://chromium-review.googlesource.com/c/chromium/src/+/897002)), so it would be best to use the [official focus-visible polyfill](https://github.com/WICG/focus-visible). It is preferable to avoid such heuristics and convey focus rings to everybody, but if you have to, focus-visible is ideal. Especially if the alternative is nothing at all.

## Focus styles as keyboard accessibility

A focused element that isn’t highlighted has a big impact on usability for keyboard users. You could make keyboard checks part of your development workflow to ensure that you don’t forget focus indicators. For instance, you could include “Can be used with a keyboard” in your definition of done. This is a [check](https://www.w3.org/WAI/test-evaluate/preliminary/#interaction) that most people in the team should be able to do before a new feature goes live. As we’ve seen above, focus styles don’t just benefit keyboard users, but keyboard operability is a good way to test them.

When testing, you might find that not all browsers and platforms let you tab through interactive elements by default. Here are some of the most common settings across platforms and browsers:

- macOS: under System Preferences > Keyboard > Shortcuts set ‘Full keyboard access’ to ‘All controls’
- Safari, macOS: in `Safari > Preferences`, under ‘Advanced’, check ‘Press Tab to highlight each item on a webpage’
- Chrome: in chrome://settings, under ‘Web content’, check ‘Pressing Tab on a webpage highlights links, as well as form fields’

## Summing up

Hopefully this post inspires you to try out your (client’s) site with just a keyboard. Maybe it is a pleasure to use already. If not, perhaps this post convinces you or your team to address the problem and design some on-brand focus indicators. Together we make the web more friendly to users of keyboards, sticks and switches. Together we make the web work for everyone.

Focus outlines are one of many ways to design for accessibility. For more tips on design with accessibility in mind, see [Accessibility Information for UI designers](https://developer.mozilla.org/en-US/docs/Mozilla/Accessibility/Accessibility_information_for_UI_designers) on MDN and [Tips for designing with accessibility](https://www.w3.org/WAI/tips/designing/) at the W3C.

## About
[
Hidde de Vries ](https://hiddedevries.nl/en)

Hidde ([@hdv](https://twitter.com/hdv)) is a front-end developer and accessibility expert, based in Rotterdam, The Netherlands. Currently, he works for the W3C in the WAI team (views are his own). Previously he was at Mozilla, the Dutch government and various other organisations and businesses. He is overly excited about all things CSS, accessibility and reusable components. Also [occassional speaker](https://talks.hiddedevries.nl).