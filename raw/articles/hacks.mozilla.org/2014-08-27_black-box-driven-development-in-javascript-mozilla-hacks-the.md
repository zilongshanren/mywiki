---
title: Black Box Driven Development in JavaScript – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/08/black-box-driven-development-in-javascript/
author: Krasimir Tsonev
published: '2014-08-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Sooner or later every developer finds the beauty of the design patterns. Also, sooner or later the developer finds that most of the patterns are not applicable in their pure format. Very often we use variations. We change the well-known definitions to fit in our use cases. I know that we (the programmers) like [buzzwords](http://en.wikipedia.org/wiki/Buzzword). Here is a new one – Black Box Driven Development or simply BBDD. I started applying the concept before a couple of months, and I could say that the results are promising. After finishing several projects, I started seeing the good practices and formed three principles.

## What is a black box?

Before to go with the principles of the BBDD let’s see what is meant by a black box. According to [Wikipedia](http://en.wikipedia.org/wiki/Black_box):

In science and engineering, a black box is a device, system or object which can be viewed in terms of its input, output and transfer characteristics without any knowledge of its internal workings.


In programming, every piece of code that accepts input, performs actions and returns an output could be considered as a black box. In JavaScript, we could apply the concept easily by using a function. For example:

```
var Box = function(a, b) {
var result = a + b;
return result;
}
```

This is the simplest version of a BBDD unit. It is a box that performs an operation and returns output immediately. However, very often we need something else. We need continuous interaction with the box. This is another kind of box that I use to call *living black box*.

```
var Box = function(a, b) {
var api = {
calculate: function() {
return a + b;
}
};
return api;
}
```

We have an API containing all the public functions of the box. It is identical to the [revealing module pattern](http://addyosmani.com/resources/essentialjsdesignpatterns/book/#revealingmodulepatternjavascript). The most important characteristic of this pattern is that it brings encapsulation. We have a clear separation of the public and private objects.

Now that we know what a black box is, let’s check out the three principles of BBDD.

## Principle 1: Modulize everything

Every piece of logic should exist as an independent module. In other words – a black box. In the beginning of the development cycle it is a little bit difficult to recognize these pieces. Spending too much time in *architecting* the application without having even a line of code may not produce good results. The approach that works involves coding. We should sketch the application and even make part of it. Once we have something we could start thinking about black boxing it. It is also much easier to jump into the code and make something without thinking if it is wrong or right. The key is to refactor the implementation till you feel that it is good enough.

Let’s take the following example:

```
$(document).ready(function() {
if(window.localStorage) {
var products = window.localStorage.getItem('products') || [], content = '';
for(var i=0; i
``` ';
}
$('.content').html(content);
} else {
$('.error').css('display', 'block');
$('.error').html('Error! Local storage is not supported.')
}
});

We are getting an array called `products`

from the local storage of the browser. If the browser does not support local storage, then we show a simple error message.

The code as it is, is fine, and it works. However, there are several responsibilities that are merged into a single function. The first optimization that we have to do is to form a good entry point of our code. Sending just a newly defined closure to the `$(document).ready`

is not flexible. What if we want to delay the execution of our initial code or run it in a different way. The snippet above could be transformed to the following:

```
var App = function() {
var api = {};
api.init = function() {
if(window.localStorage) {
var products = window.localStorage.getItem('products') || [], content = '';
for(var i=0; i
``` ';
}
$('.content').html(content);
} else {
$('.error').css('display', 'block');
$('.error').html('Error! Local storage is not supported.');
}
return api;
}
return api;
}
var application = App();
$(document).ready(application.init);

Now, we have better control over the bootstrapping.

The source of our data at the moment is the local storage of the browser. However, we may need to fetch the products from a database or simply use a [mock-up](http://en.wikipedia.org/wiki/Mockup). It makes sense to extract this part of the code:

```
var Storage = function() {
var api = {};
api.exists = function() {
return !!window && !!window.localStorage;
};
api.get = function() {
return window.localStorage.getItem('products') || [];
}
return api;
}
```

We have two other operations that could form another box – setting HTML content and show an element. Let’s create a module that will handle the DOM interaction.

```
var DOM = function(selector) {
var api = {}, el;
var element = function() {
if(!el) {
el = $(selector);
if(el.length == 0) {
throw new Error('There is no element matching "' + selector + '".');
}
}
return el;
}
api.content = function(html) {
element().html(html);
return api;
}
api.show = function() {
element().css('display', 'block');
return api;
}
return api;
}
```

The code is doing the same thing as in the first version. However, we have a test function `element`

that checks if the passed selector matches anything in the DOM tree. We are also black boxing the jQuery element that makes our code much more flexible. Imagine that we decide to remove jQuery. The DOM operations are hidden in this module. It is worth nothing to edit it and start using vanilla JavaScript for example or some other library. If we stay with the old variant, we will probably go through the whole code base replacing code snippets.

Here is the transformed script. A new version that uses the modules that we’ve created above:

```
var App = function() {
var api = {},
storage = Storage(),
c = DOM('.content'),
e = DOM('.error');
api.init = function() {
if(storage.exists()) {
var products = storage.get(), content = '';
for(var i=0; i
``` ';
}
c.content(content);
} else {
e.content('Error! Local storage is not supported.').show();
}
return api;
}
return api;
}

Notice that we have separation of responsibilities. We have objects that play roles. It is easier and much more interesting to work with such codebase.

## Principle 2: Expose only public methods

What makes the black box valuable is the fact that it hides the complexity. The programmer should expose only methods (or properties) that are needed. All the other functions that are used for internal processes should be private.

Let’s get the DOM module above:

```
var DOM = function(selector) {
var api = {}, el;
var element = function() { … }
api.content = function(html) { … }
api.show = function() { … }
return api;
}
```

When a developer uses our class, he is interested in two things – changing the content and showing a DOM element. He should not think about validations or change CSS properties. In our example, there are private variable `el`

and private function `element`

. They are hidden from the outside world.

## Principle 3: Use composition over inheritance

One of the popular ways to inherit classes in JavaScript uses the prototype chain. In the following snippet, we have class A that is inherited by class C:

```
function A(){};
A.prototype.someMethod = function(){};
function C(){};
C.prototype = new A();
C.prototype.constructor = C;
```

However, if we use the revealing module pattern, it makes sense to use composition. It is because we are dealing with objects and not functions (* in fact the functions in JavaScript are also objects). Let’s say that we have a box that implements the observer pattern, and we want to extend it.

```
var Observer = function() {
var api = {}, listeners = {};
api.on = function(event, handler) { … };
api.off = function(event, handler) { … };
api.dispatch = function(event) { … };
return api;
}
var Logic = function() {
var api = Observer();
api.customMethod = function() { … };
return api;
}
```

We get the required functionality by assigning an initial value to the `api`

variable. We should notice that every class that uses this technique receives a brand new observer object so there is no way to produce collisions.

## Summary

Black box driven development is a nice way to architect your applications. It provides encapsulation and flexibility. BBDD comes with a simple module definition that helps organizing big projects (and teams). I saw how several developers worked on the same project, and they all built their black boxes independently.

## About Krasimir Tsonev

Krasimir Tsonev is a front-end developer, blogger and speaker. He loves writing JavaScript and experimenting with the latest CSS and HTML features. Author of the "Node.js blueprints" book he is focused on delivering cutting edge applications. Krasimir started his career as graphic designer, he spent several years coding in ActionScript3. Right now, with the rise of the mobile development, he is enthusiastic to work on responsive applications targeted to various devices. Living and working in Bulgaria he graduated at the Technical University of Varna with bachelor and master degree in computer science.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 35 comments

mAugust 27th, 2014 at 06:27Krasimir TsonevAugust 27th, 2014 at 07:35Adam FreidinAugust 27th, 2014 at 07:46Krasimir TsonevAugust 27th, 2014 at 08:33Robert Nyman [Editor]August 27th, 2014 at 08:37LukeAugust 27th, 2014 at 20:27Pavel IvanovAugust 27th, 2014 at 06:31Norman KabirAugust 27th, 2014 at 06:33Robert Nyman [Editor]August 27th, 2014 at 06:50Felix HammerlAugust 27th, 2014 at 06:44Krasimir TsonevAugust 27th, 2014 at 09:02Ted k’August 27th, 2014 at 06:55Erick MendozaAugust 27th, 2014 at 07:36Krasimir TsonevAugust 27th, 2014 at 08:35DaveAugust 27th, 2014 at 07:48Krasimir TsonevAugust 27th, 2014 at 08:40Marcos RodriguesAugust 27th, 2014 at 08:24Krasimir TsonevAugust 27th, 2014 at 08:58Marcos RodriguesAugust 27th, 2014 at 09:37Krasimir TsonevAugust 27th, 2014 at 14:10ReneAugust 27th, 2014 at 08:57azendalAugust 27th, 2014 at 09:49AutomateAllTheThingsAugust 27th, 2014 at 18:54Krasimir TsonevAugust 28th, 2014 at 03:49PulakAugust 27th, 2014 at 19:34Krasimir TsonevAugust 28th, 2014 at 03:52David HansonAugust 27th, 2014 at 22:17Krasimir TsonevAugust 28th, 2014 at 03:55David HansonAugust 28th, 2014 at 05:48TedvGAugust 27th, 2014 at 23:57Krasimir TsonevAugust 28th, 2014 at 03:56Matt PerdeckAugust 28th, 2014 at 03:14Krasimir TsonevAugust 28th, 2014 at 06:38AcazAugust 28th, 2014 at 09:43LoopsSeptember 4th, 2014 at 01:08