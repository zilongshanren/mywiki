---
title: 'Keyboard events in Firefox OS TV: Part 2 – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2015/08/keyboard-events-in-firefox-os-tv-part-2/
author: Chun-Min Chang
published: '2015-08-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

### Implementation details for keyboard events

In our introductory post, [Keyboard events in Firefox OS TV](https://hacks.mozilla.org/2015/07/keyboard-events-in-firefox-os-tv/), we described four keyboard event scenarios triggered by the Info key on a Smart TV remote: SYSTEM-ONLY, SYSTEM-FIRST, APP-CANCELLED, AND APP-FIRST. We explained how these keyboard events are activated, described the default sequence of events, and explored the iframe structure in Firefox OS and its embedded browser, in order to understand how developers can implement the four keyboard event scenarios.

Now we’ll take a closer look at each of the four scenarios, complete with example code for each event-handling scenario.

###### SYSTEM-ONLY

If a keyboard event is categorized as **SYSTEM-ONLY**, then the desired response is defined in *mozbrowserbeforekey**’s event handler. Once this key is pressed, the system receives the *mozbrowserbeforekey** event before the *key** event is dispatched to an app. In addition, the *key** events dispatch is cancelled once the system event handler is called. Now, we need to figure out a way to stop the event dispatch. [ Fig 5 – Keyboard events in Firefox OS TV](https://2r4s9p1yi1fa2jd7j43zph8r-wpengine.netdna-ssl.com/files/2015/07/f5.png) shows that the keyboard events are dispatched to the system process, then also to the app process. To stop dispatching events to the

*the embedded page*,

[is a straightforward solution.](https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault)

*event.preventDefault()**Event.preventDefault()*is used to prevent the

*default action*. The defined

*default action*of the

*mozbrowserbeforekey** event is to dispatch the

*key** event. For this reason, by calling

*event.preventDefault()*in

*mozbrowserbeforekey**’s event handler,

*key** events won’t be dispatched. The final result will be the same as shown in Fig 7.

###### SYSTEM-FIRST

This is very similar to the implementation of **SYSTEM-ONLY**. The only difference — it’s not necessary to call *event.preventDefault()* in *mozbrowserbeforekey**’s event handler. Apps are able to handle the *key** event after the system finishes processing it.

###### APP-CANCELLED

If specific keyboard events are designated for use by apps only, such as those assigned to the four colored keys (shown in Fig 9) on smart TV remotes, then *event.preventDefault()* will be called in the app’s *key** event handler. The *event.preventDefault()* cannot prevent the *mozbrowserafterkey** event from being dispatched to the system, but the property *embeddedCancelled* of *mozbrowserafterkey** will be set to **true** once the embedded app calls *event.preventDefault()*. The value of *embeddedCancelled* lets the system detect whether or not this event has been handled already. If this value is true, the system does nothing.

###### APP-FIRST

The difference between **APP-FIRST** and **APP-CANCELLED** is that with **APP-FIRST** *event.preventDefault()* will not be called in the app’s event handler. Therefore, the value of *embeddedCancelled* is **false** and the system can take over the keyboard event.

### Sample code

##### Event handlers

```
function handleEvent(event) {
dump("Receive event '" + event.type + "'.");
// Handle event here.....
};
function handleEventAndPreventDefault(event) {
dump("Receive event '" + event.type + "'.");
// Handle event here.....
// Call preventDefault() to stop the default action.
// It means that the event is already handled.
event.preventDefault();
};
function checkAttrAndHandleEvent(event) {
dump("Receive event '" + event.type +
"' with embeddedCancelled equals to '" +
event.embeddedCancelled + "'.");
if (!event.embeddedCancelled) {
// Do something if the event wasn't being handled before!
// The following code should be executed in APP-FIRST scenario only!
}
};
```


##### SYSTEM-ONLY

- mozbrowser iframe host page

```
window.addEventListener('mozbrowserbeforekeydown', handleEventAndPreventDefault);
window.addEventListener('mozbrowserbeforekeyup', handleEventAndPreventDefault);
window.addEventListener('mozbrowserafterkeydown', function() { }); // no use
window.addEventListener('mozbrowserafterkeyup', function() { }); // no use
```


- the embedded page

```
// This function will never be triggered because the preventDefault() is called in mozbrowserbeforekeyXXX's handler.
window.addEventListener('keydown', handleEvent);
window.addEventListener('keyup', handleEvent);
```


- Results of
*keydown*related events

| Order | the embedded page | mozbrowser iframe host page | Output |
|---|---|---|---|
| 1 | mozbrowserbeforekeydown | Receive event ‘mozbrowserbeforekeydown’. | |
| 2 | mozbrowserafterkeydown |

- Results of
*keyup*related events

| Order | the embedded page | the host page | Output |
|---|---|---|---|
| 1 | mozbrowserbeforekeyup | Receive event ‘mozbrowserbeforekeyup’. | |
| 2 | mozbrowserafterkeyup |

##### SYSTEM-FIRST

- mozbrowser iframe host page

```
window.addEventListener('mozbrowserbeforekeydown', handleEvent);
window.addEventListener('mozbrowserbeforekeyup', handleEvent);
window.addEventListener('mozbrowserafterkeydown', function() { }); // no use
window.addEventListener('mozbrowserafterkeyup', function() { }); // no use
```


- the embedded page

```
window.addEventListener('keydown', handleEvent);
window.addEventListener('keyup', handleEvent);
```


- Received results of
*keydown*related events

| Order | mozbrowser-embedded page | mozbrowser iframe host page | Output |
|---|---|---|---|
| 1 | mozbrowserbeforekeydown | Receive event ‘mozbrowserbeforekeydown’. | |
| 2 | keydown | Receive event ‘keydown’. | |
| 3 | mozbrowserafterkeydown |

- Received results of
*keyup*related events

| Order | the embedded page | mozbrowser iframe host page | Output |
|---|---|---|---|
| 1 | mozbrowserbeforekeyup | Receive event ‘mozbrowserbeforekeyup’. | |
| 2 | keyup | Receive event ‘keyup’. | |
| 3 | mozbrowserafterkeyup | Receive event ‘mozbrowserafterkeyup’ with embeddedCancelled equals to ‘true’. |

##### APP-CANCELLED

- mozbrowser iframe host page

```
window.addEventListener('mozbrowserbeforekeydown', function() { }); // no use
window.addEventListener('mozbrowserbeforekeyup', function() { }); // no use
window.addEventListener('mozbrowserafterkeydown', checkAttrAndHandleEvent);
window.addEventListener('mozbrowserafterkeyup', checkAttrAndHandleEvent);
```


- mozbrowser iframe embedded page

```
window.addEventListener('keydown', handleEventAndPreventDefault);
window.addEventListener('keyup', handleEventAndPreventDefault);
```


- Received results of
*keydown*related events

| Order | the embedded page | mozbrowser iframe host page | Output |
|---|---|---|---|
| 1 | mozbrowserbeforekeydown | ||
| 2 | keydown | Receive event ‘keydown’. | |
| 3 | mozbrowserafterkeydown | Receive event ‘mozbrowserafterkeydown’ with embeddedCancelled equals to ‘true’. |

- Received results of keyup related events

| Order | mozbrowser-embedded page | mozbrowser iframe host page | Output |
|---|---|---|---|
| 1 | mozbrowserbeforekeyup | ||
| 2 | keyup | Receive event ‘keyup’. | |
| 3 | mozbrowserafterkeyup | Receive event ‘mozbrowserafterkeyup’ with embeddedCancelled equals to ‘true’. |

##### APP-FIRST

- mozbrowser iframe host page

```
window.addEventListener('mozbrowserbeforekeydown', function() { }); // no use
window.addEventListener('mozbrowserbeforekeyup', function() { }); // no use
// This will be trigger after keydown event is
// dispatched to mozbrowser iframe embedded page
window.addEventListener('mozbrowserafterkeydown', checkAttrAndHandleEvent);
window.addEventListener('mozbrowserafterkeyup', checkAttrAndHandleEvent);
```


- mozbrowser iframe embedded page

```
window.addEventListener('keydown', handleEvent);
window.addEventListener('keyup', handleEvent);
```


- Received results of
*keydown*related events

| Order | mozbrowser-embedded page | mozbrowser-iframe host page | Output |
|---|---|---|---|
| 1 | mozbrowserbeforekeydown | ||
| 2 | keydown | Receive event ‘keydown’. | |
| 3 | mozbrowserafterkeydown | Receive event ‘mozbrowserafterkeydown’ with embeddedCancelled equals to ‘false’. |

- Received results of
*keyup*related events

| Order | mozbrowser-embedded page | mozbrowser iframe host page | Output |
|---|---|---|---|
| 1 | mozbrowserbeforekeyup | ||
| 2 | keyup | Receive event ‘keyup’. | |
| 3 | mozbrowserafterkeyup | Receive event ‘mozbrowserafterkeyup’ with embeddedCancelled equals to ‘false’. |