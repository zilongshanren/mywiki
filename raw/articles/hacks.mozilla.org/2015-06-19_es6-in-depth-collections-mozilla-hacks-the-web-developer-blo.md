---
title: 'ES6 In Depth: Collections – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/06/es6-in-depth-collections/
author: Jason Orendorff
published: '2015-06-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) is a series on new features being added to the JavaScript programming language in the 6th Edition of the ECMAScript standard, ES6 for short.

Earlier this week, the ES6 specification, officially titled *ECMA-262, 6th Edition, ECMAScript 2015 Language Specification*, cleared the final hurdle and was approved as an Ecma standard. Congratulations to TC39 and everyone who contributed. ES6 is in the books!

Even better news: it will not be six more years before the next update. The standard committee now aims to produce a new edition roughly every 12 months. [Proposals for the 7th Edition](https://github.com/tc39/ecma262) are already in development.

It is appropriate, then, to celebrate this occasion by talking about something I’ve been eager to see in JS for a long time—and which I think still has some room for future improvement!

### Hard cases for coevolution

JS isn’t quite like other programming languages, and sometimes this influences the evolution of the language in surprising ways.

ES6 modules are a good example. Other languages have module systems. Racket has a great one. Python too. When the standard committee decided to add modules to ES6, why didn’t they just copy an existing system?

JS is different, because it runs in web browsers. I/O can take a long time. Therefore JS needs a module system that can support loading code asynchronously. It can’t afford to serially search for modules in multiple directories, either. Copying existing systems was no good. The ES6 module system would need to do some new things.

How this influenced the final design is an interesting story. But we’re not here to talk about modules.

This post is about what the ES6 standard calls “keyed collections”: `Set`

, `Map`

, `WeakSet`

, and `WeakMap`

. These features are, in most respects, just like the [hash tables](https://en.wikipedia.org/wiki/Hash_table) in other languages. But the standard committee made some interesting tradeoffs along the way, because JS is different.

### Why collections?

Anyone familiar with JS knows that there’s already something like a hash table built into the language: objects.

A plain `Object`

, after all, is pretty much nothing but an open-ended collection of key-value pairs. You can get, set, and delete properties, iterate over them—all the things a hash table can do. So why add a new feature at all?

Well, many programs do use plain objects to store key-value pairs, and for programs where this works well, there is no particular reason to switch to `Map`

or `Set`

. Still, there are some well-known issues with using objects this way:

-
Objects being used as lookup tables can’t also have methods, without some risk of collision.

-
Therefore programs must either use

`Object.create(null)`

(rather than plain`{}`

) or exercise care to avoid misinterpreting builtin methods (like`Object.prototype.toString`

) as data. -
Property keys are always strings (or, in ES6, symbols). Objects can’t be keys.

-
There’s no efficient way to ask how many properties an object has.


ES6 adds a new concern: plain objects are not [iterable](https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/), so they will not cooperate with the `for`

–`of`

loop, the `...`

operator, and so on.

Again, there are plenty of programs where none of that really matters, and a plain object will continue to be the right choice. `Map`

and `Set`

are for the other cases.

Because they are designed to avoid collisions between user data and builtin methods, the ES6 collections do *not* expose their data as properties. This means that expressions like `obj.key`

or `obj[key]`

cannot be used to access hash table data. You’ll have to write `map.get(key)`

. Also, hash table entries, unlike properties, are *not* inherited via the prototype chain.

The upside is that, unlike plain `Object`

s, `Map`

and `Set`

do have methods, and more methods can be added, either in the standard or in your own subclasses, without conflict.

### Set

A `Set`

is a collection of values. It’s mutable, so your program can add and remove values as it goes. So far, this is just like an array. But there are as many differences between sets and arrays as there are similarities.

First, unlike an array, a set never contains the same value twice. If you try to add a value to a set that’s already in there, nothing happens.

`<pre>`


> var desserts = new Set("🍪🍦🍧🍩");

> desserts.size

4

> desserts.add("🍪");

Set [ "🍪", "🍦", "🍧", "🍩" ]

> desserts.size

4

</pre>

This example uses strings, but a `Set`

can contain any type of JS value. Just as with strings, adding the same object or number more than once has no added effect.

Second, a `Set`

keeps its data organized to make one particular operation fast: membership testing.

`<pre>`


> // Check whether "zythum" is a word.

> arrayOfWords.indexOf("zythum") !== -1 // slow

true

> setOfWords.has("zythum") // fast

true

</pre>

What you don’t get with a `Set`

is indexing:

`<pre>`


> arrayOfWords[15000]

"anapanapa"

> setOfWords[15000] // sets don't support indexing

undefined

</pre>

Here are all the operations on sets:

-
`new Set`

creates a new, empty set. -
`new Set(iterable)`

makes a new set and fills it with data from[any iterable value](https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/). -
`set.size`

gets the number of values in the set. -
`set.has(value)`

returns`true`

if the set contains the given value. -
`set.add(value)`

adds a value to the set. If the value was already in the set, nothing happens. -
`set.delete(value)`

removes a value from the set. If the value wasn’t in the set, nothing happens. Both`.add()`

and`.delete()`

return the set object itself, so you can chain them. -
`set[Symbol.iterator]()`

returns a new iterator over the values in the set. You won’t normally call this directly, but this method is what makes sets iterable. It means you can write`for (v of set) {...}`

and so on. -
`set.forEach(f)`

is easiest to explain with code. It’s like shorthand for:`<pre>`


for (let value of set)

f(value, value, set);

</pre>This method is analogous to the

`.forEach()`

method on arrays. -
`set.clear()`

removes all values from the set. -
`set.keys()`

,`set.values()`

, and`set.entries()`

return various iterators. These are provided for compatibility with`Map`

, so we’ll talk about them below.

Of all these features, the constructor `new Set(iterable)`

stands out as a powerhouse, because it operates at the level of whole data structures. You can use it to convert an array to a set, eliminating duplicate values with a single line of code. Or, pass it a generator: it will run the generator to completion and collect the yielded values into a set. This constructor is also how you copy an existing `Set`

.

I promised last week to complain about the new collections in ES6. I’ll start here. As nice as `Set`

is, there are some missing methods that would make nice additions to a future standard:

-
Functional helpers that are already present on arrays, like

`.map()`

,`.filter()`

,`.some()`

, and`.every()`

. -
Non-mutating

`set1.union(set2)`

and`set1.intersection(set2)`

. -
Methods that can operate on many values at once:

`set.addAll(iterable)`

,`set.removeAll(iterable)`

, and`set.hasAll(iterable)`

.

The good news is that all of these can be implemented efficiently using the methods provided by ES6.

`Map`


A `Map`

is a collection of key-value pairs. Here’s what `Map`

can do:

-
`new Map`

returns a new, empty map. -
`new Map(pairs)`

creates a new map and fills it with data from an existing collection of`[key, value]`

pairs.`pairs`can be an existing`Map`

object, an array of two-element arrays, a generator that yields two-element arrays, etc. -
`map.size`

gets the number of entries in the map. -
`map.has(key)`

tests whether a key is present (like`key in obj`

). -
`map.get(key)`

gets the value associated with a key, or undefined if there is no such entry (like`obj[key]`

). -
`map.set(key, value)`

adds an entry to the map associating`key`with`value`, overwriting any existing entry with the same key (like`obj[key] = value`

). -
`map.delete(key)`

deletes an entry (like`delete obj[key]`

). -
`map.clear()`

removes all entries from the map. -
`map[Symbol.iterator]()`

returns an iterator over the entries in the map. The iterator represents each entry as a new`[key, value]`

array. -
`map.forEach(f)`

works like this:`<pre>`


for (let [key, value] of map)

f(value, key, map);

</pre>The odd argument order is, again, by analogy to

`Array.prototype.forEach()`

. -
`map.keys()`

returns an iterator over all the keys in the map. -
`map.values()`

returns an iterator over all the values in the map. -
`map.entries()`

returns an iterator over all the entries in the map, just like`map[Symbol.iterator]()`

. In fact, it’s just another name for the same method.

What is there to complain about? Here are some features *not* present in ES6 that I think would be useful:

-
A facility for default values, like Python’s

.`collections.defaultdict`

-
A helper function,

`Map.fromObject(obj)`

, to make it easy to write maps using object-literal syntax.

Again, these features are easy to add.

OK. Remember how I started this article with a bit about how unique concerns about running in the browser affect the design of JS language features? This is where we start to talk about that. I’ve got three examples. Here are the first two.

### JS is different, part 1: Hash tables without hash codes?

There’s one useful feature that the ES6 collection classes do not support at all, as far as I can tell.

Suppose we have a `Set`

of [ URL](https://url.spec.whatwg.org/) objects.

`<pre>`


var urls = new Set;

urls.add(new URL(location.href)); // two URL objects.

urls.add(new URL(location.href)); // are they the same?

alert(urls.size); // 2

</pre>

These two `URL`

s really ought to be considered equal. They have all the same fields. But in JavaScript, these two objects are distinct, and there is no way to overload the language’s notion of equality.

Other languages support this. In Java, Python, and Ruby, individual classes can overload equality. In many Scheme implementations, individual hash tables can be created that use different equality relations. C++ supports both.

However, all of these mechanisms require users to implement custom hashing functions and all expose the system’s default hashing function. The committee chose not to expose hash codes in JS—at least, not yet—due to open questions about interoperability and security, concerns that are not as pressing in other languages.

### JS is different, part 2: Surprise! Predictability!

You would think that deterministic behavior from a computer could hardly be surprising. But people are often surprised when I tell them that `Map`

and `Set`

iteration visits entries in the order they were inserted into the collection. It’s deterministic.

We’re used to certain aspects of hash tables being arbitrary. We’ve learned to accept it. But there are good reasons to try to avoid arbitrariness. As I wrote in 2012:


- There is evidence that some programmers find arbitrary iteration order surprising or confusing at first.
[[1]][[2]][[3]][[4]][[5]][[6]]- Property enumeration order is unspecified in ECMAScript, yet all the major implementations have been forced to converge on insertion order, for compatibility with the Web as it is. There is, therefore, some concern that if TC39 does not specify a deterministic iteration order, “the web will just go and specify it for us”.
[[7]]- Hash table iteration order can expose some bits of object hash codes. This imposes some astonishing security concerns on the hashing function implementer. For example, an object’s address must not be recoverable from the exposed bits of its hash code. (Revealing object addresses to untrusted ECMAScript code, while not exploitable by itself, would be a bad security bug on the Web.)

When all this was being discussed back in February 2012, I [argued in favor of arbitrary iteration order](https://mail.mozilla.org/pipermail/es-discuss/2012-February/020541.html). Then I set out to show by experiment that keeping track insertion order would make a hash table too slow. I wrote a handful of C++ microbenchmarks. [The results surprised me.](https://wiki.mozilla.org/User:Jorend/Deterministic_hash_tables)

And that’s how we ended up with hash tables that track insertion order in JS!

### Strong reasons to use weak collections

[Last week,](https://hacks.mozilla.org/2015/06/es6-in-depth-symbols/) we discussed an example involving a JS animation library. We wanted to store a boolean flag for every DOM object, like this:

`<pre>`


if (element.isMoving) {

smoothAnimations(element);

}

element.isMoving = true;

</pre>

Unfortunately, setting an expando property on a DOM object like this is a bad idea, for reasons discussed in the original post.

That post showed how to solve this problem using symbols. But couldn’t we do the same thing using a `Set`

? It might look like this:

`<pre>`


if (movingSet.has(element)) {

smoothAnimations(element);

}

movingSet.add(element);

</pre>

There is only one drawback: `Map`

and `Set`

objects keep a strong reference to every key and value they contain. This means that if a DOM element is removed from the document and dropped, garbage collection can’t recover that memory until that element is removed from `movingSet`

as well. Libraries typically have mixed success, at best, in imposing complex clean-up-after-yourself requirements on their users. So this could lead to memory leaks.

ES6 offers a surprising fix for this. Make `movingSet`

a `WeakSet`

rather than a `Set`

. Memory leak solved!

This means it is possible to solve this particular problem using either a weak collection or symbols. Which is better? A full discussion of the tradeoffs would, unfortunately, make this post a little too long. If you can use a single symbol across the whole lifetime of the web page, that’s probably fine. If you end up wanting many short-lived symbols, that’s a danger sign: consider using `WeakMap`

s instead to avoid leaking memory.

`WeakMap`

and `WeakSet`


`WeakMap`

and `WeakSet`

are specified to behave exactly like `Map`

and `Set`

, but with a few restrictions:

-
`WeakMap`

supports only`new`

,`.has()`

,`.get()`

,`.set()`

, and`.delete()`

. -
`WeakSet`

supports only`new`

,`.has()`

,`.add()`

, and`.delete()`

. -
The values stored in a

`WeakSet`

and the keys stored in a`WeakMap`

must be objects.

Note that neither type of weak collection is iterable. You can’t get entries out of a weak collection except by asking for them specifically, passing in the key you’re interested in.

These carefully crafted restrictions enable the garbage collector to collect dead objects out of live weak collections. The effect is similar to what you could get with weak references or weak-keyed dictionaries, but ES6 weak collections get the memory management benefits *without exposing the fact that GC happened to scripts.*

### JS is different, part 3: Hiding GC nondeterminism

Behind the scenes, the weak collections are implemented as [ephemeron tables](http://www.jucs.org/jucs_14_21/eliminating_cycles_in_weak/jucs_14_21_3481_3497_barros.pdf).

In short, a `WeakSet`

does not keep a strong reference to the objects it contains. When an object in a `WeakSet`

is collected, it is simply removed from the `WeakSet`

. `WeakMap`

is similar. It does not keep a strong reference to any of its keys. If a key is alive, the associated value is alive.

Why accept these restrictions? Why not just add weak references to JS?

Again, the standard committee has been very reluctant to expose nondeterministic behavior to scripts. Poor cross-browser compatibility is the bane of Web development. Weak references expose implementation details of the underlying garbage collector—the very definition of platform-specific arbitrary behavior. Of course applications shouldn’t depend on platform-specific details, but weak references also make it very hard to know just how much you’re depending on the GC behavior in the browser you’re currently testing. They’re hard to reason about.

By contrast, the ES6 weak collections have a more limited feature set, but that feature set is rock solid. The fact that a key or value has been collected is never observable, so applications can’t end up depending on it, even by accident.

This is one case where a Web-specific concern has led to a surprising design decision that makes JS a better language.

### When can I use collections in my code?

All four collection classes are currently shipping in Firefox, Chrome, Microsoft Edge, and Safari. To support older browsers, use a polyfill, like [es6-collections](https://github.com/WebReflection/es6-collections).

`WeakMap`

was first implemented in Firefox by Andreas Gal, who went on to a stint as Mozilla’s CTO. Tom Schuster implemented `WeakSet`

. I implemented `Map`

and `Set`

. Thanks to Tooru Fujisawa for contributing several patches in this area.

Next week, ES6 In Depth starts a two-week summer break. This series has covered a lot of ground, but some of ES6’s most powerful features are yet to come. So please join us when we return with new content on July 9.

## 11 comments

JordanJune 20th, 2015 at 13:51Jason OrendorffJune 24th, 2015 at 06:51Alexander IvantsovJune 29th, 2015 at 05:00simonleungJune 23rd, 2015 at 20:30verigaisJuly 7th, 2015 at 03:45Igor OvsiannikovJuly 8th, 2015 at 02:50Jason OrendorffJuly 8th, 2015 at 15:11verigaisJuly 10th, 2015 at 08:56Qbe RootJuly 13th, 2015 at 08:45karthick sivaJuly 15th, 2015 at 09:11Jason OrendorffJuly 15th, 2015 at 14:00