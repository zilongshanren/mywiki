---
title: Old tricks for new browsers – a talk at jQuery UK 2012 – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2012/02/old-tricks-for-new-browsers-a-talk-at-jquery-uk-2012/
author: Chris Heilmann
published: '2012-02-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last Friday around 300 developers went to Oxford, England to attend jQuery UK and learn about all that is hot and new about their favourite JavaScript library. Imagine their surprise when I went on stage to tell them that a lot of what jQuery is used for these days doesn’t need it. If you want to learn more about the talk itself, there is a [detailed report, slides and the audio recording](http://christianheilmann.com/2012/02/11/jquery-uk-conference-in-oxford-england-slides-audio-impressions-and-notes/) available.

The point I was making is that libraries like jQuery were first and foremost there to give us a level playing field as developers. We should not have to know the quirks of every browser and this is where using a library allows us to concentrate on the task at hand and not on how it will fail in 10 year old browsers.

jQuery’s revolutionary new way of looking at web design was based on two main things: accessing the document via CSS selectors rather than the unwieldy DOM methods and chaining of JavaScript commands. jQuery then continued to make event handling and Ajax interactions easier and implemented the [Easing equations](http://www.robertpenner.com/easing/) to allow for slick and beautiful animations.

However, this simplicity came with a prize: developers seem to forget a few very simple techniques that allow you to write very terse and simple to understand JavaScripts that don’t rely on jQuery. Amongst others, the most powerful ones are event delegation and assigning classes to parent elements and leave the main work to CSS.

## Event delegation

[Event Delegation](http://icant.co.uk/sandbox/eventdelegation/) means that instead of applying an event handler to each of the child elements in an element, you assign one handler to the parent element and let the browser do the rest for you. Events bubble up the DOM of a document and happen on the element you want to get and each of its parent elements. That way all you have to do is to compare with the target of the event to get the one you want to access. Say you have a to-do list in your document. All the HTML you need is:

```
```

- Go round Mum's
- Get Liz back
- Sort life out!

In order to add event handlers to these list items, in jQuery beginners are tempted to do a `$('#todo li').click(function(ev){...});`

or – even worse – add a class to each list item and then access these. If you use event delegation all you need in JavaScript is:

```
document.querySelector('#todo').addEventListener( 'click',
function( ev ) {
var t = ev.target;
if ( t.tagName === 'LI' ) {
alert( t + t.innerHTML );
ev.preventDefault();
}
}, false);
```

Newer browsers have a `querySelector`

and `querySelectorAll`

method (see [support here](http://caniuse.com/#search=queryselector)) that gives you access to DOM elements via CSS selectors – something we learned from jQuery. We use this here to access the to-do list. Then we apply an event listener for `click`

to the list.

We read out which element has been clicked with `ev.target`

and compare its `tagName`

to `LI`

(this property is always uppercase). This means we will never execute the rest of the code when the user for example clicks on the list itself. We call `preventDefault()`

to tell the browser not to do anything – we now take over.

You can try this out [in this fiddle or embedded below:](http://jsfiddle.net/codepo8/4UjCY/)

The benefits of event delegation is that you can now add new items without having to ever re-assign handlers. As the main click handler is on the list new items automatically will be added to the functionality. Try it out [in this fiddle](http://jsfiddle.net/codepo8/4UjCY/1/) or embedded below:

## Leaving styling and DOM traversal to CSS

Another big use case of jQuery is to access a lot of elements at once and change their styling by manipulating their `styles`

collection with the jQuery `css()`

method. This is seemingly handy but is also annoying as you put styling information in your JavaScript. What if there is a rebranding later on? Where do people find the colours to change? It is a much simpler to add a class to the element in question and leave the rest to CSS. If you think about it, a lot of times we repeat the same CSS selectors in jQuery and the style document. Seems redundant.

Adding and removing classes in the past was a bit of a nightmare. The way to do it was using the `className`

property of a DOM element which contained a string. It was then up to you to find if a certain class name is in that string and to remove and add classes by adding to or using `replace()`

on the string. Again, browsers learned from jQuery and now have a [classList](https://developer.mozilla.org/en/DOM/element.classList) object ([support here](http://caniuse.com/#search=classlist)) that allows easy manipulation of CSS classes applied to elements. You have `add()`

, `remove()`

, `toggle()`

and `contains()`

to play with.

This makes it dead easy to style a lot of elements and to single them out for different styling. Let’s say for example we have a content area and want to show one at a time. It is tempting to loop over the elements and do a lot of comparison, but all we really need is to assign classes and leave the rest to CSS. Say our content is a navigation pointing to articles. This works in all browsers:

```
```
Make sure Tweek doesn't expect anything, then steal underwear
and bring it to the mine.

WIP

Yes, profit will come. Let's sing the underpants gnome song.


Now in order to hide all the articles, all we do is assign a ‘js’ class to the body of the document and store the first link and first article in the content section in variables. We assign a class called ‘current’ to each of those.

```
/* grab all the elements we need */
var nav = document.querySelector( '#nav' ),
content = document.querySelector( '#content' ),
/* grab the first article and the first link */
article = document.querySelector( '#content article' ),
link = document.querySelector( '#nav a' );
/* hide everything by applying a class called 'js' to the body */
document.body.classList.add( 'js' );
/* show the current article and link */
article.classList.add( 'current' );
link.classList.add( 'current' );
```

Together with a simple CSS, this hides them all off screen:

```
/* change content to be a content panel */
.js #content {
position: relative;
overflow: hidden;
min-height: 300px;
}
/* push all the articles up */
.js #content article {
position: absolute;
top: -700px;
left: 250px;
}
/* hide 'back to top' links */
.js article footer {
position: absolute;
left: -20000px;
}
```

In this case we move the articles up. We also hide the “back to top” links as they are redundant when we hide and show the articles. To show and hide the articles all we need to do is assign a class called “current” to the one we want to show that overrides the original styling. In this case we move the article down again.

```
/* keep the current article visible */
.js #content article.current {
top: 0;
}
```

In order to achieve that all we need to do is a simple event delegation on the navigation:

```
/* event delegation for the navigation */
nav.addEventListener( 'click', function( ev ) {
var t = ev.target;
if ( t.tagName === 'A' ) {
/* remove old styles */
link.classList.remove( 'current' );
article.classList.remove( 'current' );
/* get the new active link and article */
link = t;
article = document.querySelector( link.getAttribute( 'href' ) );
/* show them by assigning the current class */
link.classList.add( 'current' );
article.classList.add( 'current' );
}
}, false);
```

The simplicity here lies in the fact that the links already point to the elements with this IDs on them. So all we need to do is to read the `href`

attribute of the link that was clicked.

See the final result [in this fiddle](http://jsfiddle.net/codepo8/PmkKF/1/) or embedded below.

## Keeping the visuals in the CSS

Mixed with [CSS transitions](https://developer.mozilla.org/en/css/css_transitions) or animations ([support here](http://caniuse.com/#search=transition)), this can be made much smoother in a very simple way:

```
.js #content article {
position: absolute;
top: -300px;
left: 250px;
-moz-transition: 1s;
-webkit-transition: 1s;
-ms-transition: 1s;
-o-transition: 1s;
transition: 1s;
}
```

The transition now simply goes smoothly in one second from the state without the ‘current’ class to the one with it. In our case, moving the article down. You can add more properties by editing the CSS – no need for more JavaScript. See the result [in this fiddle](http://jsfiddle.net/codepo8/PmkKF/2/) or embedded below:

As we also toggle the current class on the link we can do more. It is simple to add visual extras like a “you are here” state by using CSS generated content with the `:after`

selector ([support here](http://caniuse.com/#search=after)). That way you can add visual nice-to-haves without needing the generate HTML in JavaScript or resort to images.

```
.js #nav a:hover:after, .js #nav a:focus:after, .js #nav a.current:after {
content: '➭';
position: absolute;
right: 5px;
}
```

See the final result [in this fiddle](http://jsfiddle.net/codepo8/PmkKF/3/) or embedded below:

The benefit of this technique is that we keep all the look and feel in CSS and make it much easier to maintain. And by using CSS transitions and animations you also leverage hardware acceleration.

## Give them a go, please?

All of these things work across browsers we use these days and using polyfills can be made to work in old browsers, too. However, not everything is needed to be applied to old browsers. As web developers we should look ahead and not cater for outdated technology. If the things I showed above fall back to server-side solutions or page reloads in IE6, nobody is going to be the wiser. Let’s build escalator solutions – smooth when the tech works but still available as stairs when it doesn’t.

## Translations

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 30 comments

Vladimir CarrerFebruary 13th, 2012 at 08:52DraeliFebruary 13th, 2012 at 09:25MustafaFebruary 13th, 2012 at 09:31ChrisFebruary 13th, 2012 at 11:56MustafaFebruary 13th, 2012 at 12:40SimonFebruary 13th, 2012 at 15:42MustafaFebruary 14th, 2012 at 02:23BuzuFebruary 14th, 2012 at 10:36Mohamed JamaFebruary 13th, 2012 at 16:06Chris HeilmannFebruary 15th, 2012 at 04:09DrewFebruary 13th, 2012 at 17:08BuzuFebruary 14th, 2012 at 10:38Chris HeilmannFebruary 15th, 2012 at 04:08Neil RashbrookFebruary 14th, 2012 at 04:51Chris HeilmannFebruary 15th, 2012 at 04:07JimFebruary 14th, 2012 at 08:15Chris HeilmannFebruary 15th, 2012 at 04:05thinsoldierFebruary 16th, 2012 at 09:09pdFebruary 15th, 2012 at 02:45Chris HeilmannFebruary 15th, 2012 at 04:01pdFebruary 15th, 2012 at 06:02Chris HeilmannFebruary 15th, 2012 at 07:04Kevin DangoorFebruary 15th, 2012 at 07:08Marcus TuckerFebruary 15th, 2012 at 06:13Marcus TuckerFebruary 15th, 2012 at 06:20Chris HeilmannFebruary 15th, 2012 at 06:25Marcus TuckerFebruary 15th, 2012 at 06:55Hannes HirzelFebruary 20th, 2012 at 01:46BillyMarch 23rd, 2012 at 18:38Abolfazl BeigiSeptember 6th, 2012 at 13:51