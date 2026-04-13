---
title: 'ES6 In Depth: Proxies – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/07/es6-in-depth-proxies-and-reflect/
author: Jason Orendorff
published: '2015-07-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) is a series on new features being added to the JavaScript programming language in the 6th Edition of the ECMAScript standard, ES6 for short.

Here is the sort of thing we are going to do today.

`<pre>`


var obj = new Proxy({}, {

get: function (target, key, receiver) {

console.log(`getting ${key}!`);

return Reflect.get(target, key, receiver);

},

set: function (target, key, value, receiver) {

console.log(`setting ${key}!`);

return Reflect.set(target, key, value, receiver);

}

});

</pre>

That’s a little complicated for a first example. I’ll explain all the parts later. For now, check out the object we created:

`<pre>`


> obj.count = 1;

setting count!

> ++obj.count;

getting count!

setting count!

2

</pre>

What’s going on here? We are intercepting property accesses on this object. We are overloading the `"."`

operator.

### How it’s done

The best trick in computing is called virtualization. It’s a very general-purpose technique for doing astonishing things. Here’s how it works.

-
Take any picture.

![(picture of a coal power plant)](../../assets/3d8744c0c04e9351.jpg)

[Photo credit: Martin Nikolaj Bech](https://www.flickr.com/photos/martini_dk/369891979) -
Draw an outline around something in the picture.

![(same photo, with the power plant circled)](../../assets/131cca37397e1380.png)


-
Now replace either everything inside the outline, or everything outside the outline, with something totally unexpected. There is just one rule, the Rule of Backwards Compatibility. Your replacement must behave enough like what was there before that

*nobody on the other side of the line notices that anything has changed.*![(the circled part is replaced with a wind farm)](../../assets/3b1df07f41d536cf.png)

[Photo credit: Beverley Goodwin.](https://www.flickr.com/photos/bevgoodwin/8671334130/)

You’ll be familiar with this kind of hack from classic computer science films such as *The Truman Show* and *The Matrix*, where a person is inside the outline, and the rest of the world has been replaced with an elaborate illusion of normalcy.

In order to satisfy the Rule of Backwards Compatibility, your replacement may need to be cunningly designed. But the real trick is in drawing the right outline.

By *outline*, I mean an API boundary. An interface. Interfaces specify how two bits of code interact and what each part expects of the other. So if an interface is designed into the system, the outline is already drawn for you. You know you can replace either side, and the other side won’t care.

It’s when there’s *not* an existing interface that you have to get creative. Some of the coolest software hacks of all time have involved drawing an API boundary where previously there was none, and bringing that interface into existence via a prodigious engineering effort.

[Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory), [Hardware virtualization](https://en.wikipedia.org/wiki/Hardware_virtualization), [Docker](https://en.wikipedia.org/wiki/Docker_%28software%29), [Valgrind](http://valgrind.org/), [rr](http://rr-project.org/)—to various degrees all of these projects involved driving new and rather unexpected interfaces into existing systems. In some cases, it took years and new operating system features and even new hardware to make the new boundary work well.

The best virtualization hacks bring with them a new understanding of whatever’s being virtualized. To write an API for something, you have to understand it. Once you understand, you can do amazing things.

ES6 introduces virtualization support for JavaScript’s most fundamental concept: the object.

### What is an object?

No, really. Take a moment. Think it over. Scroll down when you know what an object is.

![(picture of Auguste Rodin’s sculpture, The Thinker)](https://hacks.mozilla.org/wp-content/uploads/2015/07/thinker-500x274.jpg)


![(picture of Auguste Rodin’s sculpture, The Thinker)](https://hacks.mozilla.org/wp-content/uploads/2015/07/thinker-500x274.jpg)

[Photo credit: Joe deSousa.](https://www.flickr.com/photos/mustangjoe/5966894496/)

This question is too hard for me! I’ve never heard a really satisfying definition.

Is that surprising? Defining fundamental concepts is always hard—check out the first few definitions in [Euclid’s Elements](http://aleph0.clarku.edu/~djoyce/java/elements/bookI/bookI.html) sometime. The ECMAScript language specification is in good company, therefore, when it unhelpfully defines an object as a “member of the type Object.”

Later, the spec adds that “An Object is a collection of properties.” That’s not bad. If you want a definition, that will do for now. We’ll come back to it later.

I said before that *to write an API for something, you have to understand it.* So in a way, I’ve promised that if we get through all this, we’re going to understand objects better, and we’ll be able to do amazing things.

So let’s follow in the footsteps of the ECMAScript standard committee and see what it would take to define an API, an interface, for JavaScript objects. What sort of methods do we need? What can objects *do?*

That depends somewhat on the object. DOM Element objects can do certain things; AudioNode objects do other things. But there are a few fundamental abilities all objects share:

- Objects have properties. You can get and set properties, delete them, and so on.
- Objects have prototypes. This is how inheritance works in JS.
- Some objects are functions or constructors. You can call them.

Almost everything JS programs do with objects is done using properties, prototypes, and functions. Even the special behavior of an Element or AudioNode object is accessed by calling methods, which are just inherited function properties.

So when the ECMAScript standard committee defined a set of 14 internal methods, the common interface for all objects, it should come as no surprise that they ended up focusing on these three fundamental things.

The full list can be found in [tables 5 and 6 of the ES6 standard](http://www.ecma-international.org/ecma-262/6.0/index.html#table-5). Here I’ll just describe a few. The weird double brackets, [[ ]], emphasize that these are *internal* methods, hidden from ordinary JS code. You can’t call, delete, or overwrite these like ordinary methods.

-
– Get the value of a property.`obj`.[[Get]](`key`,`receiver`)Called when JS code does:

`obj.prop`

or`obj[key]`

.`obj`is the object currently being searched;`receiver`is the object where we first started searching for this property. Sometimes we have to search several objects.`obj`might be an object on`receiver`’s prototype chain. -
– Assign to a property of an object.`obj`.[[Set]](`key`,`value`,`receiver`)Called when JS code does:

`obj.prop = value`

or`obj[key] = value`

.In an assignment like

`obj.prop += 2`

, the [[Get]] method is called first, and the [[Set]] method afterwards. Same goes for`++`

and`--`

. -
– Test whether a property exists.`obj`.[[HasProperty]](`key`)Called when JS code does:

`key in obj`

. -
– List`obj`.[[Enumerate]]()`obj`’s enumerable properties.Called when JS code does:

`for (key in obj) ...`

.This returns an iterator object, and that’s how a

`for`

–`in`

loop gets an object’s property names. -
– Return`obj`.[[GetPrototypeOf]]()`obj`’s prototype.Called when JS code does:

`obj.<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/proto" target="_blank">__proto__</a>`

or`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getPrototypeOf" target="_blank">Object.getPrototypeOf</a>(obj)`

. -
– Call a function.`functionObj`.[[Call]](`thisValue`,`arguments`)Called when JS code does:

`functionObj()`

or`x.method()`

.Optional. Not every object is a function.

-
– Invoke a constructor.`constructorObj`.[[Construct]](`arguments`,`newTarget`)Called when JS code does:

`new Date(2890, 6, 2)`

, for example.Optional. Not every object is a constructor.

The

`newTarget`argument plays a role in subclassing. We’ll cover it in a future post.

Maybe you can guess at some of the other seven.

Throughout the ES6 standard, wherever possible, any bit of syntax or builtin function that does anything with objects is specified in terms of the 14 internal methods. ES6 drew a clear boundary around the brains of an object. What proxies let you do is replace the standard kind of brains with arbitrary JS code.

When we start talking about overriding these internal methods in a moment, remember, we’re talking about overriding the behavior of core syntax like `obj.prop`

, builtin functions like `<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys" target="_blank">Object.keys()</a>`

, and more.

`Proxy`


ES6 defines a new global constructor, `<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy" target="_blank">Proxy</a>`

. It takes two arguments: a *target* object and a *handler* object. So a simple example would look like this:

`<pre>`


var target = {}, handler = {};

var proxy = new Proxy(target, handler);

</pre>

Let’s set aside the handler object for a moment and focus on how `proxy` and `target` are related.

I can tell you how `proxy` is going to behave in one sentence. All of `proxy`’s internal methods are forwarded to `target`. That is, if something calls `proxy`.[[Enumerate]](), it’ll just return `target`.[[Enumerate]]().

Let’s try it out. We’ll do something that causes `proxy`.[[Set]]() to be called.

`<pre>`


proxy.color = "pink";

</pre>

OK, what just happened? `proxy`.[[Set]]() should have called `target`.[[Set]](), so that should have made a new property on `target`. Did it?

`<pre>`


> target.color

"pink"

</pre>

It did. And the same goes for all the other internal methods. This proxy will, for the most part, behave exactly the same as its target.

There are limits to the fidelity of the illusion. You’ll find that `proxy !== target`

. And a proxy will sometimes flunk type checks that the target would pass. Even if a proxy’s target is a DOM Element, for example, the proxy isn’t *really* an Element; so something like `document.body.appendChild(proxy)`

will fail with a `TypeError`

.

### Proxy handlers

Now let’s return to the handler object. This is what makes proxies useful.

The handler object’s methods can override any of the proxy’s internal methods.

For example, if you’d like to intercept all attempts to assign to an object’s properties, you can do that by defining a `<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy/handler/set" target="_blank">handler.set()</a>`

method:

`<pre>`


var target = {};

var handler = {

set: function (target, key, value, receiver) {

throw new Error("Please don't set properties on this object.");

}

};

var proxy = new Proxy(target, handler);

> proxy.name = "angelina";

Error: Please don't set properties on this object.

</pre>

The full list of handler methods is [documented on the MDN page for Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy#Methods_of_the_handler_object). There are 14 methods, and they line up with the 14 internal methods defined in ES6.

All handler methods are optional. If an internal method is not intercepted by the handler, then it’s forwarded to the target, as we saw before.

### Example: “Impossible” auto-populating objects

We now know enough about proxies to try using them for something really weird, something that’s impossible without proxies.

Here’s our first exercise. Make a function `Tree()`

that can do *this:*

`<pre>`


> var tree = Tree();

> tree

{ }

> tree.branch1.branch2.twig = "green";

> tree

{ branch1: { branch2: { twig: "green" } } }

> tree.branch1.branch3.twig = "yellow";

{ branch1: { branch2: { twig: "green" },

branch3: { twig: "yellow" }}}

</pre>

Note how all the intermediate objects `branch1`, `branch2`, and `branch3`, are magically autocreated when they’re needed. Convenient, right? How could it possibly work?

Until now, there’s no way it *could* work. But with proxies this is only a few lines of code. We just need to tap into `tree`.[[Get]](). If you like a challenge, you might want to try implementing this yourself before reading on.

![(picture of a tap in a maple tree)](https://hacks.mozilla.org/wp-content/uploads/2015/07/maple-tap-500x333.jpg)


![(picture of a tap in a maple tree)](https://hacks.mozilla.org/wp-content/uploads/2015/07/maple-tap-500x333.jpg)

[Photo credit: Chiot’s Run.](https://www.flickr.com/photos/chiotsrun/5446345665/)

Here’s my solution:

`<pre>`


function Tree() {

return new Proxy({}, handler);

}

var handler = {

get: function (target, key, receiver) {

if (!(key in target)) {

target[key] = Tree(); // auto-create a sub-Tree

}

return Reflect.get(target, key, receiver);

}

};

</pre>

Note the call to `Reflect.get()`

at the end. It turns out there’s an extremely common need, in proxy handler methods, to be able to say “now just do the default behavior of delegating to `target`.” So ES6 defines a new [ Reflect object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect) with 14 methods on it that you can use to do exactly that.

### Example: A read-only view

I think I may have given the false impression that proxies are easy to use. Let’s do one more example to see if that’s true.

This time our assignment is more complex: we have to implement a function, `readOnlyView(object)`

, that takes any object and returns a proxy that behaves just like that object, *except* without the ability to mutate it. So, for example, it should behave like this:

`<pre>`


> var newMath = readOnlyView(Math);

> newMath.min(54, 40);

40

> newMath.max = Math.min;

Error: can't modify read-only view

> delete newMath.sin;

Error: can't modify read-only view

</pre>

How can we implement this?

The first step is to intercept all internal methods that would modify the target object if we let them through. There are five of those.

`<pre>`


function NOPE() {

throw new Error("can't modify read-only view");

}

var handler = {

// Override all five mutating methods.

set: NOPE,

defineProperty: NOPE,

deleteProperty: NOPE,

preventExtensions: NOPE,

setPrototypeOf: NOPE

};

function readOnlyView(target) {

return new Proxy(target, handler);

}

</pre>

This works. It prevents assignment, property definition, and so on via the read-only view.

Are there any loopholes in this scheme?

The biggest problem is that the [[Get]] method, and others, may still return mutable objects. So even if some object `x`

is a read-only view, `x.prop`

may be mutable! That’s a huge hole.

To plug it, we must add a `handler.get()`

method:

`<pre>`


var handler = {

...

// Wrap other results in read-only views.

get: function (target, key, receiver) {

// Start by just doing the default behavior.

var result = Reflect.get(target, key, receiver);

// Make sure not to return a mutable object!

if (Object(result) === result) {

// result is an object.

return readOnlyView(result);

}

// result is a primitive, so already immutable.

return result;

},

...

};

</pre>

This is not sufficient either. Similar code is needed for other methods, including `getPrototypeOf`

and `getOwnPropertyDescriptor`

.

Then there are further problems. When a getter or method is called via this kind of proxy, the `this`

value passed to the getter or method will typically be the proxy itself. But as we saw earlier, many accessors and methods perform a type check that the proxy won’t pass. It would be better to substitute the target object for the proxy here. Can you figure out how to do it?

The lesson to draw from this is that creating a proxy is easy, but creating a proxy with intuitive behavior is quite hard.

### Odds and ends

-
**What are proxies really good for?**They’re certainly useful whenever you want to observe or log accesses to an object. They’ll be handy for debugging. Testing frameworks could use them to create

[mock objects](https://en.wikipedia.org/wiki/Mock_object).Proxies are useful if you need behavior that’s just slightly past what an ordinary object can do: lazily populating properties, for example.

I almost hate to bring this up, but one of the best ways to see what’s going on in code that uses proxies… is to wrap a proxy’s handler object in

*another proxy*that logs to the console every time a handler method is accessed.Proxies can be used to restrict access to an object, as we did with

`readOnlyView`

. That sort of use case is rare in application code, but Firefox uses proxies internally to implement[security boundaries](https://developer.mozilla.org/en-US/docs/Mozilla/Gecko/Script_security)between different domains. They’re a key part of our security model. -
**Proxies ♥ WeakMaps.**In our`readOnlyView`

example, we create a new proxy every time an object is accessed. It could save a lot of memory to cache every proxy we create in a`WeakMap`

, so that however many times an object is passed to`readOnlyView`

, only a single proxy is created for it.This is one of the motivating use cases for

`WeakMap`

. -
**Revocable proxies.**ES6 also defines another function,`Proxy.revocable(target, handler)`

, that creates a proxy, just like`new Proxy(target, handler)`

, except this proxy can be revoked later. (`Proxy.revocable`

returns an object with a`.proxy`

property and a`.revoke`

method.) Once a proxy is revoked, it simply doesn’t work anymore; all its internal methods throw. -
**Object invariants.**In certain situations, ES6 requires proxy handler methods to report results that are consistent with the*target*object’s state. It does this in order to enforce rules about immutability across all objects, even proxies. For example, a proxy can’t claim to be inextensible unless its target really is inextensible.The exact rules are too complex to go into here, but if you ever see an error message like

`"proxy can't report a non-existent property as non-configurable"`

, this is the cause. The most likely remedy is to change what the proxy is reporting about itself. Another possibility is to mutate the target on the fly to reflect whatever the proxy is reporting.

### What is an object now?

I think where we left it was: “An Object is a collection of properties.”

I’m not totally happy with this definition, even taking for granted that we throw in prototypes and callability as well. I think the word “collection” is too generous, given how poorly defined a proxy can be. Its handler methods could do anything. They could return random results.

By figuring out what an object can do, standardizing those methods, and adding virtualization as a first-class feature that everyone can use, the ECMAScript standard committee has expanded the realm of possibilities.

Objects can be almost anything now.

Maybe the most honest answer to the question “What is an object?” now is to take the 12 required internal methods as a definition. An object is something in a JS program that has a [[Get]] operation, a [[Set]] operation, and so on.

Do we understand objects better after all that? I’m not sure! Did we do amazing things? Yeah. We did things that were never possible in JS before.

### Can I use Proxies today?

Nope! Not on the Web, anyway. Only Firefox and Microsoft Edge support proxies, and there is no polyfill.

Using proxies in Node.js or io.js requires both an off-by-default option (`--harmony_proxies`

) *and* the [harmony-reflect](https://github.com/tvcutsem/harmony-reflect) polyfill, since V8 implements an older version of the `Proxy`

specification. (A previous version of this article had incorrect information about this. Thanks to Mörre and Aaron Powell for correcting my mistakes in the comments.)

So feel free to experiment with proxies! Create a hall of mirrors where there seem to be thousands of copies of every object, all alike, and it’s impossible to debug anything! Now is the time. There’s little danger of your ill-advised proxy code escaping into production… yet.

Proxies were first implemented in 2010, by Andreas Gal, with code reviews by Blake Kaplan. The standard committee then completely redesigned the feature. Eddy Bruel implemented the new spec in 2012.

I implemented `Reflect`

, with code reviews by Jeff Walden. It’ll be in Firefox Nightly starting this weekend—all except `Reflect.enumerate()`

, which is not implemented yet.

Next up, we’ll be talking about the most controversial feature in ES6, and who better to present it than the person who’s implementing it in Firefox? So please join us next week as Mozilla engineer Eric Faust presents ES6 classes in depth.

## 13 comments

simonleungJuly 18th, 2015 at 07:10MörreJuly 19th, 2015 at 03:37Jason OrendorffJuly 29th, 2015 at 16:05Aaron PowellJuly 19th, 2015 at 20:01Jason OrendorffJuly 29th, 2015 at 12:10bystanderJuly 20th, 2015 at 14:43Boris PrpićJuly 20th, 2015 at 17:12karthick sivaJuly 27th, 2015 at 02:02Jason OrendorffJuly 29th, 2015 at 13:22karthick sivaJuly 29th, 2015 at 22:43LukeJuly 28th, 2015 at 20:01Jason OrendorffJuly 29th, 2015 at 12:08simonleungJuly 29th, 2015 at 10:45