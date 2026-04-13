---
title: 'ES6 In Depth: Iterators and the for-of loop – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
author: Jason Orendorff
published: '2015-04-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) is a series on new features being added to the JavaScript programming language in the 6th Edition of the ECMAScript standard, ES6 for short.

How do you loop over the elements of an array? When JavaScript was introduced, twenty years ago, you would do it like this:

`<pre>`


for (var index = 0; index < myArray.length; index++) {

console.log(myArray[index]);

}

</pre>

Since ES5, you can use the built-in [ forEach](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach) method:

`<pre>`


myArray.forEach(function (value) {

console.log(value);

});

</pre>

This is a little shorter, but there is one minor drawback: you can’t break out of this loop using a [ break](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/break) statement or return from the enclosing function using a

[statement.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/return)

`return`

It sure would be nice if there were just a `for`

-loop syntax that looped over array elements.

How about a [ for–in](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...in) loop?


`<pre>`


for (var index in myArray) { // don't actually do this

console.log(myArray[index]);

}

</pre>

This is a bad idea for several reasons:

- The values assigned to
`index`

in this code are the strings`"0"`

,`"1"`

,`"2"`

and so on, not actual numbers. Since you probably don’t want string arithmetic (`"2" + 1 == "21"`

), this is inconvenient at best. - The loop body will execute not only for array elements, but also for any other
[expando](https://developer.mozilla.org/en-US/docs/Glossary/Expando)properties someone may have added. For example, if your array has an enumerable property`myArray.name`

, then this loop will execute one extra time, with`index == "name"`

. Even properties on the array’s prototype chain can be visited. - Most astonishing of all, in some circumstances, this code can loop over the array elements in an arbitrary order.

In short, `for`

–`in`

was designed to work on plain old `Object`

s with string keys. For `Array`

s, it’s not so great.

### The mighty for-of loop

Remember last week I promised that ES6 would not break the JS code you’ve already written. Well, millions of Web sites depend on the behavior of `for`

–`in`

—yes, even its behavior on arrays. So there was never any question of “fixing” `for`

–`in`

to be more helpful when used with arrays. The only way for ES6 to improve matters was to add some kind of new loop syntax.

And here it is:

`<pre>`


for (var value of myArray) {

console.log(value);

}

</pre>

Hmm. After all that build-up, it doesn’t seem all that impressive, does it? Well, we’ll see whether [ for–of](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of) has any neat tricks up its sleeve. For now, just note that:


- this is the most concise, direct syntax yet for looping through array elements
- it avoids all the pitfalls of
`for`

–`in`

- unlike
`forEach()`

, it works with`break`

,`continue`

, and`return`


The `for`

–** in** loop is for looping over object properties.

The `for`

–** of** loop is for looping over

*data*—like the values in an array.

But that’s not all.

### Other collections support for-of too

`for`

–`of`

is not just for arrays. It also works on most array-like objects, like DOM [ NodeList](https://developer.mozilla.org/en-US/docs/Web/API/NodeList)s.

It also works on strings, treating the string as a sequence of Unicode characters:

`<pre>`


for (var chr of "😺😲") {

alert(chr);

}

</pre>

It also works on `Map`

and `Set`

objects.

Oh, I’m sorry. You’ve never heard of `Map`

and `Set`

objects? Well, they are new in ES6. We’ll do a whole post about them at some point. If you’ve worked with maps and sets in other languages, there won’t be any big surprises.

For example, a `Set`

object is good for eliminating duplicates:

`<pre>`


// make a set from an array of words

var uniqueWords = new Set(words);

</pre>

Once you’ve got a `Set`

, maybe you’d like to loop over its contents. Easy:

`<pre>`


for (var word of uniqueWords) {

console.log(word);

}

</pre>

A `Map`

is slightly different: the data inside it is made of key-value pairs, so you’ll want to use *destructuring* to unpack the key and value into two separate variables:

`<pre>`


for (var [key, value] of phoneBookMap) {

console.log(key + "'s phone number is: " + value);

}

</pre>

Destructuring is yet another new ES6 feature and a great topic for a future blog post. I should write these down.

By now, you get the picture: JS already has quite a few different collection classes, and even more are on the way. `for`

–`of`

is designed to be the workhorse loop statement you use with all of them.

`for`

–`of`

does *not* work with plain old `Object`

s, but if you want to iterate over an object’s properties you can either use `for`

–`in`

(that’s what it’s for) or the builtin `Object.keys()`

:

`<pre>`


// dump an object's own enumerable properties to the console

for (var key of Object.keys(someObject)) {

console.log(key + ": " + someObject[key]);

}

</pre>

### Under the hood

*“Good artists copy, great artists steal.” —Pablo Picasso*

A running theme in ES6 is that the new features being added to the language didn’t come out of nowhere. Most have been tried and proven useful in other languages.

The `for`

–`of`

loop, for example, resembles similar loop statements in C++, Java, C#, and Python. Like them, it works with several different data structures provided by the language and its standard library. But it’s also an extension point in the language.

Like the `for`

/`foreach`

statements in those other languages, ** for–of works entirely in terms of method calls**. What


`Array`

s, `Map`

s, `Set`

s, and the other objects we talked about all have in common is that they have an iterator method.And there’s another kind of object that can have an iterator method too: *any object you want*.

Just as you can add a `myObject.toString()`

method to any object and suddenly JS knows how to convert that object to a string, you can add the `myObject[Symbol.iterator]()`

method to any object and suddenly JS will know how to loop over that object.

For example, suppose you’re using jQuery, and although you’re very fond of `.each()`

, you would like jQuery objects to work with `for`

–`of`

as well. Here’s how to do that:

`<pre>`


// Since jQuery objects are array-like,

// give them the same iterator method Arrays have

jQuery.prototype[Symbol.iterator] =

Array.prototype[Symbol.iterator];

</pre>

OK, I know what you’re thinking. That `[Symbol.iterator]`

syntax seems weird. What is going on there? It has to do with the method’s name. The standard committee could have just called this method `.iterator()`

, but then, your existing code might already have some objects with `.iterator()`

methods, and that could get pretty confusing. So the standard uses a *symbol*, rather than a string, as the name of this method.

Symbols are new in ES6, and we’ll tell you all about them in—you guessed it—a future blog post. For now, all you need to know is that the standard can define a brand-new symbol, like `Symbol.iterator`

, and it’s guaranteed not to conflict with any existing code. The trade-off is that the syntax is a little weird. But it’s a small price to pay for this versatile new feature and excellent backward compatibility.

An object that has a `[Symbol.iterator]()`

method is called *iterable*. In coming weeks, we’ll see that the concept of iterable objects is used throughout the language, not only in `for`

–`of`

but in the `Map`

and `Set`

constructors, destructuring assignment, and the new spread operator.

### Iterator objects

Now, there is a chance you will never have to implement an iterator object of your own from scratch. We’ll see why next week. But for completeness, let’s look at what an iterator object looks like. (If you skip this whole section, you’ll mainly be missing crunchy technical details.)

A `for`

–`of`

loop starts by calling the `[Symbol.iterator]()`

method on the collection. This returns a new iterator object. An iterator object can be any object with a `.next()`

method; the `for`

–`of`

loop will call this method repeatedly, once each time through the loop. For example, here’s the simplest iterator object I can think of:

`<pre>`


var zeroesForeverIterator = {

[Symbol.iterator]: function () {

return this;

},

next: function () {

return {done: false, value: 0};

}

};

</pre>

Every time this `.next()`

method is called, it returns the same result, telling the `for`

–`of`

loop (a) we’re not done iterating yet; and (b) the next value is `0`

. This means that `for (value of zeroesForeverIterator) {}`

will be an infinite loop. Of course, a typical iterator will not be quite this trivial.

This iterator design, with its `.done`

and `.value`

properties, is superficially different from how iterators work in other languages. In Java, iterators have separate `.hasNext()`

and `.next()`

methods. In Python, they have a single `.next()`

method that throws `StopIteration`

when there are no more values. But all three designs are fundamentally returning the same information.

An iterator object can also implement optional `.return()`

and `.throw(exc)`

methods. The `for`

–`of`

loop calls `.return()`

if the loop exits prematurely, due to an exception or a `break`

or `return`

statement. The iterator can implement `.return()`

if it needs to do some cleanup or free up resources it was using. Most iterator objects won’t need to implement it. `.throw(exc)`

is even more of a special case: `for`

–`of`

never calls it at all. But we’ll hear more about it next week.

Now that we have all the details, we can take a simple `for`

–`of`

loop and rewrite it in terms of the underlying method calls.

First the `for`

–`of`

loop:

`<pre>`


for (VAR of ITERABLE) {

STATEMENTS

}

</pre>

Here is a rough equivalent, using the underlying methods and a few temporary variables:

`<pre>`


var $iterator = ITERABLE[Symbol.iterator]();

var $result = $iterator.next();

while (!$result.done) {

VAR = $result.value;

STATEMENTS

$result = $iterator.next();

}

</pre>

This code doesn’t show how `.return()`

is handled. We could add that, but I think it would obscure what’s going on rather than illuminate it. `for`

–`of`

is easy to use, but there is a lot going on behind the scenes.

### When can I start using this?

The `for`

–`of`

loop is supported in all current Firefox releases. It’s supported in Chrome if you go to `chrome://flags`

and enable “Experimental JavaScript”. It also works in Microsoft’s Spartan browser, but not in shipping versions of IE. If you’d like to use this new syntax on the web, but you need to support IE and Safari, you can use a compiler like [Babel](http://babeljs.io/) or Google’s [Traceur](https://github.com/google/traceur-compiler#what-is-traceur) to translate your ES6 code to Web-friendly ES5.

On the server, you don’t need a compiler—you can start using `for`

–`of`

in io.js (and Node, with the `--harmony`

option) today.

(**UPDATE:** This previously neglected to mention that `for`

–`of`

is disabled by default in Chrome. Thanks to Oleg for pointing out the mistake in the comments.)

`{done: true}`


Whew!

Well, we’re done for today, but we’re *still* not done with the `for`

–`of`

loop.

There is one more new kind of object in ES6 that works beautifully with `for`

–`of`

. I didn’t mention it because it’s the topic of next week’s post. I think this new feature is the most magical thing in ES6. If you haven’t already encountered it in languages like Python and C#, you’ll probably find it mind-boggling at first. But it’s the easiest way to write an iterator, it’s useful in refactoring, and it might just change the way we write asynchronous code, both in the browser and on the server. So join us next week as we look at ES6 generators in depth.

## 26 comments

Brett ZamirApril 30th, 2015 at 17:31Jason OrendorffMay 1st, 2015 at 08:31LukeApril 30th, 2015 at 20:12Šime VidasApril 30th, 2015 at 20:53ziyunfeiMay 1st, 2015 at 00:46Andrea GiammarchiMay 1st, 2015 at 07:17Andrea GiammarchiMay 1st, 2015 at 07:22Daniel HermanMay 1st, 2015 at 08:47IgorMay 1st, 2015 at 11:15Jason OrendorffMay 1st, 2015 at 14:16Ken ArnoldMay 1st, 2015 at 18:18VladMay 1st, 2015 at 22:32Jason OrendorffMay 3rd, 2015 at 08:54Jason OrendorffMay 3rd, 2015 at 09:03SivaMay 4th, 2015 at 01:29Jason OrendorffMay 4th, 2015 at 12:01Nick FitzgeraldMay 14th, 2015 at 05:43Martin RinehartMay 3rd, 2015 at 11:13Jason OrendorffMay 4th, 2015 at 12:53Phil StrickerMay 5th, 2015 at 18:24FedgeMay 6th, 2015 at 14:15OlegMay 7th, 2015 at 00:00Jason OrendorffMay 7th, 2015 at 08:46subzeyMay 13th, 2015 at 13:49Jason OrendorffMay 13th, 2015 at 13:57subzeyMay 13th, 2015 at 14:03