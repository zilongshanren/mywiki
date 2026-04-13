---
title: The Gamepad API – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/12/the-gamepad-api/
author: Ted Mielczarek
published: '2013-12-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I’ve been fascinated by video games since I was a kid. From the Atari and Colecovision to the NES and Super NES, I’ve spent countless hours playing a variety of games. While my own video game playing has tapered off, I’m still interested in the issues and advancements surrounding gaming. I’ve watched the recent popularity explosion of web gaming and am positive that it’s going to herald a new era of gaming, with a tremendous number of games available to a wide audience. However, one thing struck me while exploring the burgeoning web gaming scene–many of these games would be a lot more fun to play with a gamepad! I set out to remedy that by implementing something for Firefox and thus the [Gamepad API](http://www.w3.org/TR/gamepad/) was born.

## Enabling the API

As of Firefox 24, the Gamepad API is available behind a preference. You can enable it by loading `about:config`

and setting the `dom.gamepad.enabled`

preference to true. Nightly and Aurora builds of Firefox have the API enabled by default. We expect to ship release builds with it similarly enabled in Firefox 28.

## Using the API

The Gamepad API was designed to be very simple. The spec intentionally only attempts to describe an interface for working with traditional Gamepad controllers—a collection of buttons and axes. We felt that this covers the majority of the gaming controllers that are out there, while avoiding the complexity of trying to specify an API that covers everything in existence. The API consists of one function call, a few DOM events, and one type of object to work with.

### Getting a Gamepad

As implemented, gamepads will not be exposed to a webpage unless the user interacts with them while the page is visible. This is for privacy reasons, mostly to prevent them from being used in fingerprinting a user’s system. If the user interacts with (presses a button, moves a stick) a controller while the page is visible a `<a href="https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#the-gamepadconnected-event">gamepadconnected</a>`

event will be sent to the page.

The `<a href="https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#gamepadevent-interface">GamepadEvent</a>`

object has a `<a href="https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-GamepadEvent-gamepad">gamepad</a>`

property that describes the device in question. In Firefox, once one gamepad has been exposed to a page, connecting any other gamepad to the system (by plugging in a USB gamepad or associating a Bluetooth gamepad) will immediately expose that device to the page and send a `gamepadconnected`

event.

The Gamepad API also provides a function–`<a href="https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#methods">navigator.getGamepads()</a>`

–that returns a list of all devices currently visible to the webpage. Each gamepad visible to the page is returned at the position in the list specified by its `index`

property.

Note: this code snippet will work in Firefox 28 nightly builds but not in older builds due to [a bug that was just recently fixed](https://bugzilla.mozilla.org/show_bug.cgi?id=936104).

If a gamepad is disconnected–by being unplugged, for example–a `<a href="https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#the-gamepaddisconnected-event">gamepaddisconnected</a>`

event is fired at the page. Any lingering references to the `Gamepad`

object will have their `connected`

property set to `false`

.

### The Gamepad object

The [Gamepad object](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#gamepad-interface) represents the state of a game controller. It has several properties that describe the controller:

[id](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-Gamepad-id)- A string containing some information about the controller. This is not strictly specified, but in Firefox it will contain three pieces of information separated by dashes (
`-`

): two 4-digit hexadecimal strings containing the USB vendor and product id of the controller, and the name of the controller as provided by the driver. This information is intended to allow you to find a mapping for the controls on the device as well as display useful feedback to the user. [index](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-Gamepad-index)- An integer that is unique for each device currently connected to the system. This can be used to distinguish multiple controllers.
[connected](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-Gamepad-connected)- A boolean:
`true`

if the controller is still connected,`false`

if it has been disconnected. [mapping](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-Gamepad-mapping)- A string indicating whether the browser has remapped the controls on the device to a known layout. Currently there is only one supported known layout–the “
[standard gamepad](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#remapping)“. If the browser is able to map controls on the device to that layout the`mapping`

property will be set to the string`standard`

. [axes](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-Gamepad-axes)- An array of floating point values containing the state of each axis on the device. Usually these represent analog sticks, with a pair of axes giving the position of the stick in its X and Y axes. Each axis is normalized to the range of -1.0..1.0, with -1.0 representing the up or left-most position of the axis, and 1.0 representing the down or right-most position of the axis.
[buttons](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-Gamepad-buttons)- An array of
[GamepadButton objects](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#gamepadbutton-interface)containing the state of each button on the device. Each`GamepadButton`

has a`<a href="https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-GamepadButton-pressed">pressed</a>`

and a`<a href="https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-GamepadButton-value">value</a>`

property. The`pressed`

property is a boolean indicating whether the button is currently pressed (`true`

) or unpressed (`false`

). The`value`

property is a floating point value used to enable representing analog buttons, such as the triggers on many modern gamepads. The values are normalized to the range 0.0..1.0, with 0.0 representing a button that is not pressed, and 1.0 representing a button that is fully pressed.

## Cross-browser compatibility

The [Gamepad API specification](http://www.w3.org/TR/gamepad/) is implemented in both Firefox and Chrome, to varying degrees of compatibility. Currently Firefox implements the entirety of [the editor’s draft](https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html) with the exception of the `<a href="https://dvcs.w3.org/hg/gamepad/raw-file/default/gamepad.html#widl-Gamepad-timestamp">timestamp</a>`

property on `Gamepad`

objects.

As of this writing, Chrome does not implement the `ongamepadconnected`

or `ongamepaddisconnected`

events. You must use the `navigator.webkitGetGamepads()`

function (note the prefix) to access gamepads.

Another difference to note is that `Gamepad`

objects are snapshots in Chrome, whereas they always reflect the latest state of the controller in Firefox. This means that for Chrome you will need to poll the set of gamepads with `navigator.webkitGetGamepads()`

each frame, whereas in Firefox you can hold a reference to a `Gamepad`

object in a variable and refer to it later to check the current state.

Finally, a recent spec change means Chrome and release versions of Firefox have a difference from Firefox 28—the `buttons`

property of the `Gamepad`

object was originally specified as an array of doubles, not an array of `GamepadButton`

objects. This can be handled safely with a simple type check, as the following code sample shows.

## A simple demo

I’ll leave you with [a simple demo](http://luser.github.io/gamepadtest/) that puts all the pieces here together and shows how you can use the API today in a cross-browser fashion. It simply looks for gamepads being connected or disconnected and displays the current state of the buttons and axes of all known controllers. This demo should work in any version of Firefox from 24 onwards and in Chrome from version 21 onwards. You can find [the source of the demo on Github](https://github.com/luser/gamepadtest).

I hope this post inspires you to rethink what is possible in gaming on the web. Let’s go make some games!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 17 comments

Dietrich AyalaDecember 19th, 2013 at 10:20Ted MielczarekDecember 19th, 2013 at 13:46Jason HutchinsonDecember 23rd, 2013 at 09:15soleDecember 19th, 2013 at 11:54Robert Nyman [Editor]December 20th, 2013 at 09:08Hugo HabelDecember 19th, 2013 at 16:58Robert Nyman [Editor]December 20th, 2013 at 09:07Šime VidasDecember 19th, 2013 at 23:34Robert Nyman [Editor]December 20th, 2013 at 09:08ilyasDecember 20th, 2013 at 00:21Robert Nyman [Editor]December 20th, 2013 at 09:08AndyDecember 22nd, 2013 at 07:30Ted MielczarekDecember 23rd, 2013 at 10:10thinsoldierDecember 23rd, 2013 at 09:36JajaDecember 30th, 2013 at 23:58Ted MielczarekDecember 31st, 2013 at 09:57Dread KnightJanuary 17th, 2014 at 13:12