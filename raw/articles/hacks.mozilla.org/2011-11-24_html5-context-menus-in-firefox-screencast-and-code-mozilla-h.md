---
title: HTML5 context menus in Firefox (Screencast and Code) – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2011/11/html5-context-menus-in-firefox-screencast-and-code/
author: Chris Heilmann
published: '2011-11-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

You may not know it, but the HTML5 specifications go beyond what we put in the pages and also define how parts of the browser should become available to developers with HTML, CSS and JavaScript. One of these parts of the specs are [context menus](http://www.whatwg.org/specs/web-apps/current-work/multipage/interactive-elements.html#context-menus), or “right click menus”. Using HTML5 and a menu element you can add new options to these without having to write a browser add-on. In Firefox 8 (the current one) we have support for those. See the following screencast for a [context menu demo](http://thewebrocks.com/demos/context-menu).

The image example is pretty simple and was actually written by Paul Rouget as a demo [in the original Firefox bug request](https://bugzilla.mozilla.org/show_bug.cgi?id=617528). The main core is the HTML of it:

```
```


As you can see you link the `menu`

element to an element via its ID. The `contextmenu`

attribute then points to this one. Each menu can have several `menuitems`

. Each of those gets a textual label and a possible icon. You can also nest `menu`

elements to create multiple layer menus. Here, we add inline

![a context menu image with a context menu](../../assets/e37d61bb4a4c16c9.png)


The functionality is simple, all the `rotate()`

and `resize()`

functions do is add class names to the image using `querySelector`

and `classList`

:

```
function rotate() {
document.querySelector('#menudemo').classList.toggle('rotate');
}
function resize() {
document.querySelector('#menudemo').classList.toggle('resize');
}
```

The real effect is in CSS transforms and transitions. As the image has an ID of `menudemo`

here is what is needed in CSS to rotate and resize:

```
#menudemo {
-moz-transition: 0.2s;
width:200px;
}
#menudemo.rotate {
-moz-transform: rotate(90deg);
}
#menudemo.resize {
-moz-transform: scale(0.7);
}
#menudemo.resize.rotate {
-moz-transform: scale(0.7) rotate(90deg);
}
```

Notice that in a real product we should of course add the other browser prefixes and go prefix-less but as the functionality now only works in Firefox, this is enough for this demo.

## Detecting support and visual hinting

Now, as this is extending the normal user offerings in the browser we need to make it obvious that there is a right-click menu available. In CSS3, there is a `context-menu`

cursor available to us. When context menus are available, this should be shown:

```
.contextmenu #menudemo, .contextmenu .demo {
cursor: context-menu;
}
```

We test the browser for support by checking for contextmenu on the body element and for `HTMLMenuItemElement`

in the window (this has been added as a pull request to [Modernizr](https://github.com/Modernizr/Modernizr), too).

```
if ('contextMenu' in document.body && 'HTMLMenuItemElement' in window) {
document.documentElement.classList.add('contextmenu');
} else {
return;
}
```

Wouldn’t `HTMLMenuItemElement`

be enough? Yes, but a real context menu should only offer functionality when it is sensible, and that is where `contextMenu`

comes in.

## Turning menuitems on and off depending on functionality

As a slightly more complex example, let’s add a “count words” functionality to the document. For this, we generate a counter element that will become a tooltip when the words were counted:

```
var counter = document.createElement('span');
counter.id = 'counter';
counter.className = 'hide';
document.body.appendChild(counter);
counter.addEventListener('click', function(ev){
this.className = 'hide';
},false);
```

This one is hidden by default and becomes visible when the `hide`

class is removed. To make it smooth, we use a transition:

```
#counter{
position: absolute;
background: rgba(0,0,0,0.7);
padding:.5em 1em;
color: #fff;
font-weight:bold;
border-radius: 5px;
-moz-transition: opacity 0.4s;
}
#counter.hide{
opacity: 0;
}
```

We start with two sections with context menus:

```
```

We then loop through all the `menuitems`

with the class `wordcount`

and apply the functionality.

```
var wordcountmenus = document.querySelectorAll('.wordcount'),
i = wordcountmenus.length;
while (i--) {
wordcountmenus[i].addEventListener('click', function(ev){
// add functionality
}, false);
}
```

We need to find out what has been selected in the page. We do this by using `getSelection()`

and splitting its string version at whitespace. We then show the counter by removing the `hide`

class name.

```
var wordcountmenus = document.querySelectorAll('.wordcount'),
i = wordcountmenus.length;
while (i--) {
wordcountmenus[i].addEventListener('click', function(ev){
var text = document.getSelection(),
count = text.toString().split(/s/).length;
counter.innerHTML = count + ' words';
counter.className = '';
}, false);
}
```

You can see this in action in the second [context menu demo](http://thewebrocks.com/demos/context-menu). Now, the issue with this (as explained in the screencast) is that it always counts the words, regardless of the user having selected some text. What we want is the menu only to be active when there is text selected.

![interactive menu item context menu item available or not available depending on selection](../../assets/5694c6c9a2eb4ab5.png)


So in order to make our menu only become available when it makes sense we check if there is a selection in the document. Every context menu fires an event called `contextmenu`

when it opens. So all we need to do is to subscribe to this event.

When something is selected in the document `document.getSelection().isCollapsed`

is true. Otherwise it is false, so all we need to do is to enable or disable the menu item accordingly:

```
document.querySelector('#interactive').addEventListener(
'contextmenu', function(ev) {
this.querySelector('.wordcount').disabled =
document.getSelection().isCollapsed;
},
false);
```

The last thing to solve is the position of the mouse to position the counter element. As the menu selection event doesn’t give us the mouse position we need to add a `contextmenu`

handler to the whole document that positions the counter invisibly behind the menu when it is opened:

```
document.body.addEventListener(
'contextmenu', function(ev) {
counter.style.left = ev.pageX + 'px';
counter.style.top = ev.pageY + 'px';
counter.className = 'hide';
},
false);
```

## Further reading and resources

[The full code demo](http://thewebrocks.com/demos/context-menu)[The Firefox bug request with lots of discussion](https://bugzilla.mozilla.org/show_bug.cgi?id=617528)[Context Menus on the WHATWG](http://www.whatwg.org/specs/web-apps/current-work/multipage/interactive-elements.html#context-menus)[A longer discussion on Google+ about context menus](https://plus.google.com/115133653231679625609/posts/CJMyExJTbug)[A jQuery Polyfill for contextmenu](http://medialize.github.com/jQuery-contextMenu/demo/html5-polyfill-firefox8.html)

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 19 comments

Mårten BjörkNovember 24th, 2011 at 03:09fpiatNovember 24th, 2011 at 03:20fpiatNovember 24th, 2011 at 03:22passcodNovember 24th, 2011 at 04:26Chris HeilmannNovember 24th, 2011 at 06:51RonnyNovember 24th, 2011 at 09:48Jonas Finnemann JensenNovember 24th, 2011 at 11:07Jonas Finnemann JensenNovember 24th, 2011 at 11:19dhineshSeptember 12th, 2012 at 03:26Rodney RehmNovember 24th, 2011 at 05:57Chris HeilmannNovember 24th, 2011 at 06:49Rodney RehmNovember 24th, 2011 at 06:59Rodney RehmNovember 25th, 2011 at 09:15Luke DornyNovember 24th, 2011 at 10:37Daniel PiechnickNovember 25th, 2011 at 00:22kangaxNovember 26th, 2011 at 17:03IsuruJanuary 11th, 2012 at 20:07icaaqMarch 19th, 2012 at 06:16pedzMay 25th, 2012 at 06:10