---
title: 'ES6 In Depth: Subclassing – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/08/es6-in-depth-subclassing/
author: Eric Faust
published: '2015-08-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) is a series on new features being added to the JavaScript programming language in the 6th Edition of the ECMAScript standard, ES6 for short.

Two weeks ago, we described [the new classes system](https://hacks.mozilla.org/2015/07/es6-in-depth-classes/) added in ES6 for handling trivial cases of object constructor creation. We showed how you can use it to write code that looks like this:

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

Unfortunately, as some people pointed out, there wasn’t time to talk then about the rest of the power of classes in ES6. Like traditional class systems (C++ or Java, for example), ES6 allows for *inheritance*, where one class uses another as a base, and then extends it by adding more features of its own. Let’s take a closer look at the possibilities of this new feature.

Before we get started talking about subclassing, it will be useful to spend a moment reviewing property inheritance and the *dynamic prototype chain*.

### JavaScript Inheritance

When we create an object, we get the chance to put properties on it, but it also inherits the properties of its prototype objects. JavaScript programmers will be familiar with the existing `Object.create`

API which allows us to do this easily:

`<pre>`


var proto = {

value: 4,

method() { return 14; }

}

var obj = Object.create(proto);

obj.value; // 4

obj.method(); // 14

</pre>

Further, when we add properties to `obj`

with the same name as ones on `proto`

, the properties on `obj`

*shadow* those on `proto`

.

`<pre>`


obj.value = 5;

obj.value; // 5

proto.value; // 4

</pre>

### Basic Subclassing

With this in mind, we can now see how we should hook up the prototype chains of the objects created by a class. Recall that when we create a class, we make a new function corresponding to the `constructor`

method in the class definition which holds all the static methods. We also create an object to be the `prototype`

property of that created function, which will hold all the instance methods. To create a new class which inherits all the static properties, we will have to make the new function object inherit from the function object of the superclass. Similarly, we will have to make the `prototype`

object of the new function inherit from the `prototype`

object of the superclass, for the instance methods.

That description is very dense. Let’s try an example, showing how we could hook this up without new syntax, and then adding a trivial extension to make things more aesthetically pleasing.

Continuing with our previous example, suppose we have a class `Shape`

that we want to subclass:

`<pre>`


class Shape {

get color() {

return this._color;

}

set color(c) {

this._color = parseColorAsRGB(c);

this.markChanged(); // repaint the canvas later

}

}

</pre>

When we try to write code that does this, we have the same problem we had in the previous post with `static`

properties: there’s no syntactic way to change the prototype of a function as you define it. While you can get around this with `Object.setPrototypeOf`

, the approach is generally less performant and less optimizable for engines than having a way to create a function with the intended prototype.

`<pre>`


class Circle {

// As above

}

// Hook up the instance properties

Object.setPrototypeOf(Circle.prototype, Shape.prototype);

// Hook up the static properties

Object.setPrototypeOf(Circle, Shape);

</pre>

This is pretty ugly. We added the classes syntax so that we could encapsulate all of the logic about how the final object would look in one place, rather than having other “hooking things up” logic afterwards. Java, Ruby, and other object-oriented languages have a way of declaring that a class declaration is a subclass of another, and we should too. We use the keyword `extends`

, so we can write:

`<pre>`


class Circle extends Shape {

// As above

}

</pre>

You can put any expression you want after `extends`

, as long as it’s a valid constructor with a `prototype`

property. For example:

- Another class
- Class-like functions from existing inheritance frameworks
- A normal function
- A variable that contains a function or class
- A property access on an object
- A function call

You can even use `null`

, if you don’t want instances to inherit from `Object.prototype`

.

### Super Properties

So we can make subclasses, and we can inherit properties, and sometimes our methods will even shadow (think *override*) the methods we inherit. But what if you want to circumvent this shadowing mechanic?

Suppose we want to write a subclass of our `Circle`

class that handles scaling the circle by some factor. To do this, we could write the following somewhat contrived class:

`<pre>`


class ScalableCircle extends Circle {

get radius() {

return this.scalingFactor * super.radius;

}

set radius() {

throw new Error("ScalableCircle radius is constant." +

"Set scaling factor instead.");

}

// Code to handle scalingFactor

}

</pre>

Notice that the `radius`

getter uses `super.radius`

. This new `super`

keyword allows us to bypass our own properties, and look for the property starting with our prototype, thus bypassing any shadowing we may have done.

Super property accesses (`super[expr]`

works too, by the way) can be used in any function defined with method definition syntax. While these functions can be pulled off of the original object, the accesses are tied to the object on which the method was first defined. This means that pulling the method off into a local variable will not change the behavior of the `super`

access.

`<pre>`


var obj = {

toString() {

return "MyObject: " + super.toString();

}

}

obj.toString(); // MyObject: [object Object]

var a = obj.toString;

a(); // MyObject: [object Object]

</pre>

### Subclassing Builtins

Another thing you might want to do is write extensions to the JavaScript language builtins. The builtin data structures add a huge amount of power to the language, and being able to create new types that leverage that power is amazingly useful, and was a foundational part of the design of subclassing. Suppose you want to write a versioned array. (I know. Trust me, I know.) You should be able to make changes and then commit them, or roll back to previously committed changes. One way to write a quick version of this is by subclassing `Array`

.

`<pre>`


class VersionedArray extends Array {

constructor() {

super();

this.history = [[]];

}

commit() {

// Save changes to history.

this.history.push(this.slice());

}

revert() {

this.splice(0, this.length, this.history[this.history.length - 1]);

}

}

</pre>

Instances of `VersionedArray`

retain a few important properties. They’re bonafide instances of `Array`

, complete with `map`

, `filter`

, and `sort`

. `Array.isArray()`

will treat them like arrays, and they will even get the auto-updating array `length`

property. Even further, functions that would return a new array (like `Array.prototype.slice()`

) will return a `VersionedArray`

!

### Derived Class Constructors

You may have noticed the `super()`

in the `constructor`

method of that last example. What gives?

In traditional class models, constructors are used to initalize any internal state for instances of the class. Each consecutive subclass is responsible for initializing the state associated with that specific subclass. We want to chain these calls, so that subclasses share the same initialization code with the class they are extending.

To call a super constructor, we use the `super`

keyword again, this time as if it were a function. This syntax is only valid inside `constructor`

methods of classes that use `extends`

. With `super`

, we can rewrite our Shape class.

`<pre>`


class Shape {

constructor(color) {

this._color = color;

}

}

class Circle extends Shape {

constructor(color, radius) {

super(color);

this.radius = radius;

}

// As from above

}

</pre>

In JavaScript, we tend to write constructors that operate on the `this`

object, installing properties and initializing internal state. Normally, the `this`

object is created when we invoke the constructor with `new`

, as if with `Object.create()`

on the constructor’s `prototype`

property. However, some builtins have different internal object layouts. Arrays, for example, are laid out differently than regular objects in memory. Because we want to be able to subclass builtins, we let the basemost constructor allocate the `this`

object. If it’s a builtin, we will get the object layout we want, and if it’s a normal constructor, we will get the default `this`

object we expect.

Probably the strangest consequence is the way `this`

is bound in subclass constructors. Until we run the base constructor, and allow it to allocate the `this`

object, we **don’t have a this value**. Consequently, all accesses to

`this`

in subclass constructors that occur before the call to the super constructor will result in a `ReferenceError`

.As we saw in the last post, where you could omit the `constructor`

method, derived class constructors can be omitted, and it is as if you had written:

`<pre>`


constructor(...args) {

super(...args);

}

</pre>

Sometimes, constructors do not interact with the `this`

object. Instead, they create an object some other way, initalize it, and return it directly. If this is the case, it is not necessary to use `super`

. Any constructor may directly return an object, independent of whether super constructors were ever invoked.

`new.target`


Another strange side effect of having the basemost class allocate the `this`

object is that sometimes the basemost class doesn’t know what kind of object to allocate. Suppose you were writing an object framework library, and you wanted a base class `Collection`

, some subclasses of which were arrays, and some of which were maps. Then, by the time you ran the `Collection`

constructor, you wouldn’t be able to tell which kind of object to make!

Since we’re able to subclass builtins, when we run the builtin constructor, internally we already have to know about the `prototype`

of the original class. Without it, we wouldn’t be able to create an object with the proper instance methods. To combat this strange `Collection`

case, we’ve added syntax to expose that information to JavaScript code. We’ve added a new *Meta Property* `new.target`

, which corresponds to the constructor that was directly invoked with `new`

. Calling a function with `new`

sets `new.target`

to be the called function, and calling `super`

within that function forwards the `new.target`

value.

This is hard to understand, so I’ll just show you what I mean:

`<pre>`


class foo {

constructor() {

return new.target;

}

}

class bar extends foo {

// This is included explicitly for clarity. It is not necessary

// to get these results.

constructor() {

super();

}

}

// foo directly invoked, so new.target is foo

new foo(); // foo

// 1) bar directly invoked, so new.target is bar

// 2) bar invokes foo via super(), so new.target is still bar

new bar(); // bar

</pre>

We’ve solved the problem with `Collection`

described above, because the `Collection`

constructor can just check `new.target`

and use it to derive the class lineage, and determine which builtin to use.

`new.target`

is valid inside any function, and if the function is not invoked with `new`

, it will be set to `undefined`

.

### The Best of Both Worlds

Hope you’ve survived this brain dump of new features. Thanks for hanging on. Let’s now take a moment to talk about whether they solve problems well. Many people have been quite outspoken about whether inheritance is even a good thing to codify in a language feature. You may believe that inheritance is never as good as [composition](https://en.wikipedia.org/wiki/Composition_over_inheritance) for making objects, or that the cleanliness of new syntax isn’t worth the resulting lack of design flexibility, as compared with the old prototypal model. It’s undeniable that mixins have become a dominant idiom for creating objects that share code in an extensible way, and for good reason: They provide an easy way to share unrelated code to the same object without having to understand how those two unrelated pieces should fit into the same inheritance structure.

There are many vehemently held beliefs on this topic, but I think there are a few things worth noting. First, the addition of classes as a language feature does not make their use mandatory. Second, and equally important, the addition of classes as a language feature doesn’t mean they are always the best way to solve inheritance problems! In fact, some problems are better suited to modeling with prototypal inheritance. At the end of the day, classes are just another tool that you can use; not the only tool nor necessarily the best.

If you want to continue to use mixins, you may wish that you could reach for classes that inherit from several things, so that you could just inherit from each mixin, and have everything be great. Unfortunately, it would be quite jarring to change the inheritance model now, so JavaScript does not implement multiple inheritance for classes. That being said, there is a hybrid solution to allow mixins inside a class-based framework. Consider the following functions, based on the well-known `extend`

mixin idiom.

`<pre>`


function mix(...mixins) {

class Mix {}

// Programmatically add all the methods and accessors

// of the mixins to class Mix.

for (let mixin of mixins) {

copyProperties(Mix, mixin);

copyProperties(Mix.prototype, mixin.prototype);

}

return Mix;

}

function copyProperties(target, source) {

for (let key of Reflect.ownKeys(source)) {

if (key !== "constructor" && key !== "prototype" && key !== "name") {

let desc = Object.getOwnPropertyDescriptor(source, key);

Object.defineProperty(target, key, desc);

}

}

}

</pre>

We can now use this function `mix`

to create a composed superclass, without ever having to create an explicit inheritance relationship between the various mixins. Imagine writing a collaborative editing tool in which editing actions are logged, and their content needs to be serialized. You can use the `mix`

function to write a class `DistributedEdit`

:

`<pre>`


class DistributedEdit extends mix(Loggable, Serializable) {

// Event methods

}

</pre>

It’s the best of both worlds. It’s also easy to see how to extend this model to handle mixin classes that themselves have superclasses: we can simply pass the superclass to `mix`

and have the return class extend it.

### Current Availability

OK, we’ve talked a lot about subclassing builtins and all these new things, but can you use any of it now?

Well, sort of. Of the major browser vendors, Chrome has shipped the most of what we’ve talked about today. When in strict mode, you should be able to do just about everything we discussed, except subclass `Array`

. Other builtin types will work, but `Array`

poses some extra challenges, so it’s not surprising that it’s not finished yet. I am writing the implementation for Firefox, and aim to hit the same target (everything but `Array`

) very soon. Check out [bug 1141863](https://bugzilla.mozilla.org/show_bug.cgi?id=1141863) for more information, but it should land in the Nightly version of Firefox in a few weeks.

Further off, Edge has support for `super`

, but not for subclassing builtins, and Safari does not support any of this functionality.

Transpilers are at a disadvantage here. While they are able to create classes, and to do `super`

, there’s basically no way to fake subclassing builtins, because you need engine support to get instances of the base class back from builtin methods (think `Array.prototype.splice`

).

Phew! That was a long one. Next week, Jason Orendorff will be back to discuss the ES6 module system.

## 5 comments

PhistucKAugust 8th, 2015 at 04:01simonleungAugust 8th, 2015 at 07:51FreshersAugust 8th, 2015 at 11:19magaAugust 12th, 2015 at 04:24Nathaniel TuckerSeptember 2nd, 2015 at 21:01