---
title: In March, we see Firefox 87 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/03/in-march-we-see-firefox-87/
author: Chris Mills
published: '2021-03-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Nearing the end of March now, and we have a new version of Firefox ready to deliver some interesting new features to your door. This month, we’ve got some rather nice DevTools additions in the form of `prefers-color-scheme`

media query emulation and toggling `:target`

pseudo-classes, some very useful additions to editable DOM elements: the `beforeinput`

event and `getTargetRanges()`

method, and some nice security, privacy, and macOS screenreader support updates.

This blog post provides merely a set of highlights; for all the details, check out the following:

## Developer tools

In developer tools this time around, we’ve first of all updated the [Page Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#view_media_rules_for_prefers-color-scheme) to allow simulation of [ prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) media queries, without having to change the operating system to trigger light or dark mode.

Open the DevTools, and you’ll see a new set of buttons in the top right corner:

![Two buttons marked with sun and moon icons](../../assets/83a5e1d24bdce44a.png)


When pressed, these enable the light and dark preference, respectively. Selecting either button deselects the other. If neither button is selected then the simulator does not set a preference, and the browser renders using the default feature value set by the operating system.

And another nice addition to mention is that the Page Inspector’s CSS pane can now be used to toggle the [ :target](https://developer.mozilla.org/docs/Web/CSS/:target) pseudo-class for the currently selected element, in addition to a number of others that were already available (

[,](https://developer.mozilla.org/docs/Web/CSS/:hover)

`:hover`

[, etc.)](https://developer.mozilla.org/docs/Web/CSS/:active)

`:active`

![Firefox devtools CSS rules pane, showing a body selector with a number of following declarations, and a bar up the top with several pseudo classes written inside it](../../assets/3ae7be8c1e10bfc0.png)


Find more out about this at [Viewing common pseudo-classes](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#viewing_common_pseudo-classes).

## Better control over user input: beforeinput and getTargetRanges()

The [ beforeinput](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/beforeinput_event) event and

[method are now enabled by default. They allow web apps to override text edit behavior before the browser modifies the DOM tree, providing more control over text input to improve performance.](https://developer.mozilla.org/en-US/docs/Web/API/InputEvent/getTargetRanges)

`getTargetRanges()`

The global `beforeinput`

event is sent to an [ <input>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input) element — or any element whose

[attribute is set to](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes#attr-contenteditable)

`contenteditable`

`true`

— immediately before the element’s value changes. The `getTargetRanges()`

method of the [interface returns an array of static ranges that will be affected by a change to the DOM if the](https://developer.mozilla.org/en-US/docs/Web/API/InputEvent)

`InputEvent`

[event is not canceled.](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event)

`input`

As an example, say we have a simple comment system where users are able to edit their comments live using a `contenteditable`

container, but we don’t want them to edit the commenter’s name or other valuable meta data? Some sample markup might look like so:

```
<p contenteditable>
<span>Mr Bungle:</span>
This is my comment; isn't it good!
<em>-- 09/16/21, 09.24</em>
</p>
```


Using `beforeinput`

and `getTargetRanges()`

, this is now really simple:

```
const editable = document.querySelector('[contenteditable]');
editable.addEventListener('beforeinput', e => {
const targetRanges = e.getTargetRanges();
if(targetRanges[0].startContainer.parentElement.tagName === 'SPAN' ||
targetRanges[0].startContainer.parentElement.tagName === 'EM') {
e.preventDefault();
};
})
```


Here we respond to the `beforeinput`

event so that each time a change to the text is attempted, we get the target range that would be affected by the change, find out if it is inside a `<span>`

or `<em>`

element, and if so, run `preventDefault()`

to stop the edit happening. Voila — non-editable text regions inside editable text. Granted, this could be handled in other ways, but think beyond this trivial example — there is a lot of power to unlock here in terms of the control you’ve now got over text input.

## Security and privacy

Firefox 87 sees some valuable security and privacy changes.

### Referrer-Policy changes

First of all, the default [ Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) has been changed to

[(from](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy#strict-origin-when-cross-origin)

`strict-origin-when-cross-origin`

`no-referrer-when-downgrade`

), reducing the risk of leaking sensitive information in cross-origin requests. Essentially this means that by default, path and query string information are no longer included in HTTP Referrers.You can find out more about this change at [Firefox 87 trims HTTP Referrers by default to protect user privacy](https://blog.mozilla.org/security/2021/03/22/firefox-87-trims-http-referrers-by-default-to-protect-user-privacy/).

### SmartBlock

We also wanted to bring our new SmartBlock feature to the attention of our readers. SmartBlock provides stand-ins for tracking scripts blocked by Firefox (e.g. when in private browsing mode), getting round the often-experienced problem of sites failing to load or not working properly when those tracking scripts are blocked and therefore not present.

The provided stand-in scripts behave close enough to the original ones that they allow sites that rely on them to load and behave normally. And best of all, these stand-ins are bundled with Firefox. No communication needs to happen with the third-party at all, so the potential for any tracking to occur is greatly diminished, and the affected sites may even load quicker than before.

Learn more about SmartBlock at [Introducing SmartBlock](https://blog.mozilla.org/security/2021/03/23/introducing-smartblock/)

## VoiceOver support on macOS

Firefox 87 sees us shipping our VoiceOver screen reader support on macOS! No longer will you have to switch over to Chrome or Safari to do significant parts of your accessibility testing.

Check it out now, and let us know what you think.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.