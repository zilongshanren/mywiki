---
title: 'Detecting touch: it''s the ''why'', not the ''how'' – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2013/04/detecting-touch-its-the-why-not-the-how/
author: Patrick H Lauke
published: '2013-04-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One common aspect of making a website or application “mobile friendly” is the inclusion of tweaks, additional functionality or interface elements that are particularly aimed at touchscreens. A very common question from developers is now “How can I detect a touch-capable device?”

## Feature detection for touch

Although there used to be a few incompatibilities and proprietary solutions in the past (such as [Mozilla’s experimental, vendor-prefixed event model](https://developer.mozilla.org/en-US/docs/DOM/Touch_events_(Mozilla_experimental))), almost all browsers now implement the same [Touch Events](http://www.w3.org/TR/touch-events/) model (based on a solution first introduced by Apple for iOS Safari, which subsequently was adopted by other browsers and retrospectively turned into a W3C draft specification).

As a result, being able to programmatically detect whether or not a particular browser supports touch interactions involves a very simple feature detection:

```
if ('ontouchstart' in window) {
/* browser with Touch Events
running on touch-capable device */
}
```

This snippet works reliably in modern browser, but older versions notoriously had a few quirks and inconsistencies which required jumping through various different detection strategy hoops. If your application is targetting these older browsers, I’d recommend having a look at [Modernizr](http://modernizr.com) – and in particular its various [touch test approaches](http://modernizr.github.com/Modernizr/touch.html) – which smooths over most of these issues.

I noted above that “almost all browsers” support this touch event model. The big exception here is Internet Explorer. While up to IE9 there was no support for any low-level touch interaction, IE10 introduced support for Microsoft’s own [Pointer Events](http://www.w3.org/Submission/pointer-events/). This event model – which has since been submitted for W3C standardisation – unifies “pointer” devices (mouse, stylus, touch, etc) under a single new class of events. As this model does not, by design, include any separate ‘touch’, the feature detection for `ontouchstart`

will naturally not work. The suggested method of detecting if a browser using Pointer Events is running on a touch-enabled device instead involves checking for the existence and return value of `navigator.maxTouchPoints`

(note that Microsoft’s Pointer Events are currently still vendor-prefixed, so in practice we’ll be looking for `navigator.msMaxTouchPoints`

). If the property exists and returns a value greater than `0`

, we have touch support.

```
if (navigator.msMaxTouchPoints > 0) {
/* IE with pointer events running
on touch-capable device */
}
```

Adding this to our previous feature detect – and also including the non-vendor-prefixed version of the Pointer Events one for future compatibility – we get a still reasonably compact code snippet:

```
if (('ontouchstart' in window) ||
(navigator.maxTouchPoints > 0) ||
(navigator.msMaxTouchPoints > 0)) {
/* browser with either Touch Events of Pointer Events
running on touch-capable device */
}
```

## How touch detection is used

Now, there are already quite a few commonly-used techniques for “touch optimisation” which take advantage of these sorts of feature detects. The most common use cases for detecting touch is to increase the responsiveness of an interface for touch users.

When using a touchscreen interface, browsers introduce an artificial delay (in the range of about 300ms) between a touch action – such as tapping a link or a button – and the time the actual click event is being fired.

More specifically, in browsers that support Touch Events the delay happens between `touchend`

and the simulated mouse events that these browser also fire for compatibility with mouse-centric scripts:

`touchstart > [touchmove]+ > touchend > <strong> delay </strong> > mousemove > mousedown > mouseup > click`


See the [event listener test page](http://mozilla.github.io/mozhacks/touch-events/event-listener.html) to see the order in which events are being fired, [code available on GitHub](https://github.com/mozilla/mozhacks/blob/gh-pages/touch-events/event-listener.html).

This delay has been introduced to allow users to double-tap (for instance, to zoom in/out of a page) without accidentally activating any page elements.

It’s interesting to note that Firefox and Chrome on Android have removed this delay for pages with a fixed, non-zoomable viewport.

<meta name="viewport" value="...user-scalable = no...">

See the [event listener with user-scalable=no test page](http://mozilla.github.io/mozhacks/touch-events/event-listener_user-scalable-no.html),

[code available on GitHub](https://github.com/mozilla/mozhacks/blob/gh-pages/touch-events/event-listener_user-scalable-no.html).

There is some discussion of tweaking Chrome’s behavior further for other situations – see [issue 169642 in the Chromium bug tracker](https://code.google.com/p/chromium/issues/detail?id=169642).

Although this affordance is clearly necessary, it can make a web app feel slightly laggy and unresponsive. One common trick has been to check for touch support and, if present, react directly to a touch event (either `touchstart`

– as soon as the user touches the screen – or `touchend`

– after the user has lifted their finger) instead of the traditional `click`

:

```
/* if touch supported, listen to 'touchend', otherwise 'click' */
var clickEvent = ('ontouchstart' in window ? 'touchend' : 'click');
blah.addEventListener(clickEvent, function() { ... });
```

Although this type of optimisation is now widely used, it is based on a logical fallacy which is now starting to become more apparent.

The artificial delay is also present in browsers that use Pointer Events.

`pointerover > mouseover > pointerdown > mousedown > pointermove > mousemove > pointerup > mouseup > pointerout > mouseout > <strong>delay</strong> > click`


Although it’s possible to extend the above optimisation approach to check `navigator.maxTouchPoints`

and to then hook up our listener to `pointerup`

rather than `click`

, there is a much simpler way: setting the [ touch-action CSS property](http://www.w3.org/Submission/pointer-events/#the-touch-action-css-property) of our element to

`none`

eliminates the delay.```
/* suppress default touch action like double-tap zoom */
a, button {
-ms-touch-action: none;
touch-action: none;
}
```

See the [event listener with touch-action:none test page](http://mozilla.github.io/mozhacks/touch-events/event-listener_touch-action-none.html),

[code available on GitHub](https://github.com/mozilla/mozhacks/blob/gh-pages/touch-events/event-listener_touch-action-none.html).

## False assumptions

It’s important to note that these types of optimisations based on the availability of touch have a fundamental flaw: they make assumptions about user behavior based on device capabilities. More explicitly, the example above assumes that because a device is capable of touch input, a user will in fact use touch as the only way to interact with it.

This assumption probably held some truth a few years back, when the only devices that featured touch input were the classic “mobile” and “tablet”. Here, touchscreens were the only input method available. In recent months, though, we’ve seen a whole new class of devices which feature both a traditional laptop/desktop form factor (including a mouse, trackpad, keyboard) *and* a touchscreen, such as the various [Windows 8 machines](http://windows.microsoft.com/en-us/windows-8/new-pcs) or [Google’s Chromebook Pixel](http://www.google.com/intl/en_uk/chrome/devices/chromebook-pixel/).

As an aside, even in the case of mobile phones or tablets, it was already possible – on some platforms – for users to add further input devices. While iOS only caters for pairing an additional bluetooth keyboard to an iPhone/iPad purely for text input, Android and Blackberry OS also let users add a mouse.

On Android, this mouse will act exactly like a “touch”, even firing the same sequence of touch events and simulated mouse events, including the dreaded delay in between – so optimisations like our example above will still work fine. Blackberry OS, however, purely fires mouse events, leading to the same sort of problem outlined below.

The implications of this change are slowly beginning to dawn on developers: that touch support does not necessarily mean “mobile” anymore, and more importantly that even if touch is available, it may not be the primary or exclusive input method that a user chooses. In fact, a user may even transition between any of their available input methods in the course of their interaction.

The innocent code snippets above can have quite annoying consequences on this new class of devices. In browsers that use Touch Events:

`var clickEvent = ('ontouchstart' in window ? 'touchend' : 'click');`

is basically saying “if the device support touch, only listen to `touchend`

and not `click`

” – which, on a multi-input device, immediately shuts out any interaction via mouse, trackpad or keyboard.

## Touch *or* mouse?

So what’s the solution to this new conundrum of touch-capable devices that may also have other input methods? While some developers have started to look at complementing a touch feature detection with additional user agent sniffing, I believe that the answer – as in so many other cases in web development – is to accept that we can’t fully detect or control how our users will interact with our web sites and applications, and to be input-agnostic. Instead of making assumptions, our code should cater for all eventualities. Specifically, instead of making the decision about whether to react to `click`

or `touchend`

/`touchstart`

mutually exclusive, these should all be taken into consideration as complementary.

Certainly, this may involve a bit more code, but the end result will be that our application will work for the largest number of users. One approach, already familiar to developers who’ve strived to make their mouse-specific interfaces also work for keyboard users, would be to simply “double up” your event listeners (while taking care to prevent the functionality from firing twice by stopping the simulated mouse events that are fired following the touch events):

```
blah.addEventListener('touchend', function(e) {
/* prevent delay and simulated mouse events */
e.preventDefault();
someFunction()
});
blah.addEventListener('click', someFunction);
```

If this isn’t DRY enough for you, there are of course fancier approaches, such as only defining your functions for `click`

and then bypassing the dreaded delay by explicitly firing that handler:

```
blah.addEventListener('touchend', function(e) {
/* prevent delay and simulated mouse events */
e.preventDefault();
/* trigger the actual behavior we bound to the 'click' event */
e.target.click();
})
blah.addEventListener('click', function() {
/* actual functionality */
});
```

That last snippet does not cover all possible scenarios though. For a more robust implementation of the same principle, see the [FastClick](https://github.com/ftlabs/fastclick) script from [FT labs](http://labs.ft.com/).

## Being input-agnostic

Of course, battling with delay on touch devices is not the only reason why developers want to check for touch capabilities. Current discussions – such as this issue in Modernizr about [detecting a mouse user](https://github.com/Modernizr/Modernizr/issues/869) – now revolve around offering completely different interfaces to touch users, compared to mouse or keyboard, and whether or not a particular browser/device supports things like hovering. And even beyond JavaScript, similar concepts (`pointer`

and `hover`

media features) are being proposed for [Media Queries Level 4](http://dev.w3.org/csswg/mediaqueries4/). But the principle is still the same: as there are now common multi-input devices, it’s not straightforward (and in many cases, impossible) anymore to determine if a user is on a device that *exclusively* supports touch.

The more generic approach taken in Microsoft’s Pointer Events specification – which is already being scheduled for implementation in other browser such as Chrome – is a step in the right direction (though it still requires extra handling for keyboard users). In the meantime, developers should be careful not to draw the wrong conclusions from touch support detection and avoid unwittingly locking out a growing number of potential multi-input users.

## Further links

[The Good & Bad of Level 4 Media Queries](http://www.stucox.com/blog/the-good-and-bad-of-level-4-media-queries/)[Handling Multi-touch and Mouse Input in All Browsers](http://blogs.msdn.com/b/ie/archive/2011/10/19/handling-multi-touch-and-mouse-input-in-all-browsers.aspx)[Hand.js: a polyfill for supporting pointer events on every browser](http://blogs.msdn.com/b/eternalcoding/archive/2013/01/16/hand-js-a-polyfill-for-supporting-pointer-events-on-every-browser.aspx)[Touch And Mouse – Together Again For The First Time](http://www.html5rocks.com/en/mobile/touchandmouse/)[Prototype Chromium build with support for MS Pointer Events](http://appendto.com/blog/2013/02/prototype-chromium-build-with-support-for-ms-pointer-events/)[Webseiten zum Anfassen](http://webkrauts.de/artikel/2012/einfuehrung-touch-events)(in German)[Generalized Input On The Cross-Device Web](http://smus.com/mouse-touch-pointer/)

## About
[
Patrick H. Lauke ](http://www.splintered.co.uk)

[@patrick_h_lauke](https://twitter.com/patrick_h_lauke) has been engaged in the discourse on standards and accessibility since early 2001. Until recently, Patrick worked as Web Evangelist in the Developer Relations team at Opera Software. An outspoken accessibility and standards advocate, Patrick favours a pragmatic hands-on approach over purely theoretical, high-level discussions.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 21 comments

Robert KaiserApril 9th, 2013 at 06:09Patrick H. LaukeApril 9th, 2013 at 06:26AndreaApril 9th, 2013 at 06:34Patrick H. LaukeApril 9th, 2013 at 07:04AndreaApril 9th, 2013 at 07:20Mary BranscombeApril 9th, 2013 at 08:05Stu CoxApril 9th, 2013 at 08:30Patrick H. LaukeApril 9th, 2013 at 12:25Patrick H. LaukeApril 9th, 2013 at 12:30Jake ArchibaldApril 9th, 2013 at 22:42DominykasApril 10th, 2013 at 23:46Patrick H. LaukeApril 12th, 2013 at 04:39Patrick H. LaukeApril 14th, 2013 at 05:27Patrick H. LaukeApril 14th, 2013 at 05:30DominykasApril 14th, 2013 at 22:38Patrick H. LaukeApril 15th, 2013 at 00:26Patrick H. LaukeApril 15th, 2013 at 08:07Andrew D. ToddApril 15th, 2013 at 13:41brothercakeApril 21st, 2013 at 02:56JApril 22nd, 2013 at 05:59Patrick H. LaukeApril 22nd, 2013 at 06:57