---
title: Keyboard events in Firefox OS TV – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/07/keyboard-events-in-firefox-os-tv/
author: Chun-Min Chang
published: '2015-07-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

### Getting started

The behavior of input events via hardware keys in Firefox OS varies widely from app to app. Early smartphones came with a limited number of keys — Power, Home, Volume up, Volume down — so it was easy for the software to determine an appropriate response for each keypress event. However, Smart TV remotes now come with many hardware keys, and defining the appropriate behavior when a key is pressed has become an important issue on the [Firefox OS TV](https://www.mozilla.org/en-US/firefox/os/devices/tv/) platform. If a hardware key on a smart remote can be used both by apps and by the system, it’s important to determine which response is triggered when the key is pressed.

This post will introduce the challenges of programming a TV remote to manage keyboard events on the Firefox OS Smart TV platform. We’ll classify keyboard events into four scenarios and describe these dispatch scenarios and how they interact. This is the first of two posts about keyboard events for Firefox OS Smart TV. In a followup [Part 2 post](https://hacks.mozilla.org/2015/08/keyboard-events-in-firefox-os-tv-part-2/), we’ll drill down into the implementation details and and take a look at sample code for event handling on the TV remote.

### Four keyboard event scenarios

To determine the appropriate behavior when hardware keys are pressed, we start by describing four scenarios for keyboard events.

| Scenario | Description | Event order |
|---|---|---|
| SYSTEM-ONLY | For keys which should be handled by mozbrowser-iframe-host-page only. |
system |
| SYSTEM-FIRST | For keys which can be handled by mozbrowser-iframe-host-page first and can then also be handled by mozbrowser-iframe-embedded-page. |
system->app |
| APP-CANCELLED | For keys which should be handled by the mozbrowser-iframe-embedded-page only. |
app |
| APP-FIRST | For keys which can be handled by mozbrowser-iframe-embedded-page first and can then also be handled by mozbrowser-iframe-host-page. |
app->system |

*[Table 1]*

The *mozbrowser-iframe-host-page* and *mozbrowser-iframe-embedded-page* mentioned in Table 1 are illustrated in Fig.2 above. If A.html represents a host page whose source is B.html, then A.html is the *mozbrowser-iframe-host-page*, and B.html is *mozbrowser-iframe-embedded-page*. `mozbrowser`

uses the non-standard Firefox [Browser API](https://developer.mozilla.org/en-US/docs/Web/API/Using_the_Browser_API), built for the implementation of key features and content experiences in Firefox OS apps. Learn more about [mozbrowser on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#attr-mozbrowser).

Suitable responses for any given keyboard event depend on the scenario. In the case illustrated above, let’s suppose that the ‘Info’ keyboard event is categorized as APP-FIRST and the default action set by system is to show system information. Thus, when we press the ‘Info’ key with app Z in the foreground, there are two possible results:

- If app Z has an event handler that tells the ‘Info’ key to show app information, then app information will appear on screen when the user presses the ‘Info’ key on the remote.
- If app Z doesn’t set an event handler for the ‘Info’ key, the default action is triggered. That is, the screen will show the system information.

### How to implement the four scenarios

To implement the four keyboard event scenarios described above, we’ve introduced four new keyboard events:

`mozbrowserbeforekeydown`

– fired**before**the*keydown*event`mozbrowserafterkeydown`

– fired**after**the*keydown*event`mozbrowserbeforekeyup`

– fired**before**the*keyup*event`mozbrowserafterkeyup`

– fired**after**the*keyup*event

These four keyboard events are only received by the *window* that embeds a mozbrowser-iframe.

The keyboard events occur in a specific sequence over time: `mozbrowserbeforekeydown`

, `mozbrowserafterkeydown`

, `mozbrowserbeforekeyup`

, `keyup`

, `mozbrowserafterkeyup`

.

This gives developers a way to implement the four scenarios mentioned above. Conceptually, the scenarios SYSTEM-ONLY, SYSTEM-FIRST and APP-CANCELLED, APP-FIRST can be implemented by setting proper handlers for the `mozbrowserbeforekey*`

and `mozbrowserafterkey*`

events. The SYSTEM-ONLY and SYSTEM-FIRST scenarios can be implemented by setting proper handlers for `mozbrowserbeforekey*`

events and the APP-CANCELLED and APP-FIRST scenarios can be implemented via `mozbrowserafterkey*`

events.

##### iframe structure in Firefox OS

To understand how to implement the four scenarios, let’s first take a look at iframe structure in Firefox OS. The outermost iframe in Firefox OS is[shell.html](https://dxr.mozilla.org/mozilla-central/source/b2g/chrome/content/shell.html). It embeds an

**in-process**iframe which is sourced from

[system/index.html](https://github.com/mozilla-b2g/gaia/blob/master/apps/system/index.html). The system app (system/index.html) contains several web apps (essentially iframes) which can be

**in-process**(

[remote](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#attr-remote)=”false”) or

**out-of-process**(remote=”true”). As a result, the relationship of these three layers can be displayed in the following table:

| mozbrowser iframe host page | mozbrowser iframe embedded page |
|---|---|
| shell.html | system/index.html |
| system/index.html | web apps(essentially iframes) |

*[Table 2]*

##### Dispatch order of keyboard events

When a*keydown*event is sent to some element in a

*mozbrowser-iframe-embedded-page*, the owner of the embedded iframe, i.e., the mozbrowser-iframe-host-page, will receive the

`mozbrowserbeforekeydown`

event before the *keydown*event is sent and the

`mozbrowserafterkeydown`

event after the event is sent to the *mozbrowser-iframe-embedded-page*.

In Gecko, once there is one *keydown* event with the target in an out-of-process iframe embedded in an HTML document, the *keydown* event is duplicated to the HTML document as well. The target of this duplicated event is set as the embedded iframe element.

This results in the keyboard event sequence shown in Fig 4. It illustrates all related *keydown* events and their relationship when a *keydown* event with a target in a *mozbrowser-iframe-embedded-page* needs to be dispatched. In brief, events follow this sequence:

- Before dispatching any
*keydown*event, the`mozbrowserbeforekeydown`

event is first dispatched to the window of*mozbrowser-iframe-host-page*. - Then, the original
*keydown*event (with a target in a*mozbrowser-iframe-embedded-page*) will be duplicated to the*mozbrowser-iframe-host-page*HTML document. Its target will be set to be the iframe that contains the*mozbrowser-iframe-embedded-page*. - Next, the original
*keydown*event will be dispatched to its target. - After the original
*keydown*event dispatch is complete, the`mozbrowserafterkeydown`

event will be dispatched to the window of*mozbrowser-iframe-host-page*.

Notice that the event dispatch process described above follows the [DOM tree event flow](http://www.w3.org/TR/DOM-Level-3-Events/#event-flow). Event sequence and event targets can be organized into the following table:

| Order | event | target |
|---|---|---|
| 1 | mozbrowserbeforekeydown |
window in mozbrowser-iframe-host-page |
| 2 | keydown |
iframe that contains the mozbrowser-iframe-embedded-page in mozbrowser-iframe-host-page |
| 3 | keydown |
original one in mozbrowser-iframe-embedded-page |
| 4 | mozbrowserafterkeydown |
window in mozbrowser-iframe-host-page |

*[Table 3]*

`mozbrowserbeforekeydown`

, `keydown`

, and `mozbrowserafterkeydown`

, can be extended to nested mozbrowser iframes, like the iframe structure in Firefox OS described in Table 2. In this case, the `mozbrowserbeforekeydown`

and `mozbrowserafterkeydown`

events will be dispatched to the innermost *mozbrowser-iframe-host-page*as well as the outer one. Thus, in Firefox OS,

`mozbrowserkeydown`

and `mozbrowserafterkeydown`

will be dispatched to the window of system/index.html and the window of shell.html. Fig. 5 illustrates the whole dispatch sequence of related events when a *keydown*event is dispatched to a web app. The sequence of events is demonstrated in Table 4.

| Order | event | target |
|---|---|---|
| 1 | mozbrowserbeforekeydown |
window in shell.html |
| 2 | mozbrowserbeforekeydown |
window in system/index.html |
| 3 | keydown |
iframe that contains the web app in system/index.html |
| 4 | keydown |
original one in web app |
| 5 | mozbrowserafterkeydown |
window in system/index.html |
| 6 | mozbrowserafterkeydown |
window in shell.html |

*[Table 4]*

*keyup*event must be fired after

*keydown*, the

*keydown*event and the

*keyup*event are independent of each other. Moreover, the path

`mozbrowserbeforekeyup`

, `keyup`

, `mozbrowserafterkeyup`

is independent of the path `mozbrowserbeforekeydown`

, `keydown`

, `mozbrowserafterkeydown`

. Therefore, it’s possible for these two paths to cross each other. The `mozbrowserbeforekeyup`

may arrive before the *keydown*event.

In Firefox OS, most apps run **out-of-process**. This means that the app runs on its own process, not on the main process. After dispatching a given *key** event (the duplicate) to the system app, it takes time to send the original *key** event to the process where the *mozbrowser-iframe-embedded-page* is located. In a similar manner, after a given key* event is dispatched to the *mozbrowser-iframe-embedded-page*’s process, time is required to send `mozbrowserafterkey*`

back to the process where the *mozbrowser-iframe-host-page* is located.

Consequently, the `mozbrowserbeforekeyup`

event may arrive in the main Firefox OS process (where the system app lives), before the *keydown* event is dispatched to the app’s own process. Common results of the order of the *key** events are demonstrated above in Fig. 6. The yellow series represents the *keydown* path, and the blue series show the *keyup* path. And yes, these two paths may cross each other.

### Next steps

If you’re looking for implementation details for the four scenarios we’ve described, as well as event handler sample code to help with your implementation of keyboard events for smart TV remotes, keep an eye out for [the followup post](https://hacks.mozilla.org/2015/08/keyboard-events-in-firefox-os-tv-part-2/), and stay tuned for more complete documentation arriving very soon on MDN.

## One comment

MiguelAugust 26th, 2015 at 07:48