---
title: A call for quality HTML5 demo markup – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/12/a-call-for-quality-html5-demo-markup/
author: Janet Swisher
published: '2010-12-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 is a necessary evolution to make the web better. Before the HTML5 specs were created we used (and still use) a hacked together bunch of systems meant for describing and linking documents to create applications. We use generic elements to simulate rich interaction modules used in desktop development and we make assumptions as to what the user agent (browser) can do for the end user.

The good thing about this mess is that it taught us over the last few years to be paranoid in our development approach – we realised that in order to deliver working, accessible, maintainable and scalable systems we have to be professional and intelligent in our decisions and especially in our planning and architecting.

The trouble is that with the excitement around the cool new HTML5 things to play with a lot of these principles get lost and discarded as outdated. They aren’t – part of the mess that the web is in is that in 1999 a lot of people discarded everything else and instead worked only on the new hotness that was Internet Explorer 6 and DHTML. Let’s not repeat that mistake.

## The two faces of HTML5 enthusiasm

Right now there are two things to get really excited about in HTML5: the richer, more meaningful semantics of new elements and the APIs that give us deep access into the workings of the browser and the operating system. The former allows us to build much richer interfaces and the latter allows us to build much more complex applications.

All of this comes with the awesome of view source (or check in development tools) for debugging. You can advocate HTML5 by writing clean and useful markup. You can kill it by treating the markup as a second class citizen which is only there to serve the script.

The markup enthusiasts are very happy about HTML5 and make it easy for people to upgrade – lots of cool new [blog templates](http://nicolasgallagher.com/anatomy-of-an-html5-wordpress-theme/) and [boilerplate HTML templates](http://html5boilerplate.com/) are being built and [polyfills](http://github.com/Modernizr/Modernizr/wiki/HTML5-Cross-browser-Polyfills) created to allow using the new features and not leave behind outdated browsers.

On the app development side of things it looks much different and that is just sad. My only possible explanation is that people who come from desktop environments now tackle the HTML5 APIs without ever having to care about markup. The pragmatism of HTML5 allows a much more forgiving syntax than XHTML but it shouldn’t mean that we can just re-apply all the bad mistakes that held us back when it comes to maintenance for years.

During my career as a web developer I realised a few things make a lot of sense when building web apps:

**If there is an element for a certain task – use that one**. It is very likely that the element comes with accessibility and interaction features for free that you would otherwise have to simulate.**Separate CSS, JavaScript and HTML**– which means it is easy to refactor your code without having to change all of them. It also means you can work in parallel with others instead of breaking each other’s code**Never rely on markup or content**– as sooner or later some editing tool will come into place that messes with everything you created

This means a lot of things:

- For starters it means that inline styles are simply evil as they override any settings you have in your style sheets. Only use them when this is exactly what you need to do or when you calculate them dynamically.
- The same applies to inline scripting. If you have an
`onclick="foo()"`

somewhere in your HTML and`foo()`

changes to`bar()`

you have to rename it in every HTML document (of course nowadays it is one template, but it still means hunting down a reference you might miss) - If instead of using a native HTML element for a certain job you use SPANs and DIVs you’ll have to add classes to make them look and work – and simulate the keyboard accessibility, too.
- You can’t rely on the text value of any element. A
`<button>edit</button>`

using the “edit” as the trigger for certain functionality would have to have the JS localised, too when you create the German`<button>bearbeiten</button>.`


## Bla bla bla… C’mon Chris, it isn’t that bad!

The above best practices have been mentioned for years and a lot of people get sick of seeing them repeated. After all, this is intelligent development and standard practice in backend technologies. I came across a lot of “creative” uses lately though when doing a view-source on HTML5 demos – specifically the ones in the HTML5 advent calendar. And here is my yield of what people do.

## Simulating a navigation list

One of the first things I encountered was a painting tool that had a gallery of created graphics as a background. Now, to me this would be a simple list:

The markup I found though was this:

```
```


[...]

This, of course is generated by the backend. My first gripe is the dropshadow image, after all this is an HTML5 showcase – just use CSS3. We also have the three instances of generated styles and double classes. Granted, an extra class gives you a handle to all images instead of tiles, so why not. But as there is no real link around the image, the click handler has to read the url from somewhere. There is a lot of unnecessary back and forth between DOM and scripting here which does slow down the whole demo. Seeing that this is also the main navigation from the entry page to the editor this could be a list inside a [ nav](http://www.w3.org/TR/html5/sections.html#the-nav-element) element. A list groups these items together, a bunch of DIVs doesn’t (screen readers for example tell you how many items there are in a list).

Another list I found was supposed to be links to refresh the app and have a hierarchy but instead was a flat list with classes to define hierarchy and group:

- Simple
- {name} [... repeated ...]
- {parent name}
- {name} [... repeated ...]

This could be OK, granted you also shift keyboard focus, but why not:

This would give you styling hooks and functionality for free. Links and buttons are great to trigger functionality – but it seems that is too easy.

## Click (probably) here for functionality

If I build a button for an application to trigger a certain functionality this is the markup:

[Buttons](http://www.w3.org/TR/html5/the-button-element.html#the-button-element) are what trigger functionality – both a backend script or a JavaScript. They are keyboard accessible, have a disabled state and sensible out-of-the-box styling that nowadays can be completely overwritten. The class can be the definition of what the button should do – instead of the text which will change. You could use an ID but a class allows to repeat buttons (for example on the top and the bottom of a results list).

The buttons I found though were slightly different:

```
```Start Drawing

View the Mural

{title}

Draw

View

Help





So instead of using a nested list with classes for each button and the hierarchy in the nesting we have a lot of classes and a hand-rolled DIV construct. Instead of making buttons really disabled we rely on opacity and there is quite a mix of inline images and background images (if all were background images, they could be one sprite!). Keyboard navigation will have to be written for this and if you were to add a button you’d have to come up with another ID.

HTML5 actually has a construct for this. There is a [ menu](http://www.w3.org/TR/html5/interactive-elements.html#menus) element with

[command](http://www.w3.org/TR/html5/interactive-elements.html#the-command)child elements. These are in use in Chrome’s side bar for example and should be what we use. If you want to make it work for everyone, a nested list with

`button`

elements is what to go for.The overly complex DIV construct is quite used though – this was another example:

```
Start Game
Help
High Scores
```

When in doubt – add an ID and class to everything.

Other buttons I encountered were actually links pointing to `javascript://`

using an inline style to indicate hierarchy:

Talking of inline – here’s a great example of a tool generating a lot of code that could be replaced by a single event handler and [event delegation](http://icant.co.uk/sandbox/eventdelegation/):

```
[...repeated 20 times...]
```

Notice that if the images for the button couldn’t be loaded for one reason or another (or you can’t see them at all) this application is very confusing indeed – no alternative text for the images and no text content to fall back to. I am also very much sure that the in and out handlers trigger visual effects CSS could handle better.

## Reasons and effects

I know there are probably good reasons for all of this, and I am sure I will also do things wrongly when I am rushed or want to get things out quickly. What we have to understand though is that right now we have a responsibility to show the best of breed demos we can.

We cannot preach the open web and technologies and view-source over closed systems and at the same time forget the things we learnt in the last decade. Some of these things I found look like code Frontpage or Dreamweaver could have produced in the 90ies and resulted in a lot of badly performing, hard to maintain products that either still annoy people who have to use them or get replaced every 2 years.

We have a mandate to educate the new developers coming to the web. Unlearning something is much harder than learning it – so let’s not start with bloat and quick fixes that work but forget to advocate clean code and thinking about the impact your product has on the end users (thinking accessibility) and the poor sods that will have to maintain your product when you are gone. We are not here to advocate effects and products, we are here to promote the tools that allow anyone to easily build something cool that is also easy to understand.

HTML5 is about evolving the web as a platform – we also need to evolve with it and take more responsibility. We have app and we have markup enthusiasts. Let’s make them work together to build things that are great functionality and clean semantics.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 10 comments

alexander farkasDecember 19th, 2010 at 14:28MardegDecember 19th, 2010 at 18:16Nick FitzsimonsDecember 19th, 2010 at 20:37Ankit SainiDecember 23rd, 2010 at 08:22Jack LukicDecember 19th, 2010 at 23:25SteveDecember 23rd, 2010 at 09:34Harp BDecember 25th, 2010 at 03:09Felix PleșoianuJanuary 1st, 2011 at 11:00brianJanuary 3rd, 2011 at 00:05icflyoncyberSeptember 20th, 2011 at 12:55