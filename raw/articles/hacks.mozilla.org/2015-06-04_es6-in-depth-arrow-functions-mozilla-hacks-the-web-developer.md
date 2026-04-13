---
title: 'ES6 In Depth: Arrow functions – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/06/es6-in-depth-arrow-functions/
author: Jason Orendorff
published: '2015-06-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) is a series on new features being added to the JavaScript programming language in the 6th Edition of the ECMAScript standard, ES6 for short.

Arrows have been part of JavaScript from the very beginning. The first JavaScript tutorials advised wrapping inline scripts in HTML comments. This would prevent browsers that *didn’t* support JS from erroneously displaying your JS code as text. You would write something like this:

```
<script language="javascript">
<!--
document.bgColor = "brown"; // red
// -->
</script>
```


Old browsers would see two unsupported tags and a comment; only new browsers would see JS code.

To support this odd hack, the JavaScript engine in your browser treats the characters `<!--`

as the start of a one-line comment. No joke. This has really been part of the language all along, and it works to this day, not just at the top of an inline `<script>`

but everywhere in JS code. It even works in Node.

As it happens, [this style of comment is standardized for the first time in ES6.](http://people.mozilla.org/~jorendorff/es6-draft.html#sec-html-like-comments) But this isn’t the arrow we’re here to talk about.

The arrow sequence `-->`

also denotes a one-line comment. Weirdly, while in HTML characters *before* the `-->`

are part of the comment, in JS the rest of the line *after* the `-->`

is a comment.

It gets stranger. This arrow indicates a comment *only* when it appears at the start of a line. That’s because in other contexts, `-->`

is an operator in JS, the “goes to” operator!

```
function countdown(n) {
while (n --> 0) // "n goes to zero"
alert(n);
blastoff();
}
```


[This code really works.](http://codepen.io/anon/pen/oXZaBY?editors=001) The loop runs until `n` gets to 0. This too is *not* a new feature in ES6, but a combination of familiar features, with a little misdirection thrown in. Can you figure out what’s going on here? As usual, the answer to the puzzle can be found [on Stack Overflow](http://stackoverflow.com/questions/1642028/what-is-the-name-of-the-operator).

Of course there is also the less-than-or-equal-to operator, `<=`

. Perhaps you can find more arrows in your JS code, Hidden Pictures style, but let’s stop here and observe that *an arrow is missing*.

`<!--` |
single-line comment |
`-->` |
“goes to” operator |
`<=` |
less than or equal to |
`=>` |
??? |

What happened to `=>`

? Today, we find out.

First, let’s talk a bit about functions.

### Function expressions are everywhere

A fun feature of JavaScript is that any time you need a function, you can just type that function right in the middle of running code.

For example, suppose you are trying to tell the browser what to do when the user clicks on a particular button. You start typing:

```
$("#confetti-btn").click(
```


jQuery’s `.click()`

method takes one argument: a function. No problem. You can just type in a function right here:

```
$("#confetti-btn").click(function (event) {
playTrumpet();
fireConfettiCannon();
});
```


Writing code like this comes quite naturally to us now. So it’s strange to recall that before JavaScript popularized this kind of programming, many languages *did not have this feature*. Of course Lisp had function expressions, also called lambda functions, in 1958. But C++, Python, C#, and Java all existed for years without them.

Not anymore. All four have lambdas now. Newer languages universally have lambdas built in. We have JavaScript to thank for this—and early JavaScript programmers who fearlessly built libraries that depended heavily on lambdas, leading to widespread adoption of the feature.

It is just slightly sad, then, that of all the languages I’ve mentioned, JavaScript’s syntax for lambdas has turned out to be the wordiest.

```
// A very simple function in six languages.
function (a) { return a > 0; } // JS
[](int a) { return a > 0; } // C++
(lambda (a) (> a 0)) ;; Lisp
lambda a: a > 0 # Python
a => a > 0 // C#
a -> a > 0 // Java
```


### A new arrow in your quiver

ES6 introduces a new syntax for writing functions.

```
// ES5
var selected = allJobs.filter(<strong>function (job) {
return job.isSelected();
}</strong>);
// ES6
var selected = allJobs.filter(<strong>job => job.isSelected()</strong>);
```


When you just need a simple function with one argument, the new arrow function syntax is simply `<i>Identifier</i> => <i>Expression</i>`

. You get to skip typing `function`

and `return`

, as well as some parentheses, braces, and a semicolon.

(I am personally very grateful for this feature. Not having to type `function`

is important to me, because I inevitably type `functoin`

instead and have to go back and correct it.)

To write a function with multiple arguments (or no arguments, or [rest parameters or defaults](https://hacks.mozilla.org/2015/05/es6-in-depth-rest-parameters-and-defaults/), or a [destructuring](https://hacks.mozilla.org/2015/05/es6-in-depth-destructuring/) argument) you’ll need to add parentheses around the argument list.

```
// ES5
var total = values.reduce(<strong>function (a, b) {
return a + b;
}</strong>, 0);
// ES6
var total = values.reduce(<strong>(a, b) => a + b</strong>, 0);
```


I think it looks pretty nice.

Arrow functions work just as beautifully with functional tools provided by libraries, like [Underscore.js](http://underscorejs.org/) and [Immutable](https://facebook.github.io/immutable-js/). In fact, the examples in [Immutable’s documentation](https://facebook.github.io/immutable-js/docs/#/) are all written in ES6, so many of them already use arrow functions.

What about not-so-functional settings? Arrow functions can contain a block of statements instead of just an expression. Recall our earlier example:

```
// ES5
$("#confetti-btn").click(<strong>function (event)</strong> {
playTrumpet();
fireConfettiCannon();
});
```


Here’s how it will look in ES6:

```
// ES6
$("#confetti-btn").click(<strong>event =></strong> {
playTrumpet();
fireConfettiCannon();
});
```


A minor improvement. The effect on code using [Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) can be more dramatic, as the `}).then(function (result) {`

lines can pile up.

Note that an arrow function with a block body does not automatically return a value. Use a `return`

statement for that.

There is one caveat when using arrow functions to create plain objects. Always wrap the object in parentheses:

```
// create a new empty object for each puppy to play with
var chewToys = puppies.map(puppy => {}); // BUG!
var chewToys = puppies.map(puppy => ({})); // ok
```


Unfortunately, an empty object `{}`

and an empty block `{}`

look exactly the same. The rule in ES6 is that `{`

immediately following an arrow is always treated as the start of a block, never the start of an object. The code `puppy => {}`

is therefore silently interpreted as an arrow function that does nothing and returns `undefined`

.

Even more confusing, an object literal like `{key: value}`

looks exactly like a block containing a labeled statement—at least, that’s how it looks to your JavaScript engine. Fortunately `{`

is the only ambiguous character, so wrapping object literals in parentheses is the only trick you need to remember.

### What’s `this`

?

There is one subtle difference in behavior between ordinary `function`

functions and arrow functions. **Arrow functions do not have their own this value.** The value of

`this`

inside an arrow function is always inherited from the enclosing scope.Before we try and figure out what that means in practice, let’s back up a bit.

How does `this`

work in JavaScript? Where does its value come from? [There’s no short answer.](http://stackoverflow.com/questions/3127429/how-does-the-this-keyword-work) If it seems simple in your head, it’s because you’ve been dealing with it for a long time!

One reason this question comes up so often is that `function`

functions receive a `this`

value automatically, whether they want one or not. Have you ever written this hack?

```
{
...
addAll: function addAll(pieces) {
var self = this;
_.each(pieces, function (piece) {
self.add(piece);
});
},
...
}
```


Here, what you’d *like* to write in the inner function is just `this.add(piece)`

. Unfortunately, the inner function doesn’t inherit the outer function’s `this`

value. Inside the inner function, `this`

will be `window`

or `undefined`

. The temporary variable `self`

serves to smuggle the outer value of `this`

into the inner function. (Another way is to use `.bind(this)`

on the inner function. Neither way is particularly pretty.)

In ES6, `this`

hacks mostly go away if you follow these rules:

- Use non-arrow functions for methods that will be called using the
`object.method()`

syntax. Those are the functions that will receive a*meaningful*`this`

value from their caller. - Use arrow functions for everything else.

```
// ES6
{
...
addAll: function addAll(pieces) {
_.each(pieces, piece => this.add(piece));
},
...
}
```


In the ES6 version, note that the `addAll`

method receives `this`

from its caller. The inner function is an arrow function, so it inherits `this`

from the enclosing scope.

As a bonus, ES6 also provides a shorter way to write methods in object literals! So the code above can be simplified further:

```
// ES6 with method syntax
{
...
addAll(pieces) {
_.each(pieces, piece => this.add(piece));
},
...
}
```


Between methods and arrows, I might never type `functoin`

again. It’s a nice thought.

There’s one more minor difference between arrow and non-arrow functions: arrow functions don’t get their own `arguments`

object, either. Of course, in ES6, you’d probably rather use a rest parameter or default value anyway.

### Using arrows to pierce the dark heart of computer science

We’ve talked about the many practical uses of arrow functions. There’s one more possible use case I’d like to talk about: ES6 arrow functions as a learning tool, to uncover something deep about the nature of computation. Whether that is practical or not, you’ll have to decide for yourself.

In 1936, Alonzo Church and Alan Turing independently developed powerful mathematical models of computation. Turing called his model *a-machines*, but everyone instantly started calling them Turing machines. Church wrote instead about functions. His model was called the [λ-calculus](https://en.wikipedia.org/wiki/Lambda_calculus). (λ is the lowercase Greek letter lambda.) This work was the reason Lisp used the word `LAMBDA`

to denote functions, which is why we call function expressions “lambdas” today.

But what is the λ-calculus? What is “model of computation” supposed to mean?

It’s hard to explain in just a few words, but here is my attempt: the λ-calculus is one of the first programming languages. It was not *designed* to be a programming language—after all, stored-program computers wouldn’t come along for another decade or two—but rather a ruthlessly simple, stripped-down, purely mathematical idea of a language that could express any kind of computation you wished to do. Church wanted this model in order to prove things about computation in general.

And he found that he only needed one thing in his system: *functions.*

Think how extraordinary this claim is. Without objects, without arrays, without numbers, without `if`

statements, `while`

loops, semicolons, assignment, logical operators, or an event loop, it is possible to rebuild every kind of computation JavaScript can do, from scratch, using only functions.

Here is an example of the sort of “program” a mathematician could write, using Church’s λ notation:

```
fix = λf.(λx.f(λv.x(x)(v)))(λx.f(λv.x(x)(v)))
```


The equivalent JavaScript function looks like this:

```
var fix = f => (x => f(v => x(x)(v)))
(x => f(v => x(x)(v)));
```


That is, JavaScript contains an implementation of the λ-calculus that actually runs. *The λ-calculus is in JavaScript.*

The stories of what Alonzo Church and later researchers did with the λ-calculus, and how it has quietly insinuated itself into almost every major programming language, are beyond the scope of this blog post. But if you’re interested in the foundations of computer science, or you’d just like to see how a language with nothing but functions can do things like loops and recursion, you could do worse than to spend some rainy afternoon looking into [Church numerals](https://en.wikipedia.org/wiki/Church_encoding) and [fixed-point combinators](https://en.wikipedia.org/wiki/Fixed-point_combinator#Strict_fixed_point_combinator), and playing with them in your Firefox console or [Scratchpad](https://developer.mozilla.org/en-US/docs/Tools/Scratchpad). With ES6 arrows on top of its other strengths, JavaScript can reasonably claim to be the best language for exploring the λ-calculus.

### When can I use arrows?

ES6 arrow functions were implemented in Firefox by me, back in 2013. Jan de Mooij made them fast. Thanks to Tooru Fujisawa and ziyunfei for patches.

Arrow functions are also implemented in the Microsoft Edge preview release. They’re also available in [Babel](http://babeljs.io/), [Traceur](https://github.com/google/traceur-compiler#what-is-traceur), and [TypeScript](http://www.typescriptlang.org/), in case you’re interested in using them on the Web right now.

Our next topic is one of the stranger features in ES6. We’ll get to see `typeof x`

return a totally new value. We’ll ask: When is a name not a string? We’ll puzzle over the meaning of equality. It’ll be weird. So please join us next week as we look at ES6 symbols in depth.

## 21 comments

Kyle SimpsonJune 4th, 2015 at 17:34Simeon VincentJune 4th, 2015 at 23:31johnJune 12th, 2015 at 09:51BergoJune 23rd, 2015 at 20:31BergiJune 24th, 2015 at 09:59BergiJune 23rd, 2015 at 20:30Blaise KalJune 5th, 2015 at 01:40Julian LambJune 5th, 2015 at 14:26Karthick SivaJune 6th, 2015 at 05:55rbzlJune 7th, 2015 at 04:35Jason OrendorffJune 7th, 2015 at 05:08KeithJune 7th, 2015 at 10:52Jason OrendorffJune 8th, 2015 at 13:08Karthick SivaJune 7th, 2015 at 21:03Mörre NoseshineJune 11th, 2015 at 05:13thinsoldierJune 11th, 2015 at 11:55Mörre NoseshineJune 11th, 2015 at 12:07Kyle SimpsonJune 12th, 2015 at 11:02Mörre NoseshineJune 12th, 2015 at 11:19Jason OrendorffJune 16th, 2015 at 05:10BergiJune 23rd, 2015 at 20:39