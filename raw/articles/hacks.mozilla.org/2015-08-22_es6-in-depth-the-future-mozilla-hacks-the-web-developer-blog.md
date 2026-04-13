---
title: 'ES6 In Depth: The Future – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/08/es6-in-depth-the-future/
author: Jason Orendorff
published: '2015-08-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) is a series on new features being added to the JavaScript programming language in the 6th Edition of the ECMAScript standard, ES6 for short.

[Last week’s article on ES6 modules](https://hacks.mozilla.org/2015/08/es6-in-depth-modules/) wrapped up a 4-month survey of the major new features in ES6.

This post covers over a dozen *more* new features that we never got around to talking about at length. Consider it a fun tour of all the closets and oddly-shaped upstairs rooms in this mansion of a language. Maybe a vast underground cavern or two. If you haven’t read the other parts of the series, [take a look](https://hacks.mozilla.org/category/es6-in-depth/); this installment may not be the best place to start!

![(a picture of the Batcave, inexplicably)](../../assets/1268ee467ab7c7fc.png)


![(a picture of the Batcave, inexplicably)](../../assets/1268ee467ab7c7fc.png)

*“On your left, you can see typed arrays…”*

One more quick warning: Many of the features below are not widely implemented yet.

OK. Let’s get started.

### Features you may already be using

ES6 standardizes some features that were previously in other standards, or widely implemented but nonstandard.

-
These were all standardized as part of WebGL, but they’ve been used in many other APIs since then, including Canvas, the Web Audio API, and WebRTC. They’re handy whenever you need to process large volumes of raw binary or numeric data.[Typed arrays](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray),`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer" target="_blank">ArrayBuffer</a>`

, and`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView" target="_blank">DataView</a>`

.For example, if the

`Canvas`

rendering context is missing a feature you want, and if you’re feeling sufficiently hardcore about it, you can just implement it yourself:`<pre>`


var context = canvas.getContext("2d");

var image = context.getImageData(0, 0, canvas.width, canvas.height);

var pixels = image.data; // a Uint8ClampedArray object

// ... Your code here!

// ... Hack on the raw bits in `pixels`

// ... and then write them back to the canvas:

context.putImageData(image, 0, 0);

</pre>During standardization, typed arrays picked up

[methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray)like`.slice()`

,`.map()`

, and`.filter()`

. -
**Promises.**Writing just one paragraph about promises is like eating just one potato chip. Never mind how*hard*it is; it barely even makes sense as a thing to do. What to say? Promises are the building blocks of asynchronous JS programming. They represent values that will become available later. So for example, when you call`<a href="https://developer.mozilla.org/en-US/docs/Web/API/GlobalFetch/fetch" target="_blank">fetch()</a>`

, instead of blocking, it returns a`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise" target="_blank">Promise</a>`

object immediately. The fetch goes on in the background, and it’ll call you back when the response arrives. Promises are better than callbacks alone, because they chain really nicely, they’re first-class values with[interesting](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)[operations](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/race)on them, and you can get error handling right with a lot less boilerplate. They’re polyfillable in the browser. If you don’t already know all about promises, check out[Jake Archibald’s very in-depth article](http://www.html5rocks.com/en/tutorials/es6/promises/). -
**Functions in block scope.**You*shouldn’t*be using this one, but it’s possible you have been. Maybe unintentionally.In ES1-5, this code was technically illegal:

`<pre>`


if (temperature > 100) {

function chill() {

return fan.switchOn().then(obtainLemonade);

}

chill();

}

</pre>That function declaration inside an

`if`

block was supposedly forbidden. They were only legal at toplevel, or inside the outermost block of a function.But it worked in all major browsers anyway. Sort of.

Not compatibly. The details were a little different in each browser. But it sort of worked, and many web pages still use it.

ES6 standardizes this, thank goodness. The function is hoisted to the top of the enclosing block.

Unfortunately, Firefox and Safari don’t implement the new standard yet. So for now, use a function expression instead:

`<pre>`


if (temperature > 100) {

var chill = function () {

return fan.switchOn().then(obtainLemonade);

};

chill();

}

</pre>The only reason block-scoped functions weren’t standardized years ago is that the backward-compatibility constraints were incredibly complicated. Nobody thought they could be solved. ES6 threads the needle by adding a

that only applies in non-strict code. I can’t explain it here. Trust me, use strict mode.*very*strange rule -
**Function names.**All the major JS engines have also long supported a nonstandard`.name`

property on functions that have names. ES6 standardizes this, and makes it better by inferring a sensible`.name`

for some functions that were heretofore considered nameless:`<pre>`


> var lessThan = function (a, b) { return a < b; };

> lessThan.name

"lessThan"

</pre>For other functions, such as callbacks that appear as arguments to

`.then`

methods, the spec still can’t figure out a name.`<var>fn</var>.name`

is then the empty string.

### Nice things

-
A new standard library function, similar to Underscore’s`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign" target="_blank">Object.assign(target, ...sources)</a>`

.`<a href="http://underscorejs.org/#extend" target="_blank">_.extend()</a>`

. -
**The spread operator for function calls.**This is nothing to do with Nutella, even though Nutella is a tasty spread. But it is a delicious feature, and I think you’ll like it.Back in May, we introduced

[rest parameters](https://hacks.mozilla.org/2015/05/es6-in-depth-rest-parameters-and-defaults/). They’re a way for functions to receive any number of arguments, a more civilized alternative to the random, clumsy`arguments`

object.`<pre>`


function log(...stuff) { // stuff is the rest parameter.

var rendered = stuff.map(renderStuff); // It's a real array.

$("#log").add($(rendered));

}

</pre>What we didn’t say is that there’s matching syntax for

*passing*any number of arguments to a function, a more civilized alternative to`fn.apply()`

:`<pre>`


// log all the values from an array

log(...myArray);

</pre>Of course it works with any

[iterable object](https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/), so you can log all the stuff in a`Set`

by writing`log(...mySet)`

.Unlike rest parameters, it makes sense to use the spread operator multiple times in a single argument list:

`<pre>`


// kicks are before trids

log("Kicks:", ...kicks, "Trids:", ...trids);

</pre>The spread operator is handy for flattening an array of arrays:

`<pre>`


> var smallArrays = [[], ["one"], ["two", "twos"]];

> var oneBigArray = [].concat(...smallArrays);

> oneBigArray

["one", "two", "twos"]

</pre>…but maybe this one of those pressing needs that only I have. If so, I blame Haskell.

-
**The spread operator for building arrays.**Also back in May, we talked about[“rest” patterns in destructuring](https://hacks.mozilla.org/2015/05/es6-in-depth-destructuring/). They’re a way to get any number of elements out of an array:`<pre>`


> var [head, ...tail] = [1, 2, 3, 4];

> head

1

> tail

[2, 3, 4]

</pre>Guess what! There’s matching syntax for getting any number of elements

*into*an array:`<pre>`


> var reunited = [head, ...tail];

> reunited

[1, 2, 3, 4]

</pre>This follows all the same rules as the spread operator for function calls: you can use the spread operator many times in the same array, and so on.

-
**Proper tail calls.**This one is too amazing for me to try to explain here.To understand this feature, there’s no better place to start than

[page 1 of](https://mitpress.mit.edu/sicp/full-text/book/book-Z-H-9.html#%_chap_1). If you enjoy it, just keep reading. Tail calls are explained in*Structure and Interpretation of Computer Programs*[section 1.2.1, “Linear Recursion and Iteration”](https://mitpress.mit.edu/sicp/full-text/book/book-Z-H-11.html#%_sec_1.2.1). The ES6 standard requires that implementations be “tail-recursive”, as the term is defined there.None of the major JS engines have implemented this yet. It’s hard to implement. But all in good time.


### Text

-
**Unicode version upgrade.**ES5 required implementations to support at least all the characters in Unicode version 3.0. ES6 implementations must support at least Unicode 5.1.0. You can now use characters from[Linear B](https://en.wikipedia.org/wiki/Linear_B)in your function names![Linear A](../../assets/c583f6d1407525a2.img)is still a bit risky, both because it was not added to Unicode until version 7.0 and because it might be hard to maintain code written in a language that has never been deciphered.(Even in JavaScript engines that support the emoji added in Unicode 6.1, you can’t use 😺 as a variable name. For some reason, the Unicode Consortium decided not to classify it as an identifier character. 😾)

-
**Long Unicode escape sequences.**ES6, like earlier versions, supports four-digit Unicode escape sequences. They look like this:`\u212A`

. These are great. You can use them in strings. Or if you’re feeling playful and your project has no code review policy whatsoever, you can use them in variable names. But then, for a character like U+13021 (

), the Egyptian hieroglyph of a guy standing on his head, there’s a slight problem. The number `13021`

has five digits. Five is more than four.In ES5, you had to write two escapes, a UTF-16

[surrogate pair](https://en.wikipedia.org/wiki/UTF-16#Description). This felt exactly like living in the Dark Ages: cold, miserable, barbaric. ES6, like the dawn of the Italian Renaissance, brings tremendous change: you can now write`\u{13021}`

. -
**Better support for characters outside the BMP.**The`.toUpperCase()`

and`.toLowerCase()`

methods now work on strings written in[the Deseret alphabet](https://en.wikipedia.org/wiki/Deseret_alphabet)!In the same vein,

`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCodePoint" target="_blank">String.fromCodePoint(...codePoints)</a>`

is a function very similar to the older`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCharCode" target="_blank">String.fromCharCode(...codeUnits)</a>`

, but with support for code points beyond the BMP. -
**Unicode RegExps.**ES6 regular expressions support a new flag, the`u`

flag, which causes the regular expression to treat characters outside the BMP as single characters, not as two separate code units. For example, without the`u`

,`/./`

only matches half of the character`"😭"`

. But`/./<strong>u</strong>`

matches the whole thing.Putting the

`u`

flag on a`RegExp`

also enables more Unicode-aware case-insensitive matching and long Unicode escape sequences. For the whole story, see[Mathias Bynens’s very detailed post](https://mathiasbynens.be/notes/es6-unicode-regex). -
**Sticky RegExps.**A non-Unicode-related feature is the`y`

flag, also known as the[sticky flag](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/sticky). A sticky regular expression only looks for matches starting at the exact offset given by its`.lastIndex`

property. If there isn’t a match there, rather than scanning forward in the string to find a match somewhere else, a sticky regexp immediately returns`null`

. -
**An official internationalization spec.**ES6 implementations that provide any internationalization features must support[ECMA-402, the ECMAScript 2015 Internationalization API Specification](http://www.ecma-international.org/publications/standards/Ecma-402.htm). This separate standard specifies[the](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl). Firefox, Chrome, and IE11+ already fully support it. So does Node 0.12.`Intl`

object

### Numbers

-
**Binary and octal number literals.**If you need a fancy way to write the number 8,675,309, and`0x845fed`

isn’t doing it for you, you can now write`0o41057755`

(octal) or`0b100001000101111111101101`

(binary).`Number(str)`

also now recognizes strings in this format:`Number("0b101010")`

returns 42.(Quick reminder:

`<var>number</var>.toString(base)`

and`parseInt(<var>string</var>, base)`

are the original ways to convert numbers to and from arbitrary bases.) -
**New**These are pretty niche. If you’re interested, you can browse the standard yourself, starting at`Number`

functions and constants.`<a href="http://www.ecma-international.org/ecma-262/6.0/index.html#sec-number.epsilon" target="_blank">Number.EPSILON</a>`

.Maybe the most interesting new idea here is the “safe integer” range, from −(2

53– 1) to +(253– 1) inclusive. This special range of numbers has existed as long as JS. Every integer in this range can be represented exactly as a JS number, as can its nearest neighbors. In short, it’s the range where`++`

and`--`

work as expected. Outside this range, odd integers aren’t representable as 64-bit floating-point numbers, so incrementing and decrementing the numbers that*are*representable (all of which are even) can’t give a correct result. In case this matters to your code, the standard now offers constants`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MIN_SAFE_INTEGER" target="_blank">Number.MIN_SAFE_INTEGER</a>`

and`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER" target="_blank">Number.MAX_SAFE_INTEGER</a>`

, and a predicate`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isSafeInteger" target="_blank">Number.isSafeInteger(n)</a>`

. -
**New**ES6 adds`Math`

functions.[hyperbolic](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/asinh)[trig](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/acosh)[functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/atanh)[and](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/asinh)[their](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/acosh)[inverses](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/atanh),`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/cbrt" target="_blank">Math.cbrt(x)</a>`

for computing cube roots,`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/hypot" target="_blank">Math.hypot(x, y)</a>`

for computing the hypotenuse of a right triangle,`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/log2" target="_blank">Math.log2(x)</a>`

and`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/log10" target="_blank">Math.log10(x)</a>`

for computing logarithms in common bases,`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/clz32" target="_blank">Math.clz32(x)</a>`

to help compute integer logarithms, and a few others.`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/sign" target="_blank">Math.sign(x)</a>`

gets the sign of a number.ES6 also adds

`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/imul" target="_blank">Math.imul(x, y)</a>`

, which does signed multiplication modulo 232. This is a very strange thing to want… unless you are working around the fact that JS does not have 64-bit integers or big integers. In that case it’s very handy. This helps compilers. Emscripten uses this function to implement 64-bit integer multiplication in JS.Similarly

`<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/fround" target="_blank">Math.fround(x)</a>`

is handy for compilers that need to support 32-bit floating-point numbers.

### The end

Is this everything?

Well, no. I didn’t even mention the object that’s the [common prototype of all built-in iterators](http://www.ecma-international.org/ecma-262/6.0/index.html#sec-%iteratorprototype%-object), the top-secret [GeneratorFunction constructor](http://www.ecma-international.org/ecma-262/6.0/index.html#sec-generatorfunction-constructor), `<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is" target="_blank">Object.is(v1, v2)</a>`

, how `Symbol.species`

helps support subclassing builtins like [Array](http://www.ecma-international.org/ecma-262/6.0/index.html#sec-arrayspeciescreate) and [Promise](http://www.ecma-international.org/ecma-262/6.0/index.html#sec-promise.prototype.then), or how ES6 specifies details of how [multiple globals](http://www.ecma-international.org/ecma-262/6.0/index.html#sec-code-realms) work that have never been standardized before.

I’m sure I missed a few things, too.

But if you’ve been following along, you have a pretty good picture of where we’re going. You know [you can use ES6 features today](https://hacks.mozilla.org/2015/06/es6-in-depth-babel-and-broccoli/), and if you do, you’ll be opting in to a better language.

A few days ago, [Josh Mock](https://twitter.com/JoshMock) remarked to me that he had just used [eight different ES6 features in about 50 lines of code](https://gist.github.com/JoshMock/98f187c7a8bf745e4cf6), without even really thinking about it. Modules, classes, argument defaults, `Set`

, `Map`

, template strings, arrow functions, and `let`

. (He missed the `for`

–`of`

loop.)

This has been my experience, too. The new features hang together very well. They end up affecting almost every line of JS code you write.

Meanwhile, every JS engine is hurrying to implement and optimize the features we’ve been discussing for the past few months.

Once we’re done, the language will be complete. We’ll never have to change anything again. I’ll have to find something else to work on.

Just kidding. [Proposals for ES7](https://github.com/tc39/ecma262) are already picking up steam. Just to pick a few:

-
[Exponentation operator.](https://github.com/rwaldron/exponentiation-operator)`2 ** 8`

will return 256. Implemented in[Firefox Nightly](https://nightly.mozilla.org/). -
Returns true if this array contains the given value. Implemented in Firefox Nightly; polyfillable.`<a href="https://github.com/tc39/Array.prototype.includes/" target="_blank">Array.prototype.includes(value)</a>`

. -
Exposes 128-bit[SIMD.](https://docs.google.com/presentation/d/1MY9NHrHmL7ma7C8dyNXvmYNNGgVmmxXk8ZIiQtPlfH4/edit?usp=sharing)[SIMD instructions](https://en.wikipedia.org/wiki/SIMD)provided by modern CPUs. These instructions do an arithmetic operation on 2, or 4, or 8 adjacent array elements at a time. They can dramatically speed up a wide variety of algorithms for streaming audio and video, cryptography, games, image processing, and more. Very low-level, very powerful. Implemented in Firefox Nightly; polyfillable. -
We hinted at this feature in the[Async functions.](https://github.com/tc39/ecmascript-asyncawait)[post on generators](https://hacks.mozilla.org/2015/05/es6-in-depth-generators/). Async functions are like generators, but specialized for asynchronous programming. When you call a generator, it returns an iterator. When you call an async function, it returns a promise. Generators use the`yield`

keyword to pause and produce a value; async functions instead use the`await`

keyword to pause and wait for a promise.It’s hard to describe them in a few sentences, but async functions will be the landmark feature in ES7.

-
This is a follow-up to typed arrays. Typed arrays have elements that are typed. A typed object is simply an object whose properties are typed.[Typed Objects.](https://github.com/dslomov/typed-objects-es7)`<pre>`


// Create a new struct type. Every Point has two fields

// named x and y.

var Point = new TypedObject.StructType({

x: TypedObject.int32,

y: TypedObject.int32

});// Now create an instance of that type.


var p = new Point({x: 800, y: 600});

console.log(p.x); // 800

</pre>You would only do this for performance reasons. Like typed arrays, typed objects offer a few of the benefits of typing (compact memory usage and speed), but on a per-object, opt-in basis, in contrast to languages where everything is statically typed.

They’re are also interesting for JS as a compilation target.

Implemented in Firefox Nightly.

-
Decorators are tags you add to a property, class, or method. An example shows what this is about:[Class and property decorators.](https://github.com/wycats/javascript-decorators/blob/master/README.md)`<pre>`


import debug from "jsdebug";class Person {


@debug.logWhenCalled

hasRoundHead(assert) {

return this.head instanceof Spheroid;

}

...

}

</pre>`@debug.logWhenCalled`

is the decorator here. You can imagine what it does to the method.[The proposal](https://github.com/wycats/javascript-decorators/blob/master/README.md)explains how this would work in detail, with many examples.

There’s one more exciting development I have to mention. This one is not a language feature.

TC39, the ECMAScript standard committee, is moving toward more frequent releases and [a more public process](https://tc39.github.io/process-document/). Six years passed between ES5 and ES6. The committee aims to ship ES7 just 12 months after ES6. Subsequent editions of the standard will be released on a 12-month cadence. Some of the features listed above will be ready in time. They will “catch the train” and become part of ES7. Those that aren’t finished in that timeframe can catch the next train.

It’s been great fun sharing the staggering amount of good stuff in ES6. It’s also a pleasure to be able to say that a feature dump of this size will probably never happen again.

Thanks for joining us for ES6 In Depth! I hope you enjoyed it. Keep in touch.

## 6 comments

Johannes BrodwallAugust 22nd, 2015 at 07:12IgorAugust 22nd, 2015 at 16:45LukeAugust 23rd, 2015 at 21:46voracityAugust 23rd, 2015 at 23:45Phil DokasAugust 29th, 2015 at 16:39Rahul gargSeptember 7th, 2015 at 10:58