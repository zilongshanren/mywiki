---
title: 'ES6 In Depth: Classes – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/07/es6-in-depth-classes/
author: Eric Faust
published: '2015-07-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) is a series on new features being added to the JavaScript programming language in the 6th Edition of the ECMAScript standard, ES6 for short.

Today, we get a bit of a respite from the complexity that we’ve seen in previous posts in this series. There are no new never-before-seen ways of [writing code with Generators](https://hacks.mozilla.org/2015/07/es6-in-depth-generators-continued/); no [all-powerful Proxy objects](https://hacks.mozilla.org/2015/07/es6-in-depth-proxies-and-reflect/) which provide hooks into the inner algorithmic workings of the JavaScript language; no new data structures that obviate the need for roll-your-own solutions. Instead, we get to talk about syntactic and idiomatic cleanups for an old problem: object constructor creation in JavaScript.

### The Problem

Say we want to create the most quintessential example of object-oriented design principles: the Circle class. Imagine we are writing a Circle for a simple Canvas library. Among other things, we might want to know how to do the following:

- Draw a given Circle to a given Canvas.
- Keep track of the total number of Circles ever made.
- Keep track of the radius of a given Circle, and how to enforce
[invariants](https://en.wikipedia.org/wiki/Invariant_%28computer_science%29)on its value. - Calculate the area of a given Circle.

Current JS idioms say that we should first create the constructor as a function, then add any properties we might want to the function itself, then replace the `prototype`

property of that constructor with an object. This `prototype`

object will contain all of the properties that instance objects created by our constructor should start with. For even a simple example, by the time you get it all typed out, this ends up being a lot of boilerplate:

`<pre>`


function Circle(radius) {

this.radius = radius;

Circle.circlesMade++;

}

Circle.draw = function draw(circle, canvas) { /* Canvas drawing code */ }

Object.defineProperty(Circle, "circlesMade", {

get: function() {

return !this._count ? 0 : this._count;

},

set: function(val) {

this._count = val;

}

});

Circle.prototype = {

area: function area() {

return Math.pow(this.radius, 2) * Math.PI;

}

};

Object.defineProperty(Circle.prototype, "radius", {

get: function() {

return this._radius;

},

set: function(radius) {

if (!Number.isInteger(radius))

throw new Error("Circle radius must be an integer.");

this._radius = radius;

}

});

</pre>

Not only is the code cumbersome, it’s also far from intuitive. It requires having a non-trivial understanding of the way functions work, and how various installed properties make their way onto created instance objects. If this approach seems complicated, don’t worry. The whole point of this post is to show off a much simpler way of writing code that does all of this.

### Method Definition Syntax

In a first attempt to clean this up, ES6 offered a new syntax for adding special properties to an object. While it was easy to add the `area`

method to `Circle.prototype`

above, it felt much heavier to add the getter/setter pair for `radius`

. As JS moved towards a more object-oriented approach, people became interested in designing cleaner ways to add accessors to objects. We needed a new way of adding “methods” to an object exactly as if they had been added with `obj.prop = method`

, without the weight of `Object.defineProperty`

. People wanted to be able to do the following things easily:

- Add normal function properties to an object.
- Add generator function properties to an object.
- Add normal accessor function properties to an object.
- Add any of the above as if you had done it with
`[]`

syntax on the finished object. We’ll call these*Computed property names*.

Some of these things couldn’t be done before. For example, there is no way to define a getter or setter with assignments to `obj.prop`

. Accordingly, new syntax had to be added. You can now write code that looks like this:

`<pre>`


var obj = {

// Methods are now added without a function keyword, using the name of the

// property as the name of the function.

method(args) { ... },

// To make a method that's a generator instead, just add a '*', as normal.

*genMethod(args) { ... },

// Accessors can now go inline, with the help of |get| and |set|. You can

// just define the functions inline. No generators, though.

// Note that a getter installed this way must have no arguments

get propName() { ... },

// Note that a setter installed this way must have exactly one argument

set propName(arg) { ... },

// To handle case (4) above, [] syntax is now allowed anywhere a name would

// have gone! This can use symbols, call functions, concatenate strings, or

// any other expression that evaluates to a property id. Though I've shown

// it here as a method, this syntax also works for accessors or generators.

[functionThatReturnsPropertyName()] (args) { ... }

};

</pre>

Using this new syntax, we can now rewrite our snippet above:

`<pre>`


function Circle(radius) {

this.radius = radius;

Circle.circlesMade++;

}

Circle.draw = function draw(circle, canvas) { /* Canvas drawing code */ }

Object.defineProperty(Circle, "circlesMade", {

get: function() {

return !this._count ? 0 : this._count;

},

set: function(val) {

this._count = val;

}

});

Circle.prototype = {

area() {

return Math.pow(this.radius, 2) * Math.PI;

},

get radius() {

return this._radius;

},

set radius(radius) {

if (!Number.isInteger(radius))

throw new Error("Circle radius must be an integer.");

this._radius = radius;

}

};

</pre>

Pedantically, this code isn’t exactly identical to the snippet above. Method definitions in object literals are installed as configurable and enumerable, while the accessors installed in the first snippet will be non-configurable and non-enumerable. In practice, this is rarely noticed, and I decided to elide enumerability and configurability above for brevity.

Still, it’s getting better, right? Unfortunately, even armed with this new method definition syntax, there’s not much we can do for the definition of `Circle`

, as we have yet to define the function. There’s no way to get properties onto a function as you’re defining it.

### Class Definition Syntax

Though this was better, it still didn’t satisfy people who wanted a cleaner solution to object-oriented design in JavaScript. Other languages have a construct for handling object-oriented design, they argued, and that construct is called a *class*.

Fair enough. Let’s add classes, then.

We want a system that will allow us to add methods to a named constructor, and add methods to its `.prototype`

as well, so that they will appear on constructed instances of the class. Since we have our fancy new method definition syntax, we should definitely use it. Then, we only need a way to differentiate between what is generalized over all instances of the class, and what functions are specific to a given instance. In C++ or Java, the keyword for that is `static`

. Seems as good as any. Let’s use it.

Now it would be useful to have a way to designate one of the methods of the bunch to be the function that gets called as the constructor. In C++ or Java, that would be named the same as the class, with no return type. Since JS doesn’t have return types, and we need a `.constructor`

property anyway, for backwards compatibility, let’s call that method `constructor`

.

Putting it together, we can rewrite our Circle class as it was always meant to be:

`<pre>`


class Circle {

constructor(radius) {

this.radius = radius;

Circle.circlesMade++;

};

static draw(circle, canvas) {

// Canvas drawing code

};

static get circlesMade() {

return !this._count ? 0 : this._count;

};

static set circlesMade(val) {

this._count = val;

};

area() {

return Math.pow(this.radius, 2) * Math.PI;

};

get radius() {

return this._radius;

};

set radius(radius) {

if (!Number.isInteger(radius))

throw new Error("Circle radius must be an integer.");

this._radius = radius;

};

}

</pre>

Wow! Not only can we group everything related to a `Circle`

together, but everything looks so… clean. This is definitely better than what we started with.

Even so, some of you are likely to have questions or to find edge cases. I’ll try to anticipate and address some of these below:

-
**What’s with the semicolons?**– In an attempt to “make things look more like traditional classes,” we decided to go with a more traditional separator. Don’t like it? It’s optional. No delimiter is required. -
**What if I don’t want a constructor, but still want to put methods on created objects?**– That’s fine. The`constructor`

method is totally optional. If you don’t supply one, the default is as if you had typed`constructor() {}`

. -
**Can**– Nope! Adding a`constructor`

be a generator?`constructor`

that’s not a normal method will result in a`TypeError`

. This includes both generators and accessors. -
**Can I define**– Unfortunately not. That would be really hard to detect, so we don’t try. If you define a method with a computed property name that ends up being named`constructor`

with a computed property name?`constructor`

, you will still get a method named`constructor`

, it just won’t be the class’s constructor function. -
**What if I change the value of**– Nope! Much like function expressions, classes get an internal binding of their given name. This binding cannot be changed by external forces, so no matter what you set the`Circle`

? Will that cause`new Circle`

to misbehave?`Circle`

variable to in the enclosing scope,`Circle.circlesMade++`

in the constructor will function as expected. -
**OK, but I could pass an object literal directly as a function argument. This new class thing looks like it won’t work anymore.**– Luckily, ES6 also adds class expressions! They can be either named or unnamed, and will behave exactly the same way as described above, except they won’t create a variable in the scope in which you declare them. -
**What about those shenanigans above with enumerability and so on?**– People wanted to make it so that you could install methods on objects, but that when you enumerated the object’s properties, you only got the added data properties of the object. Makes sense. Because of this, installed methods in classes are configurable, but not enumerable. -
**Hey, wait… what..? Where are my instance variables? What about**– You caught me. They currently don’t exist in class definitions in ES6. Good news, though! Along with others involved in the spec process, I am a strong proponent of both`static`

constants?`static`

and`const`

values being installable in class syntax. In fact, it’s already come up in spec meetings! I think we can look forward to more discussion of this in the future. -
**OK, even still, these are awesome! Can I use them yet?**– Not exactly. There are polyfill options (especially[Babel](https://babeljs.io/)) so that you can play around with them today. Unfortunately, it’s going to be a little while before they are natively implemented in all major browsers. I’ve implemented everything we discussed here today in the[Nightly version of Firefox](https://nightly.mozilla.org/), and it’s implemented but not enabled by default in Edge and Chrome. Unfortunately, it looks like there’s no current implementation in Safari. -
**Java and C++ have subclassing and a**– It does! However, that’s a whole other post’s worth of discussion. Check back with us later for an update about subclassing, where we’ll discuss more about the power of JavaScript classes.`super`

keyword, but there’s nothing mentioned here. Does JS have that?

I would not have been able to implement classes without the guidance and enormous code review responsiblity of [Jason Orendorff](https://hacks.mozilla.org/author/jorendorffmozillacom/) and [Jeff Walden](https://whereswalden.com/).

Next week, Jason Orendorff returns from a week’s vacation and takes up the subject of *let* and *const*.

## 40 comments

Cris MooneyJuly 23rd, 2015 at 07:46Jovica AleksicJuly 23rd, 2015 at 10:45Eric FaustJuly 24th, 2015 at 11:26Phil RickettsJuly 23rd, 2015 at 11:12Miguel CambaJuly 28th, 2015 at 04:02bogusJuly 23rd, 2015 at 13:03Eric FaustJuly 24th, 2015 at 11:29Christian MartinJuly 24th, 2015 at 12:10Jason OrendorffJuly 30th, 2015 at 08:18Eric ElliottJuly 23rd, 2015 at 15:59Jeff WaldenJuly 24th, 2015 at 16:53Eric ElliottJuly 24th, 2015 at 18:55Eric ElliottJuly 24th, 2015 at 19:06Jeff WaldenJuly 25th, 2015 at 16:03Dmitry SoshnikovJuly 24th, 2015 at 12:10Eric FaustJuly 24th, 2015 at 12:26Dmitry SoshnikovJuly 24th, 2015 at 16:03Dmitry SoshnikovJuly 24th, 2015 at 16:15Allen Wirfs-BrockJuly 24th, 2015 at 17:32Simon SpeichJuly 27th, 2015 at 02:25PhistucKJuly 25th, 2015 at 11:10Neil StansburyJuly 27th, 2015 at 03:45Jason OrendorffJuly 30th, 2015 at 09:17Eric ElliottJuly 30th, 2015 at 10:47DominikJuly 27th, 2015 at 06:48simonleungJuly 28th, 2015 at 09:52Jeff WaldenJuly 28th, 2015 at 10:04simonleungJuly 28th, 2015 at 11:12Cris MooneyJuly 29th, 2015 at 07:53Cris MooneyJuly 29th, 2015 at 08:43Jason OrendorffJuly 29th, 2015 at 15:50Neil StansburyJuly 29th, 2015 at 20:15Jason OrendorffJuly 30th, 2015 at 10:28Cris MooneyJuly 30th, 2015 at 12:48PhistucKJuly 29th, 2015 at 08:18Cris MooneyJuly 29th, 2015 at 08:30simonleungJuly 29th, 2015 at 09:58yunpengAugust 6th, 2015 at 20:39Havi Hoffman [Editor]August 7th, 2015 at 11:37markgAugust 8th, 2015 at 14:07