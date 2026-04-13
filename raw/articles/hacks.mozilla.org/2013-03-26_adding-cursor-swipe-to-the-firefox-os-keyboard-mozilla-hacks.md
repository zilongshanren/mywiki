---
title: Adding cursor swipe to the Firefox OS keyboard – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/03/adding-cursor-swipe-to-the-firefox-os-keyboard/
author: Sergi Mansilla
published: '2013-03-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In this article we will take a look at how to approach adding features to a core component in the system such as the input keyboard. It turns out it is pretty easy!

Before we start, take a look at this concept video from Daniel Hooper to get an idea of what we want to implement:

Cool, huh? Making such a change for other mobile platforms would be pretty hard or just plain impossible, but in Firefox OS it is quite simple and it will take us less than 50 lines of code.

## The plan

Conceptually, what we want to achieve is that when the user swipes her finger on the keyboard area, the cursor in the input field moves a distance and direction proportional to the swiping, left or right.

Since a common scenario is that the user might be pressing a wrong key and would like to slide to a close-by key to correct it, we will only start moving the cursor when the swipe distance is longer than the width of a single key.

## Preparing your environment

In order to start hacking Firefox OS itself, you will need a copy of Gaia (the collection of webapps that make up the frontend of Firefox OS) and B2G desktop (a build of the B2G app runtime used on devices where all apps should run as they would on a device).

You can take a look at this [previous article](https://hacks.mozilla.org/2013/01/hacking-gaia-for-firefox-os-part-1/) from Mozilla Hacks in which we guide you through setting up and hacking on Gaia. There is also a complete guide to setting up this environment at [https://wiki.mozilla.org/Gaia/Hacking](https://wiki.mozilla.org/Gaia/Hacking).

Once you get Gaia to run in B2G, you are ready to hack!

## Ready to hack!

Firefox OS is all HTML5, and internally it is composed by several ‘apps’. We can find the main system apps in the `apps`

folder in the gaia repository that you cloned before, including the keyboard app that we will be modifying.

In this post we will be editing only `apps/keyboard/js/keyboard.js`

, which is where

a big chunk of the keyboard logic lives.

We start by initializing some extra variables at the top of the file that will help us keep track of the swiping later.

```
var swipeStartMovePos = null; // Starting point of the swiping
var swipeHappening = false; // Are we in the middle of swiping?
var swipeLastMousex = -1; // Previous mouse position
var swipeMouseTravel = 0; // Amount traveled by the finger so far
var swipeStepWidth = 0; // Width of a single keyboard key
```

Next we should find where the keyboard processes touch events. At

the top of `keyboard.js`

we see that the event handlers for touch events are

declared:

```
var eventHandlers = {
'touchstart': onTouchStart,
'mousedown': onMouseDown,
'mouseup': onMouseUp,
'mousemove': onMouseMove
};
```

Nice! Now we need to store the coordinates of the initial touch event. Both `onTouchStart`

and `onMouseDown`

end up calling the function `startPress`

after they do their respective post-touch tasks, so we will take care of storing the coordinates there.

`startPress`

does some work for when a key is pressed, like highlighting the key or checking whether the user is pressing backspace. We will write our logic after that. A convenient thing is that one of the arguments in its signature is `coords`

, which refers to the coordinates where the user started touching, in the context of the keyboard element. So storing the coordinates is as easy as that:

```
function startPress(target, coords, touchId) {
swipeStartMovePos = { x: coords.pageX, y: coords.pageY };
...
```

In that way we will always have available the coordinates of the last touch even starting point.

The meat of our implementation will happen during the `mousemove`

event, though. We see that the function `onMouseMove`

is just a simple proxy function for the bigger `movePress`

function, where the ‘mouse’ movements are processed. Here is where we will write our cursor-swiping logic.

We will use the width of a keyboard key as our universal measure. Since the width of keyboard keys changes from device to device, we will first have to retrieve it calling a method in `IMERender`

, which is the object that controls how the keyboard is rendered on the screen:

```
swipeStepWidth = swipeStepWidth || IMERender.getKeyWidth();
```

Now we can check if swiping is happening, and whether the swiping is longer than `swipeStepWidth`

. Conveniently enough, our `movePress`

function also gets passed the `coords`

object:

```
if (swipeHappening || (swipeStartMovePos && Math.abs(swipeStartMovePos.x - coords.pageX) > swipeStepWidth)) {
```

Most of our logic will go inside that ‘if’ block. Now that we know that swiping is happening, we have to determine what direction it is going, assigning `1`

for right and `-1`

for left to our previously initialized variable `swipeDirection`

. After that, we add the amount of distance traveled to the variable `swipeMouseTravel`

, and set `swipeLastMousex`

to the current touch coordinates:

```
var swipeDirection = coords.pageX > swipeLastMousex ? 1 : -1;
if (swipeLastMousex > -1) {
swipeMouseTravel += Math.abs(coords.pageX - swipeLastMousex);
}
swipeLastMousex = coords.pageX;
```

Ok, now we have to decide how the pixels travelled by the user’s finger will translate into cursor movement. Let’s make that half the width of a key. That means that for every `swipeStepWidth / 2`

pixels travelled, the cursor in the input field will move one character.

The way we will move the cursor is a bit hacky. What we do is to simulate the pressing of ‘left arrow’ or ‘right arrow’ by the user, even if these keys don’t even exist in the phone’s virtual keyboard. That allows us to move the cursor in the input field. Not ideal, but Mozilla is about to push a new Keyboard IME API that will give the programmer a proper API to manipulate curor positions and selections. For now, we will just workaround it:

```
var stepDistance = swipeStepWidth / 2;
if (swipeMouseTravel > stepDistance) {
var times = Math.floor(swipeMouseTravel / stepDistance);
swipeMouseTravel = 0;
for (var i = 0; i < times; i++)
navigator.mozKeyboard.sendKey(swipeDirection === -1 ? 37 : 39, undefined);
}
```

After that we just need to confirm that swiping is happening and do some cleanup of timeouts and intervals initialized in other areas of the file, that because of our new swiping functionality ouldn't get executed otherwise. We also call `hideAlternatives`

to avoid the keyboard to present us with alternative characters while we are swiping.

```
swipeHappening = true;
clearTimeout(deleteTimeout);
clearInterval(deleteInterval);
clearTimeout(menuTimeout);
hideAlternatives();
return;
```

The only thing left to do is to reset all the values we've set when the user lifts her finger off the screen. The event handler for that is `onMouseUp`

, which calls the function `endPress`

, at the beginning of which we will put our logic:

```
// The user is releasing a key so the key has been pressed. The meat is here.
function endPress(target, coords, touchId) {
swipeStartMovePos = null;
...
if (swipeHappening === true) {
swipeHappening = false;
swipeLastMousex = -1;
return;
}
```

With this last bit, our implementation is complete. Here is a rough video I've made with the working implementation:

You can see the [complete implementation code changes on GitHub](https://github.com/comoyo/gaia/compare/master...swipe_selection).

## Conclusion

Contributing bugfixes or features to Firefox OS is as easy as getting Gaia, B2G and start hacking in HTML5. If you are comfortable programming in JavaScript and familiar with making web pages, you can already contribute to the mobile operating system from Mozilla.

## Appendix: Finding an area to work on

If you already know what bug you want to solve or what feature you want to implement in Firefox OS, first check if it has already been filed in Bugzilla, which is the issue repository that Mozilla uses to keep track of bugs. If it hasn't, feel free to add it. Otherwise, if you are looking for new bugs to fix, a [quick search](https://bugzilla.mozilla.org/buglist.cgi?quicksearch=gaia&list_id=5995257) will reveal many new ones that are sill unassigned. Feel free to pick them up!

## About
[
Sergi Mansilla ](http://sergimansilla.com)

Sergi is lead developer for the Firefox OS team at [Telenor Comoyo](http://www.comoyo.com/no). In the past he's been a developer for Cloud9 IDE, and was responsible for the JavaScript framework that powered the UI of TomTom devices. He is obsessed with programming languages, and he's always juggling with [several projects](http://github.com/sergi) on the side often involving JavaScript, whether it is in the front-end, back-end, or both. Whenever he is not hacking, you'll find him traveling, speaking at some conference or diving in some tropical latitude. Sergi lives currently in Amsterdam.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 14 comments

Tobias FlorekMarch 26th, 2013 at 02:56Robert Nyman [Editor]March 26th, 2013 at 04:12GerbenMarch 26th, 2013 at 04:30Robert Nyman [Editor]March 26th, 2013 at 12:23Robert KaiserMarch 26th, 2013 at 07:44Robert Nyman [Editor]March 26th, 2013 at 12:23hexxMarch 26th, 2013 at 08:52Robert Nyman [Editor]March 26th, 2013 at 12:23Caspy7March 26th, 2013 at 14:05Josh CarpenterMarch 26th, 2013 at 23:44Sergi MansillaMarch 27th, 2013 at 01:45Jared WeinMarch 27th, 2013 at 07:48NikhilMarch 27th, 2013 at 07:58ZiTALApril 4th, 2013 at 14:30