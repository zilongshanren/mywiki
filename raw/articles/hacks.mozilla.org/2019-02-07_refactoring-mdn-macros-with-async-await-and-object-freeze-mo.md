---
title: Refactoring MDN macros with async, await, and Object.freeze() – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2019/02/refactoring-mdn-macros-with-async-await-and-object-freeze/
author: David Flanagan
published: '2019-02-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In March of last year, the MDN Engineering team began the experiment of publishing a monthly changelog on Mozilla Hacks. After nine months of [the changelog format](https://hacks.mozilla.org/2018/04/mdn-changelog-for-march-2018/), we’ve decided it’s time to try something that we hope will be of interest to the web development community more broadly, and more fun for us to write. These posts may not be monthly, and they won’t contain the kind of granular detail that you would expect from a changelog. They *will* cover some of the more interesting engineering work we do to manage and grow the MDN Web Docs site. And if you want to know exactly what has changed and who has contributed to MDN, you can always [check](https://github.com/mozilla/kuma) [the](https://github.com/mdn/kumascript) [repos](https://github.com/mdn/browser-compat-data) on GitHub.

In January, we landed a major refactoring of the [KumaScript codebase](https://github.com/mdn/kumascript) and that is going to be the topic of this post because the work included some techniques of interest to JavaScript programmers.

### Modern JavaScript

One of the pleasures of undertaking a big refactor like this is the opportunity to modernize the codebase. JavaScript has matured so much since KumaScript was first written, and I was able to take advantage of this, using [ let](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let) and

[,](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const)

`const`

[classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes),

[arrow functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions),

[,](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...of)

`for...of`

loops[the spread (…) operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax), and

[destructuring assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)in the refactored code. Because KumaScript runs as a Node-based server, I didn’t have to worry about browser compatibility or transpilation: I was free (like a kid in a candy store!) to use all of the latest JavaScript features supported by

[Node 10](https://nodejs.org/en/download/).

### KumaScript and macros

Updating to modern JavaScript was a lot of fun, but it wasn’t reason enough to justify the time spent on the refactor. To understand why my team allowed me to work on this project, you need to understand what KumaScript does and how it works. So bear with me while I explain this context, and then we’ll get back to the most interesting parts of the refactor.

First, you should know that Kuma is the Python-based wiki that powers MDN, and KumaScript is a server that renders macros in MDN documents. If you look at the raw form of an MDN document (such as the [HTML < body> element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/body?raw)) you’ll see lines like this:

```
It must be the second element of an {{HTMLElement("html")}} element.
```


The content within the double curly braces is a macro invocation. In this case, the macro is defined to render a cross-reference link to the MDN documentation for the `html`

element. Using macros like this keeps our links and angle-bracket formatting consistent across the site and makes things simpler for writers.

MDN has been using macros like this since before the Kuma server existed. Before Kuma, we used a commercial wiki product which allowed macros to be defined in a language they called DekiScript. DekiScript was a JavaScript-based templating language with a special API for interacting with the wiki. So when we moved to the Kuma server, our documents were full of macros defined in DekiScript, and we needed to implement our own compatible version, which we called KumaScript.

Since our macros were defined using JavaScript, we couldn’t implement them directly in our Python-based Kuma server, so KumaScript became a separate service, written in Node. This was 7 years ago in early 2012, when Node itself was only on version 0.6. Fortunately, a JavaScript-based templating system known as [EJS](https://ejs.co/) already existed at that time, so the basic tools for creating KumaScript were all in place.

But there was a catch: some of our macros needed to make HTTP requests to fetch data they needed. Consider the `HTMLElement`

macro shown above for instance. That macro renders a link to the MDN documentation for a specified HTML tag. But, it also includes a tooltip (via the `title`

attribute) on the link that includes a quick summary of the element:

That summary has to come from the document being linked to. This means that the implementation of the KumaScript macro needs to fetch the page it is linking to in order to extract some of its content. Furthermore, macros like this are written by technical writers, not software engineers, and so the decision was made (I assume by whoever designed the DekiScript macro system) that things like HTTP fetches would be done with blocking functions that returned synchronously, so that technical writers would not have to deal with nested callbacks.

This was a good design decision, but it made things tricky for KumaScript. Node does not naturally support blocking network operations, and even if it did, the KumaScript server could not just stop responding to incoming requests while it fetched documents for pending requests. The upshot was that KumaScript used the [node-fibers](https://github.com/laverdet/node-fibers) binary extension to Node in order to define methods that blocked while network requests were pending. And in addition, KumaScript adopted the [node-hirelings](https://github.com/lmorchard/node-hirelings) library to manage a pool of child processes. (It was written by the original author of KumaScript for this purpose). This enabled the KumaScript server to continue to handle incoming requests in parallel because it could farm out the possibly-blocking macro rendering calls to a pool of *hireling* child processes.

### Async and await

This fibers+hirelings solution rendered MDN macros for 7 years, but by 2018 it had become obsolete. The original design decision that macro authors should not have to understand asynchronous programming with callbacks (or Promises) is still a good decision. But when Node 8 added support for the new `async`

and `await`

keywords, the fibers extension and hirelings library were no longer necessary.

You can read about [ async functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) and

[on MDN, but the gist is this:](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await)

`await`

expressions- If you declare a function
`async`

, you are indicating that it returns a Promise. And if you return a value that is not a Promise, that value will be wrapped in a resolved Promise before it is returned. - The
`await`

operator makes asynchronous Promises appear to behave synchronously. It allows you to write asynchronous code that is as easy to read and reason about as synchronous code.

As an example, consider this line of code:

```
let response = await fetch(url);
```


In web browsers, the `fetch()`

function starts an HTTP request and returns a Promise object that will resolve to a response object once the HTTP response begins to arrive from the server. Without `await`

, you’d have to call the `.then()`

method of the returned Promise, and pass a callback function to receive the response object. But the magic of `await`

lets us pretend that `fetch()`

actually blocks until the HTTP response is received. There is only one catch:

- You can only use
`await`

within functions that are themselves declared`async`

. Meantime,`await`

doesn’t actually make anything block: the underlying operation is still fundamentally asynchronous, and even if we pretend that it is not, we can only do that within some larger asynchronous operation.

What this all means is that the design goal of protecting KumaScript macro authors from the complexity of callbacks can now be done with Promises and the `await`

keyword. And this is the insight with which I undertook our KumaScript refactor.

As I mentioned above, each of our KumaScript macros is implemented as an EJS template. The EJS library compiles templates to JavaScript functions. And to my delight, the latest version of the library has already been updated with [an option](https://github.com/mde/ejs/blob/master/docs/jsdoc/options.jsdoc#L70) to compile templates to `async`

functions, which means that `await`

is now supported in EJS.

With this new library in place, the refactor was relatively simple. I had to find all the blocking functions available to our macros and convert them to use Promises instead of the node-fibers extension. Then, I was able to do a search-and-replace on our macro files to insert the `await`

keyword before all invocations of these functions. Some of our more complicated macros define their own internal functions, and when those internal functions used `await`

, I had to take the additional step of changing those functions to be `async`

. I did get tripped up by one piece of syntax, however, when I converted an old line of blocking code like this:

```
var title = wiki.getPage(slug).title;
```


To this:

```
let title = await wiki.getPage(slug).title;
```


I didn’t catch the error on that line until I started seeing failures from the macro. In the old KumaScript, `wiki.getPage()`

would block and return the requested data synchronously. In the new KumaScript, `wiki.getPage()`

is declared `async`

which means it returns a Promise. And the code above is trying to access a non-existent `title`

property on that Promise object.

Mechanically inserting an `await`

in front of the invocation does not change that fact because the `await`

operator has lower precedence than the `.`

property access operator. In this case, I needed to add some extra parentheses to wait for the Promise to resolve before accessing the `title`

property:

```
let title = (await wiki.getPage(slug)).title;
```


This relatively small change in our KumaScript code means that we no longer need the fibers extension compiled into our Node binary; it means we don’t need the hirelings package any more; and it means that I was able to remove a bunch of code that handled the complicated details of communication between the main process and the hireling worker processes that were actually rendering macros.

And here’s the kicker: when rendering macros that do not make HTTP requests (or when the HTTP results are cached) *I saw rendering speeds increase by a factor of 25 (not 25% faster–25 times faster!). And at the same time CPU load dropped in half.* In production, the new KumaScript server is measurably faster, but not nearly 25x faster, because, of course, the time required to make asynchronous HTTP requests dominates the time required to synchronously render the template. But achieving a 25x speedup, even if only under controlled conditions, made this refactor a very satisfying experience!

`Object.create()`

and `Object.freeze()`


There is one other piece of this KumaScript refactor that I want to talk about because it highlights some JavaScript techniques that deserve to be better known. As I’ve written above, KumaScript uses [EJS](https://github.com/mde/ejs) templates. When you render an EJS template, you pass in an object that defines the bindings available to the JavaScript code in the template. Above, I described a KumaScript macro that called a function named `wiki.getPage()`

. In order for it to do that, KumaScript has to pass an object to the EJS template rendering function that binds the name `wiki`

to an object that includes a `getPage`

property whose value is the relevant function.

For KumaScript, there are three layers of this global environment that we make available to EJS templates. Most fundamentally, there is the macro API, which includes `wiki.getPage()`

and a number of related functions. All macros rendered by KumaScript share this same API. Above this API layer is an `env`

object that gives macros access to page-specific values such as the language and title of the page within which they appear. When the Kuma server submits an MDN page to the KumaScript server for rendering, there are typically multiple macros to be rendered within the page. But all macros will see the same values for per-page variables like `env.title`

and `env.locale`

. Finally, each individual macro invocation on a page can include arguments, and these are exposed by binding them to variables `$0`

, `$1`

, etc.

So, in order to render macros, KumaScript has to prepare an object that includes bindings for a relatively complex API, a set of page-specific variables, and a set of invocation-specific arguments. When refactoring this code, I had two goals:

- I didn’t want to have to rebuild the entire object for each macro to be rendered.
- I wanted to ensure that macro code could not alter the environment and thereby affect the output of future macros.

I achieved the first goal by using the JavaScript [prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain) and [ Object.create()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create). Rather than defining all three layers of the environment on a single object, I first created an object that defined the fixed macro API and the per-page variables. I reused this object for all macros within a page. When it was time to render an individual macro, I used

`Object.create()`

to create a new object that inherited the API and per-page bindings, and I then added the macro argument bindings to that new object. This meant that there was much less setup work to do for each individual macro to be rendered.But if I was going to reuse the object that defined the API and per-page variables, I had to be very sure that a macro could not alter the environment, because that would mean that a bug in one macro could alter the output of a subsequent macro. Using `Object.create()`

helped a lot with this: if a macro runs a line of code like `wiki = null;`

, that will only affect the environment object created for that one render, not the prototype object that it inherits from, and so the `wiki.getPage()`

function will still be available to the next macro to be rendered. (I should point out that using `Object.create()`

like this can cause some confusion when debugging because an object created this way will look like it is empty even though it has inherited properties.)

This `Object.create()`

technique was not enough, however, because a macro that included the code `wiki.getPage = null;`

would still be able to alter its execution environment and affect the output of subsequent macros. So, I took the extra step of calling [ Object.freeze()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze) on the prototype object (and recursively on the objects it references) before I created objects that inherited from it.

`Object.freeze()`

has been part of JavaScript since 2009, but you may not have ever used it if you are not a library author. It locks down an object, making all of its properties read-only. Additionally it [“seals”](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal) the object, which means that new properties cannot be added and existing properties can not be deleted or configured to make them writable again.

I’ve always found it reassuring to know that `Object.freeze()`

is there if I need it, but I’ve rarely actually needed it. So it was exciting to have a legitimate use for this function. There was one hitch worth mentioning, however: after triumphantly using `Object.freeze()`

, I found that my attempts to stub out macro API methods like `wiki.getPage()`

were failing silently. By locking down the macro execution environment so tightly, I’d locked out my own ability to write tests! The solution was to set a flag when testing and then omit the `Object.freeze()`

step when the flag was set.

If this all sounds intriguing, you can take a look at the [Environment class](https://github.com/mdn/kumascript/blob/master/src/environment.js#L955) in the KumaScript source code.

## About David Flanagan

David is a software engineer on the MDN team at Mozilla, and the author of the book *Javascript: The Definitive Guide*.

## 2 comments

JBFebruary 7th, 2019 at 12:56Steve LeeFebruary 12th, 2019 at 08:46