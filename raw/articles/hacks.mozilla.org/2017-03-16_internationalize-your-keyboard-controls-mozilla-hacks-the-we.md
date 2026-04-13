---
title: Internationalize your keyboard controls – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/03/internationalize-your-keyboard-controls/
author: Julien Wajsberg
published: '2017-03-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Recently I came across two lovely new graphical demos, and in both cases, the controls would not work on my French [AZERTY keyboard](https://en.wikipedia.org/wiki/AZERTY).

There was the wonderful WebGL 2 technological demo [After The Flood](https://www.youtube.com/watch?v=TT7ugKuUMv0/), and the very cute [Alpaca Peck](http://codepen.io/shshaw/full/apwMwM/). [Shaw](http://codepen.io/shshaw/#) was nice enough to fix the latter when I told him about the issue. It turns out the web browser actually exposes a useful API for this.

Let’s investigate further.

## One keyboard, many layouts

People around the world use different keyboard layouts. You can read a lot on [Wikipedia’s keyboard layout page](https://en.wikipedia.org/wiki/Keyboard_layout), but I’ll try to summarise the important bits here.

The best-known and most widely used layout is [QWERTY](https://en.wikipedia.org/wiki/QWERTY), used in most of the world:

You may also know AZERTY, used in some French-speaking countries:

In addition, QWERTZ keyboards are in use in Germany and other European countries, and DVORAK is another alternative to QWERTY:

Each layout also has variants, especially in the symbols in the topmost row, as well as in the right-hand keys. Two keyboards of the same layout family might not be exactly the same. For example Spanish QWERTY keyboards have a special key for `ñ`

, and German QWERTZ keyboards have special keys for `ä`

and `ö`

.

You will notice that the keyboards have essentially the same structure for all layouts. For the most part, the keys are in the same location, although they can be slightly rearranged or adjusted. This is called the *mechanical layout*.

So a regional layout is made up of:

- The
*visual layout*is physically printed on the physical keys. - The
*functional layout*refers to the software (driver) that mapps hardware keys to characters.

This means **we can actually change the layout used in the operating system without changing the physical keyboard**. They are two different things! Some users will install [improved](http://users.sfr.be/denis.liegeois/kbdfrac.htm) [layout](https://github.com/fabi1cazenave/qwerty-lafayette) [drivers](http://marin.jb.free.fr/qwerty-fr/) to be able to type faster or to type specific characters more easily. This is very helpful when useful characters are not normally available in the layout. For example, to type in French, I can very easily reach `É`

, `È`

, `Ç`

or the french quotes `«`

and `»`

thanks to the driver I’m using.

But it comes also handy when you need to write text in several languages: I don’t have the `ø`

character anywhere on my keyboard but my driver allows me to type it in easily.

## What happens on the Web?

Well, [it used to be a complete mess](http://unixpapa.com/js/key.html). Then we converged to a cross-browser behavior quite appropriate for QWERTY keyboards.

The API we’ve grown used to revolves around the three events: `keydown`

, `keypress`

, and `keyup`

. `keydown`

and `keyup`

are called *key events* because they are fired each time a user presses any key, while `keypress`

is called a *character event* because it’s supposed to be fired when a *character* is sent as a result of the key press. All modern browsers seem to agree on this, even if it wasn’t always the case.

For this legacy API, we use the three properties of `KeyboardEvent`

: `keyCode`

, `charCode`

and `which`

. I won’t enter much into the details here, please believe me when I tell you this is a nightmare to work with:

- Properties don’t have the same meaning when handling a key event (
`keydown`

or`keyup`

) versus a character event (`keypress`

). - For some keys and events, the values are not consistent cross-browser, even for the latest browser versions.
`keyCode`

on key events tries to be international-friendly — no, really — but it fails miserably, because of the lack of a common specification.

So, let’s see what improvements the new API brings us!

## The new API, part of UI Events

[UI Events](https://w3c.github.io/uievents/), formerly known as DOM Level 3 Events, is a W3C specification in discussion since 2000. It’s still being discussed as a Working Draft, but because most browsers seem to agree today, we can hope that the specification will move forward to a recommendation. The latest [keyboard events working draft](https://w3c.github.io/uievents/#events-keyboardevents) is available online now.

The new API brings two new very useful properties to a `KeyboardEvent`

event: `key`

and `code`

. They replace the previously existing (and *still* existing) `charCode`

, `keyCode`

, and `which`

.

Let’s see why these changes are so useful, especially to do *cross-keyboard* websites (if you will allow me this neologism).

`KeyboardEvent.key`

gives you a printable character or a descriptive string

The property `key`

is almost a direct replacement for the previously used `which`

, except it’s a lot more predictable.

When the pressed key is a printable character, you get the character in string form (instead of its ASCII/Windows-1252 code for `which`

and `keyCode`

, or Unicode code for `charCode`

).

When the pressed key is not a printable character (for example: *Backspace*, *Control*, but also *Enter* or *Tab* which actually *are* printable characters), you get a multi-character descriptive string, like `'Backspace'`

, `'Control'`

, `'Enter'`

, `'Tab'`

.

Among major, modern desktop browsers, only Safari doesn’t support the property yet, but will in the next version.

`KeyboardEvent.code`

gives you the physical key

The property is completely new with this specification, although it is what `keyCode`

should have been.

It gives you, in a string form, the physical key that was pressed. This means it’s totally independent of the keyboard layout that is being used.

So let’s say the user presses the *Q* key on a QWERTY keyboard. Then `event.code`

gives you `'KeyQ'`

while `event.key`

gives you `'q'`

.

But when a AZERTY keyboard user presses the *A* key, he also gets `'KeyQ'`

as `event.code`

, yet `event.key`

contains `'a'`

. This happens because the *A* key on a AZERTY keyboard is at the same location as the *Q* key on a QWERTY keyboard.

As for numbers, the top digit bar yields values like `'Digit1'`

, while the numeric pad yields values like `'Numpad1'`

.

Unfortunately this feature is currently implemented only in Blink and Firefox, but Safari support is coming soon.

### The reference keyboard

*If each key triggers a specific code…*, then I can hear your next question. Which code is triggered for which key? What is the reference keyboard?

This is more complicated than it seems. There’s no existing keyboard with all the possible keys.

That’s why the W3C published [a specification just for this](https://www.w3.org/TR/uievents-code/). You can read about [the existing mechanical layouts](https://www.w3.org/TR/uievents-code/#keyboard-layout) around the world, [as well as their reference keyboard](https://www.w3.org/TR/uievents-code/#code-value-tables). For instance here is their reference keyboard for the alphanumerical part:

I encourage you to take a look and get at least an overview of this specification.

Please also note that the W3C has also published [a sibling specification describing the values for the key property](https://www.w3.org/TR/uievents-key/).

### The relationship between keys and codes

I highly recommend to read through [the examples given in the specification](https://w3c.github.io/uievents/#code-examples). They show very clearly what happens when the user presses various types of keys, both for `code`

and `key`

.

## Cross-browser controls

The wonderful Mozilla Developer Network offers a good example of [how to control a game using WASD or arrows](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/code#Handle_keyboard_events_in_a_game). But the example doesn’t run cross-browser, and in particular, it doesn’t work on Safari or Internet Explorer because they haven’t implemented the specification yet. So let’s look at how we can support some cross-browser code.

Of course, where the specification isn’t implemented, it won’t work properly on a non-QWERTY keyboard. For this reason, it’s a good idea to use the arrow keys as well, because they’re always at the same place everywhere. In this example, I also use the numeric pad and the IJKL keys, as they’re less likely to be at different locations.

Here’s an example of how JavaScript code can support both the new API and the older API.

```
window.addEventListener('keydown', function(e) {
if (e.defaultPrevented) {
return;
}
// We don't want to mess with the browser's shortcuts
if (e.ctrlKey || e.altKey || e.metaKey || e.shiftKey) {
return;
}
// We try to use `code` first because that's the layout-independent property.
// Then we use `key` because some browsers, notably Internet Explorer and
// Edge, support it but not `code`. Then we use `keyCode` to support older
// browsers like Safari, older Internet Explorer and older Chrome.
switch (e.code || e.key || e.keyCode) {
case 'KeyW': // This is 'W' on QWERTY keyboards, but 'Z' on AZERTY keyboards
case 'KeyI':
case 'ArrowUp':
case 'Numpad8':
case 38: // keyCode for arrow up
changeDirectionUp();
break;
// ... Other letters: ASD, JKL, arrows, numpad
default:
return;
}
e.preventDefault();
doSomethingUseful();
});
// touch handling
// A real implementation would want to use touchstart and touchend as well.
window.addEventListener('touchmove', function(e) {
// don't forget to throttle the event
});
```


## What’s missing?

The API itself is quite well done, not much is missing.

Yet I miss something. There is no way to know what the current keyboard layout is. This would be really useful for writing the instructions to control the game: `press WASD/ZQSD/...`

depending on the layout.

An API to know which letter is behind a specific key would also be useful. Yet I don’t know for sure if the underlying operating systems offer the necessary low-level calls to provide that information.

## Other useful things

Without entering into too much detail, let’s fly over some other significant functionalities in the API:

- The
`keypress`

event is deprecated. Now you should always use`keydown`

instead. The eventis also planned but isn’t supported to date by any stable version of a browser (Chrome Canary has an implementation). The event`beforeinput`

is a higher-level event supported by all browsers that is also useful in some situations.`input`

- With the
`location`

property on`KeyboardEvent`

, if a pressed key exists in several locations — e.g. the Shift or Ctrl keys, or the digits —, then you can know which one was actually used. For example, you can know whether the pressed key is in the numeric pad or on the digit top bar.

Note: This information is also contained in the`code`

property, as every physical key gets its own`code`

. - The
`repeat`

property is set to`true`

if the user keeps a key depressed and an event is sent repeatedly as a result. - If you want to know if a modifier key is depressed while handling another key’s
`KeyboardEvent`

, you don’t need to keep track of the state yourself. The boolean properties`altKey`

,`ctrlKey`

,`metaKey`

,`shiftKey`

, as well as the method[getModifierState](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/getModifierState), can give you the state of various modifier keys when the event was triggered.

Oddly enough, the keyboard events don’t seem to work properly on mobile platforms (iPhone untested). So be sure to have a touch interface as well!

## You can use it now

This is my conclusion: You can use this *now*! It’s possible to progressively enhance your game controller code by taking advantage of the newer API for modern browsers while supporting older browsers at the same time.

Your international users will thank you for this… by using your product :-)

## About
[
Julien Wajsberg ](https://everlong.org)

Using and contributing to the web since many years, Julien works for Mozilla since 2012. Former Firefox OS developer he's now part of the Firefox Developer Tools team.

## 3 comments

NoitidartMarch 17th, 2017 at 11:38Julien WajsbergMarch 17th, 2017 at 15:47Tomas KaplerMarch 24th, 2017 at 08:55