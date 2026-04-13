---
title: Constructors Are Bad For JavaScript
url: https://tsherif.wordpress.com/2013/08/04/constructors-are-bad-for-javascript/
author: Tarek Sherif
published: '2013-08-04'
source_blog: Tarek Sherif
source_site: https://tsherif.wordpress.com
category: game programming
fetched: '2026-04-13'
---

JavaScript is a language that has always been at odds with itself. It derives its core strength from a simple, flexible object model that allows code reuse through direct object-to-object prototypal inheritance, and a powerful execution model based on functions that are simply executable objects. Unfortunately, there are many aspects of the language that obscure this powerful core. It is [well-known](https://en.wikipedia.org/wiki/JavaScript#Birth_at_Netscape) that JavaScript originally wanted to look like other popular languages built on fundamentally different philosophies, and this trend in its history has lead to constructs in the language that actively work against its natural flow.


Consider the fact that although the prototypal, object-to-object inheritance mentioned above is a core aspect of the language, there was **no way**, until ECMAScript 5, to simply say “I want to create an object whose prototype is this other object”. You would have to do something like the following:

var proto = {protoprop: "protoprop"}; function C() {} //Dummy throwaway constructor. C.prototype = proto; var obj = new C(); proto.isPrototypeOf(obj); => true

Thankfully, using `Object.create()`

, this can now be simplified to:

var proto = {protoprop: "protoprop"}; var obj = Object.create(proto); proto.isPrototypeOf(obj); => true

The latter construct is much more in tune with JavaScript’s core structure. The constructor mechanism used in the former example is a clunky indirection of the simple object-to-object inheritance model the language actually uses, but until recently there was no other way for objects to inherit from one another. They were forced to use constructors as mediators. This gave JavaScript the veneer of a typed, class-based language, while obfuscating and actively interfering with its natural structure and flow.

# Constructors

In [JavaScript: The Good Parts](http://shop.oreilly.com/product/9780596517748.do), Douglas Crockford warns against using the `new`

keyword for constructor invocation. I’ll admit that when I first read this, I believed his argument to be based mainly on the dangers of forgetting `new`

and polluting the global namespace:

function C() { this.instance_member = "whoops!" } var c = C(); // Forgot "new" c; => undefined; window.instance_member; // Property added to global namespace! => "whoops!"

But in [JavaScript Patterns](http://shop.oreilly.com/product/9780596806767.do), Stoyan Stefanov suggests using the following pattern to safeguard against accidentally polluting the global namespace:

function C() { if (! (this instanceof C)) { return new C(); } this.instance_member = "This is ok."; } var c = C(); // Is this a constructor? c; => {instance_member:"This is ok."} window.instance_member; // No global namespace pollution. => undefined

Allowing a constructor to be used without `new`

looks a little strange, and one might argue that it makes the code less clear, but this pattern does make the constructor much safer. And using the constructor mechanism allows us to organize our code in a class-like manner around constructor-object links:

c instanceof C; // It's like a class, right? => true c.constructor === C; => true

This seemed like a perfect solution, and it gave me the impression that perhaps Crockford was being overcautious. But digging a little deeper, I stumbled upon the following bit of odd behaviour. I’ll use standard constructor invocation to make things clear:

// Constructor function C() {} // Create object. var c = new C(); c instanceof C; => true c.constructor === C; => true // Change prototype C.prototype = { prototype_prop : "proto"}; c.constructor === C; => true c instanceof C; // instanceof no longer works! => false

Changing the prototype breaks `instanceof`

! On a conceptual level, I suppose one could argue that if you change the prototype a constructor uses to create objects, it can’t really be considered the template for objects created before the change. And that’s essentially all `instanceof`

does: [it checks prototypes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof). But that means the result of `c instanceof C`

has nothing to do with what `C`

actually is! This is especially clear in the following example:

// Create two constructors with the // same prototype. var proto = {protoprop: "protoprop"}; function C() { this.cprop = "cprop" }; C.prototype = proto; function F() { this.fprop = "fprop" }; F.prototype = proto; var f = new F(); f.protoprop; // Has prototype properties => "protoprop" f.fprop; // Has F properties => "fprop" f.cprop; // Doesn't have C properties => undefined f instanceof C; // Is an instance of C!?! => true

So the `instanceof`

operator is **extremely** misleading about what it’s doing. `c instanceof C`

does not mean that `c`

was created by `C`

or that `c`

has anything to do with `C`

. It basically just means “at this moment, the prototype `C`

will use if it’s invoked as a constructor (even if it’s never actually invoked as a constructor) appears somewhere in the chain of prototypes of `c`

”. Essentially, it’s equivalent to `C.prototype.isPrototypeOf(c)`

, but the latter is far more upfront about what it’s actually doing.

Also consider the rarely used `constructor`

property that’s set for all objects. The information it provides is of questionable value:

function C() {} C.prototype = { prototype_prop : "proto"}; // Changing the prototype breaks the constructor // property for all objects created after the change. c = new C(); c instanceof C; => true c.constructor === C; => false

A full treatment of this behaviour can be found [here](http://zeekat.nl/articles/constructors-considered-mildly-confusing.html), but essentially, the `constructor`

property of an object is set by the engine exactly once. When a function is defined, its `prototype`

property is initialized to an object with a `constructor`

property pointing back to the function itself. If you set the function’s `prototype`

property to some other object, without explicitly setting that new object’s `constructor`

property, all objects created by the function will have their constructor properties set to `Object`

(which is the default).

So why do `instanceof`

and the `constructor`

property even exist in JavaScript? They create false links between objects and the functions that create them in a manner so brittle and misleading that they only serve to obfuscate how the code actually works. I believe they exist simply to prop up a fundamentally broken construct: the constructor. To be clear, constructors, at their core, are useful: they are simply functions for creating objects. The key problem is all the extra baggage that comes with that creation. Why should an object be considered an `instanceof`

the function that creates it? Why the mysterious invocation of `new`

to magically create the new object?

What we need is a way to take advantage of the reuse patterns of constructors, while at the same time writing code that is more explicit about what it’s actually doing. This can be done by pushing the object creation and inheritance code directly into the constructor, essentially turning it into a **factory function**.

# Factory Functions

Writing explicit factory functions involves relatively minor changes to the code of constructors. Say, for example, that we have a constructor like the following:

function MyObject(data) { this.data = data; } MyObject.prototype = { getData: function() { return this.data; } } var o = new MyObject("data");

This can be replaced by the following equivalent factory function:

function myObject(data) { var obj = Object.create(myObject.proto); obj.data = data; return obj; } myObject.proto = { getData: function() { return this.data; } } var o = myObject("data");

The objects created by the constructor and the factory function are equivalent, but the factory function construct has the following advantages:

- There’s no risk of using it in the “wrong” way. It doesn’t require
`new`

, as it isn’t meant to be used as a constructor. Nor is it a constructor that forces proper invocation, essentially hiding errors. The factory function is meant to be used in exactly one way: as a regular function. - There’s no pretense of creating a “class” of objects by capitalizing the name or otherwise trying to make it look like the classes of other languages. The
`prototype`

property isn’t used, so there will be no`instanceof`

link between the function and the objects it creates. It is simply a function that happens to create objects.

So the advantages aren’t just theoretical. Code written in this way will be more maintainable and less error-prone.

Taking this idea a step further, if we want to go all the way and not use `new`

at all in our code, the following generic factory can be used to invoke constructor functions in a more explicit manner:

function genericFactory(Ctr) { var obj = Object.create(Ctr.prototype); var args = Array.prototype.slice.call(arguments, 1); Ctr.apply(obj, args); return obj; }

Using it to invoke the `MyObject`

constructor described earlier in this section would look like the following:

var o = genericFactory(MyObject, "data");

Whether this makes the code clearer or not might be debatable, but one definite advantage is that this construct allows us to invoke constructors dynamically, something not possible with invocations that use `new`

. This example also shows more generally that constructor invocation can be done away with quite easily with the tools now afforded us in ECMAScript 5.

# Conclusions

JavaScript at its core, is a simple, elegant, expressive language that has unfortunately been weighed down by its confused history. Constructors, as an example, were clearly introduced to give the JavaScript the appearance of other popular, class-based, object-oriented languages, but as was discussed here, they at best mislead, and at worst actively interfere with our ability to engage with the core structure of the language. Constructors run contrary to the prototypal, functional, object-based nature from which JavaScript draws its strength. I believe that by putting them aside, by recognizing them as artifacts of a time when JavaScript was trying to look like something other than itself, we’ll be able to embrace the language for what it actually is and write clearer, safer, more elegant and more maintainable code.

If you start with the assumption that prototypal inheritance is somehow cleaner/better than class-based inheritance, you’re right.

If you start with the assumption that both have their places, however, …

Constructors serve exactly the same purpose in JS that they serve in C++, Java, VB, Cobol, Fortran, …

JS supports class-based and prototypal. It’s better with class-based. (A JS “prototype” lets an object be inherited by a class.)

Thanks for your comments, Martin.

I wouldn’t say I’m starting with the assumption that prototypal inheritance is better. More that prototypal inheritance is the only kind that’s actually implemented in JavaScript. The class-based model, built around constructors, only serves to obscure this fact, especially given that the only meaningful definition of a class in JavaScript is “objects that share a prototype”.

And I wouldn’t agree that constructors in JavaScript serve the same purpose they do in C++ and Java. Those languages implement classes as something concrete that exists in memory, and constructors serve to instantiate those classes. The classes act as a concrete type for the objects they create. JavaScript, on the other hand, has no implemented concept of a class. Constructors create a “class” simply by linking objects to their prototypes. So why not deal with objects and their prototypes directly and avoid confusing the issue?

I have never seen any evidence that classical inheritance has a place alongside prototypal OO. What I do see is a lot of people stuck in their ways who have little understanding of how to take best advantage of prototypal inheritance, and little understanding of the many pitfalls inherent with classical inheritance.

See: “Classical Inheritance is Obsolete: How to Think in Prototypal OO” – https://vimeo.com/69255635

Very interesting points, but I’ve never seen this cause problems in real world code. However, what I *have* seen cause problems is the fact that instanceof and isPrototypeOf don’t work across execution contexts. They should be avoided in JavaScript in favor of things like ducktyping and generic functions (functions that work with any object that supports the required properties).

Here’s an example of a generic function in JavaScript:

var longest = function longest() {

var args = [].slice.call(arguments),

max = args[0] || [];

return args.reduce(function (previousValue, currentValue) {

if (currentValue && currentValue.length > max.length) {

max = currentValue;

}

return max;

});

}

longest(undefined, ‘aoeu’, [1,2,3], null, false, ‘abcdefg’, {length:43}); // {length:43}

Thanks for the comments, Eric.

True, I don’t think the issues related to constructor-object links necessarily come up in day-to-day development. What I was getting at more is that the entire class/aconstructor/new/instanceof mechanism in JavaScript is fundamentally broken at a conceptual level. One real world issue related to them is that I do think they make it harder for new developers to really understand how the language works. The “make it look like Java” philosophy lead to a very unclear syntax that I think acts as a hurdle that you have to get over to really understand how the language works. And since things can be done in more direct ways, why use misleading constructs?

Duck typing definitely makes sense as an approach to JavaScript development. I’ve become very comfortable with it in Ruby, and it allows for an amazing amount of code reuse that’s not possible if you’re stuck thinking in terms of static “types”. And I would say that most developers are used to a kind of duck typing in JS. When you write something like “Array.prototype.slice.call(arguments)” in a function, aren’t you duck typing “arguments”, an object that isn’t an array but has the necessary properties to act like one? It’s just a question of applying that same approach more generally.

Very good points. Just don’t forget `.call()` with that idiom. 😉

Ack! Thanks for catching that. Fixed it!

How true your quote is … “I do think they make it harder for new developers to really understand how the language works”. I’m NOT a professional JavaScript developer and I’m on the first rung of the ladder to learn the JavaScript language; simply because I find it interesting. But trying to find out the best way to program using JavaScript is a minefield of confusion. What parts to ignore(Bad parts). What parts to use(the Good parts). Should I just use a combination of simple functions, or what about functional programming? Help! Where is the way ahead?

I know I should probably buy a good JS book, but how do I determine whether it is using the “best” style of programming in JS?

Thanks for commenting, john. In the end, finding the “best” style will come down to taste and your own programming habits. Some key priorities for me are:

1. Clarity: Making it easier for myself and other devs understand what the code does.

2. Robustness: Avoiding patterns that can lead to hard-to-find bugs.

Thanks, this was a helpful post. Factory function pattern is interesting.

Thanks, Ryan 🙂 Glad you found it useful.

You should like my frameworks 🙂

They have no classes, and no constructors:

https://github.com/quadroid/clonejs-nano

https://github.com/quadroid/clonejs

Looks very interesting, Alexander. I’m curious to take a closer look and see how you’re implementing the lazy loading of properties. Two other libraries you might be interested in are Eric Elliot’s stampit: https://github.com/dilvie/stampit

And my oFactory: https://github.com/tsherif/oFactory

They’re both libraries for creating object factories. Mine was heavily inspired by Eric’s.

I have a question that bothers me for a long time: why do we want to move some part of ‘Class’ declaration out of the function, using FuncName.prototype = { someMethod: …} or FuncName.proto = {} syntax — at all?

Why not just have everything inside the func body, like in classical Doug’s object creation pattern:

function Name (params, parent) {

var obj = parent || {};

obj.name = ‘xx’;

obj.someMethod = function () {…}

return obj;

}

What, if any, a benefit of defining someMethod outside, in Name.prototype construct? I don’t think this is because of ‘every new object will have copy of func body’ — I guess interpreter can handle that just well. Why then? An interface that can be mixed into different ‘Classes’? Not so: the construct explicitly references its target function (*Name*.prototype). Why then?

Thanks in advance.

Hi Pavel. What’s going on there is not just defining methods outside the creator function. You’re defining them on the prototype. All objects in JavaScript (except Object.prototype) have a prototype object from which they inherit properties. The advantage of defining properties on the prototype is that they are defined once for all objects that inherit from that prototype, so you get a savings in terms of the memory cost of your objects. This is generally most useful for methods, since they define the behaviour of your objects, and you usually want shared behaviour among objects with the same prototype. On the other hand, you usually do not want data properties defined on the prototype as they define state, and you usually want this to be separate among the separate objects, even if they share a prototype. (If the prototype data property changes, it will change for all objects that inherit from that prototype). You can find more information about all this here: http://goo.gl/Bg4R8p

Thanks Tarek. I quite understand the mechanics of prototypes (probably not perfectly for still cannot find it useful).

1. Sharing properties across instances is not practical, as you said and I agree — so this is gone.

2. Sharing methods? I believe that interpreters are not stupid and having:

a) function Name () { return { myMethod: function () {} }; }

or b) function Name () {};

Name.prototype = { myMethod: function () {} };

..and then:

var inst1 = Name(), inst2 = Name();

..will 1) consume the same memory (obvious optimization) and 2) behave identically. So why bother?

3. I can figure out a ‘usage’ of it though: overriding myMethod for *all* instances in run-time? But again this is unpractical and I’d say insane 🙂

So, the question actually is: is there any *practical* pattern of using this property of prototypes?

—

Hi Pavel,

I don’t really understand the “obvious optimization” you’re describing. Nothing of the sort happens in JavaScript, and if it did it would break a lot of the expressive power of the language. Functions are objects that can have separate instances with their own properties and their own closures.

Objects created by your two

Name()functions (I’m assuming the second one was meant to be invoked withnew. It won’t work otherwise), will not behave at all in the same way. Consider the following code (using your constructor version):Objects

n1andn2nowbothhave asayHellomethod defined. This is not possible will your first version ofName(), or more generally without using prototypes.For a more useful example, consider what the following code does:

Tarek,

Thanks for pointing out this pattern. I mean extending objects that I cannot/must not change diractly – namely native objects and objects from 3rd-party libs. This way I see how prototypes are useful.

Regarding performance, I thought about closures (not properties of function, for I think they are evil). But my point is (purely intuitive) that despite closures, the code, I mean *processor instructions*, will still be the same. E.g. in case of some hypothetical Obj.prototype.add vs Obj.add there will be assembly somewhere like:

mov eax, [ebp + 8]

add eax, eax

I argue there will be only *one* instance of such instructions in memory due to optimizations.

Back to prototypes, I see where is my confusion come from: I never extended 3rd-party libs this way and never extended native objects this way too (because there are libs that do it already). My question was more like how to use it in practical day-to-day programming (i.e. manipulating DOM), now I see this is from a slightly different field 🙂

Cheers.

Pardon my ignorance but you use the term “protypal”, is this a new concept or did you mean prototypal. I ask as I have seen this term used in a number of articles.

Not sure about the other articles, but in my case, it was just a typo. Thanks for pointing it out, Tracy.

Hi Tarek. Thanks for posting this – I’ve found it very useful whilst researching some of the ideas behind avoiding ‘new’ etc. The genericFactory function seems like a great idea.

I was wondering, how might you extend one object instance (that will be created by a factory) from within another factory – or am I missing the point?

If for example [Factory A ]provides me with ‘examplar’ objects that are extended from within Factory B. it seems like the only way to get hold of this object is to invoke Factory A from within B.

My thinking’s a little tangled here.

Thanks for the comment, James. I’d suggest using what’s often referred to as “functional inheritance” where you could have your factory functions either create an object or modify one that’s passed in as argument:

It still seems over-complicated to me. I don’t see any good reason to use constructors or factories or any object that exists only to be used as a template to create other objects. Just write objects.

What’s the point of an “empty” generic-car “class” that is used just to stamp-out other cars?