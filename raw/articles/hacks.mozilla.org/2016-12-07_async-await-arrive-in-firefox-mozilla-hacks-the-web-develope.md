---
title: Async/Await Arrive in Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/12/asyncawait-arrive-in-firefox/
author: Dan Callahan
published: '2016-12-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The new `async`

and `await`

keywords—which make asynchronous code more concise, obvious, and maintainable—have arrived in Firefox 52. Currently available in the latest [Developer Edition](https://firefox.com/developer) release, Firefox 52 is scheduled for general release in March 2017.

JavaScript owes its excellent single-threaded performance and responsiveness on the web to its pervasively asynchronous design. Unfortunately, that same design gives rise to “callback hell,” where sequential calls to asynchronous functions require deeply nested, hard-to-manage code, as seen in this slightly contrived example using the [localforage](https://localforage.github.io/localForage/) library:

```
function foo(callback) {
localforage.setItem('x', Math.random(), function(err) {
if (err) {
console.error("Something went wrong:", err);
} else {
localforage.getItem('x', function(err, value) {
if (err) {
console.error("Something went wrong:", err);
} else {
console.log("The random number is:", value);
}
if (callback) {
callback();
}
});
}
});
}
foo(function() { console.log("Done!"); });
```


If you glossed over that code, or didn’t immediately understand what it did, *that’s the problem*.

ES2015 began addressing this challenge by standardizing on [Promises](https://developers.google.com/web/fundamentals/getting-started/primers/promises) for chained, asynchronous functions. Since their introduction, Promises have become an integral part of new web standards, including [fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) and [service workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers). They make it possible to rewrite the previous example as:

```
function foo() {
return localforage.setItem('x', Math.random())
.then(() => localforage.getItem('x'))
.then((value) => console.log("The random number is:", value))
.catch((err) => console.error("Something went wrong:", err));
}
foo().then(() => console.log("Done!"));
```


Thanks to Promises, the code doesn’t nest deeper with each successive call, and all of the error handling can be consolidated into a single case at the end of the chain.

Note that in the example above, `foo()`

returns immediately, *before localforage does its work.* Because `foo()`

itself returns a Promise, future callbacks can be scheduled for after it completes with the `.then()`

method.

Semantically, the example above is much more straightforward, but syntactically, there’s still a lot to read and understand. The new `async`

and `await`

keywords are [syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar) on top of Promises to help make Promises more manageable:

```
async function foo() {
try {
await localforage.setItem('x', Math.random());
let value = await localforage.getItem('x');
console.log("The random number is:", value);
} catch (err) {
console.error("Something went wrong:", err);
}
}
foo().then(() => console.log("Done!"));
```


The code above is functionally identical to the previous example, but it is much easier to understand and maintain, since the function body now resembles a common, synchronous function.

Functions marked `async`

always return Promises, and thus calls to `.then()`

work on their return value to schedule callbacks. Expressions prefixed with `await`

effectively pause functions until the expression resolves. If an `await`

ed expression encounters an error, then execution passes to the `catch`

block. If uncaught, the returned Promise settles into a rejected state.

Similarly, instead of handling errors inside `async`

functions, it’s possible to use normal `.catch()`

methods on the return value instead:

```
async function foo() {
await localforage.setItem('x', Math.random());
let value = await localforage.getItem('x');
console.log("The random number is:", value);
}
foo().catch(err => console.error("Something went wrong:", err))
.then(() => console.log("Done!"));
```


For a more practical example, consider a function you might write to unsubscribe a user from [web push notifications](https://hacks.mozilla.org/2016/01/web-push-arrives-in-firefox-44/):

```
function unsubscribe() {
return navigator.serviceWorker.ready
.then(reg => reg.pushManager.getSubscription())
.then(subscription => subscription.unsubscribe())
.then(success => {
if (!success) {
throw "unsubscribe not successful";
}
});
}
```


With `async`

and `await`

, it becomes:

```
async function unsubscribe() {
let reg = await navigator.serviceWorker.ready;
let subscription = await reg.pushManager.getSubscription();
let success = await subscription.unsubscribe();
if (!success) {
throw "unsubscribe not successful";
}
}
```


Both function identically, but the latter example hides the complexities of Promises, and turns asynchronous code into code that reads (and executes) like synchronous code: from top to bottom, waiting for each line of code to fully resolve before moving on to the next line.

Native [cross-browser support](http://caniuse.com/#feat=async-functions) for `async`

and `await`

keywords is still nascent, but you can use them today with the help of a JavaScript transpiler like [Babel](http://babeljs.io/), which can convert `async`

/ `await`

to functionally equivalent, backward-compatible code.

To learn more about the `async`

and `await`

keywords, or Promises in general, check out the following resources:

[MDN: Async functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)[Can I Use: Async functions](http://caniuse.com/#feat=async-functions)[PouchDB: We have a problem with Promises](https://pouchdb.com/2015/05/18/we-have-a-problem-with-promises.html)[Promisees: An interactive Promise visualization](http://bevacqua.github.io/promisees/)by[@ponyfoo.](https://ponyfoo.com/)

Remember, `async`

and `await`

are just helpers for Promises: you can mix and match either syntax, and everything you learn about Promises applies directly to `async`

and `await`

.

*Special thanks to Jamund Ferguson for suggesting improvements to the code samples in this post.*

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 10 comments

CrystalGammaDecember 7th, 2016 at 12:06Dan CallahanDecember 7th, 2016 at 12:23voracityDecember 9th, 2016 at 22:28Dan CallahanDecember 12th, 2016 at 09:13Matt GaleDecember 8th, 2016 at 03:50Dan CallahanDecember 8th, 2016 at 10:23Matt GaleDecember 8th, 2016 at 13:49Mindaugas JDecember 8th, 2016 at 12:13Dan CallahanDecember 8th, 2016 at 15:14AndreiDecember 11th, 2016 at 09:12