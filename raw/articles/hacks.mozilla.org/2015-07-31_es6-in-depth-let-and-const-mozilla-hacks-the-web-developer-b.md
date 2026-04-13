---
title: 'ES6 In Depth: let and const – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/07/es6-in-depth-let-and-const/
author: Jason Orendorff
published: '2015-07-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/) is a series on new features being added to the JavaScript programming language in the 6th Edition of the ECMAScript standard, ES6 for short.

The feature I’d like to talk about today is at once humble and startlingly ambitious.

When Brendan Eich designed the first version of JavaScript back in 1995, he got plenty of things wrong, including things that have been part of the language ever since, like the `Date`

object and objects automatically converting to `NaN`

when you accidentally multiply them. However, the things he got right are stunningly important things, in hindsight: objects; prototypes; first-class functions with lexical scoping; mutability by default. The language has good bones. It was better than anyone realized at first.

Still, Brendan made one particular design decision that bears on today’s article—a decision that I think can be fairly characterized as a mistake. It’s a little thing. A subtle thing. You might use the language for years and not even notice it. But it matters, because this mistake is in the side of the language that we now think of as “the good parts”.

It has to do with variables.

### Problem #1: Blocks are not scopes

The rule sounds so innocent: **The scope of a var declared in a JS function is the whole body of that function.** But there are two ways this can have groan-inducing consequences.


One is that the scope of variables declared in blocks is not just the block. It’s the entire function.

You may never have noticed this before. I’m afraid it’s one of those things you won’t be able to un-see. Let’s walk through a scenario where it leads to a tricky bug.

Say you have some existing code that uses a variable named `t`:

`<pre>`


function runTowerExperiment(tower, startTime) {

var t = startTime;

tower.on("tick", function () {

... code that uses t ...

});

... more code ...

}

</pre>

Everything works great, so far. Now you want to add bowling ball speed measurements, so you add a little `if`

-statement to the inner callback function.

`<pre>`


function runTowerExperiment(tower, startTime) {

var t = startTime;

tower.on("tick", function () {

... code that uses t ...

if (bowlingBall.altitude() <= 0) {

var t = readTachymeter();

...

}

});

... more code ...

}

</pre>

Oh, dear. You’ve unwittingly added a second variable named `t`. Now, in the “code that uses `t`”, which was working fine before, `t`

refers to the new inner variable `t` rather than the existing outer variable.

The scope of a `var`

in JavaScript is like the bucket-of-paint tool in Photoshop. It extends in both directions from the declaration, forwards and backwards, and it just keeps going until it reaches a function boundary. Since this variable `t`’s scope extends so far backwards, it has to be created as soon as we enter the function. This is called hoisting. I like to imagine the JS engine lifting each `var`

and `function`

to the top of the enclosing function with a tiny code crane.

Now, hoisting has its good points. Without it, lots of perfectly cromulent techniques that work fine in the global scope wouldn’t work inside an [IIFE](https://en.wikipedia.org/wiki/Immediately-invoked_function_expression). But in this case, hoisting is causing a nasty bug: all your calculations using `t` will start producing `NaN`

. It’ll be hard to track down, too, especially if your code is larger than this toy example.

Adding a new block of code caused a mysterious error in code *before* that block. Is it just me, or is that really weird? We don’t expect effects to precede causes.

But this is a piece of cake compared to the *second* `var`

problem.

### Problem #2: Variable oversharing in loops

You can guess what happens when you run this code. It’s totally straightforward:

`<pre>`


var messages = ["Hi!", "I'm a web page!", "alert() is fun!"];

for (var i = 0; i < messages.length; i++) {

alert(messages[i]);

}

</pre>

If you’ve been following [this series](https://hacks.mozilla.org/category/es6-in-depth/), you know I like to use `alert()`

for example code. Maybe you also know that `alert()`

is a terrible API. It’s synchronous. So while an alert is visible, input events are not delivered. Your JS code—and in fact your whole UI—is basically paused until the user clicks OK.

All of which makes `alert()`

the wrong choice for almost anything you want to do in a web page. I use it because I think all those same things make `alert()`

a great teaching tool.

Still, I could be persuaded to give up all that clunkiness and bad behavior… if it means I can make a talking cat.

`<pre>`


var messages = ["Meow!", "I'm a talking cat!", "Callbacks are fun!"];

for (var i = 0; i < messages.length; i++) {

setTimeout(function () {

cat.say(messages[i]);

}, i * 1500);

}

</pre>

But something’s wrong. Instead of saying all three messages in order, the cat says “undefined” three times.

Can you spot the bug?

![(Photo of a caterpillar well camouflaged on the bark of a tree. Gujarat, India.)](../../assets/e520479bfdafbb0a.jpg)


![(Photo of a caterpillar well camouflaged on the bark of a tree. Gujarat, India.)](https://hacks.mozilla.org/wp-content/uploads/2015/07/7994751456_e8d2019876_o.jpg)

[nevil saveri](https://www.flickr.com/photos/nevilzaveri/7994751456/)

The problem here is that there is only one variable `i`. It’s shared by the loop itself and all three timeout callbacks. When the loop finishes running, the value of `i` is 3 (because `messages.length`

is 3), and none of the callbacks have been called yet.

So when the first timeout fires, and calls `cat.say(messages[i])`

, it’s using `messages[3]`

. Which of course is `undefined`

.

There are many ways to fix this ([here’s one](http://jsfiddle.net/sybn4h33/3/)), but this is a second problem caused by the `var`

scoping rules. It would be awfully nice never to have this kind of problem in the first place.

`let`

is the new `var`


For the most part, design mistakes in JavaScript (other programming languages too, but *especially* JavaScript) can’t be fixed. Backwards compatibility means never changing the behavior of existing JS code on the Web. Even the standard committee has no power to, say, fix the weird quirks in JavaScript’s automatic semicolon insertion. Browser makers simply will not implement breaking changes, because that kind of change punishes their users.

So about ten years ago, when Brendan Eich decided to fix this problem, there was really only one way to do it.

He added a new keyword, `let`

, that could be used to declare variables, just like `var`

, but with better scoping rules.

It looks like this:

`<pre>`


let t = readTachymeter();

</pre>

Or this:

`<pre>`


for (let i = 0; i < messages.length; i++) {

...

}

</pre>

`let`

and `var`

are different, so if you just do a global search-and-replace throughout your code, that could break parts of your code that (probably unintentionally) depend on the quirks of `var`

. But for the most part, in new ES6 code, you should just stop using `var`

and use `let`

everywhere instead. Hence the slogan: “`let`

is the new `var`

”.

What exactly are the differences between `let`

and `var`

? Glad you asked!

-
The scope of a variable declared with`let`

variables are block-scoped.`let`

is just the enclosing block, not the whole enclosing function.There’s still hoisting with

`let`

, but it’s not as indiscriminate. The`runTowerExperiment`

example can be fixed simply by changing`var`

to`let`

. If you use`let`

everywhere, you will never have that kind of bug. -
**Global**That is, you won’t access them by writing`let`

variables are not properties on the global object.`window.variableName`

. Instead, they live in the scope of an invisible block that notionally encloses all JS code that runs in a web page. -
**Loops of the form**`for (let x...)`

create a fresh binding for`x`in each iteration.This is a very subtle difference. It means that if a

`for (let...)`

loop executes multiple times, and that loop contains a closure, as in our talking cat example, each closure will capture a different copy of the loop variable, rather than all closures capturing the same loop variable.So the talking cat example, too, can be fixed just by changing

`var`

to`let`

.This applies to all three kinds of

`for`

loop:,`for`

–`of`

`for`

–`in`

, and the old-school C kind with semicolons. -
**It’s an error to try to use a**The variable is uninitialized until control flow reaches the line of code where it’s declared. For example:`let`

variable before its declaration is reached.`<pre>`


function update() {

console.log("current time:", t); // ReferenceError

...

let t = readTachymeter();

}

</pre>This rule is there to help you catch bugs. Instead of

`NaN`

results, you’ll get an exception on the line of code where the problem is.This period when the variable is in scope, but uninitialized, is called the temporal dead zone. I keep waiting for this inspired bit of jargon to make the leap to science fiction. Nothing yet.

(Crunchy performance details: In most cases, you can tell whether the declaration has run or not just by looking at the code, so the JavaScript engine does not actually need to perform an extra check every time the variable is accessed to make sure it’s been initialized. However, inside a closure, it sometimes isn’t clear. In those cases the JavaScript engine will do a run-time check. That means

`let`

can be a touch slower than`var`

.)(Crunchy alternate-universe scoping details: In some programming languages, the scope of a variable starts at the point of the declaration, instead of reaching backwards to cover the whole enclosing block. The standard committee considered using that kind of scoping rule for

`let`

. That way, the use of`t`

that causes a ReferenceError here simply wouldn’t be in the scope of the later`let t`

, so it wouldn’t refer to that variable at all. It could refer to a`t`in an enclosing scope. But this approach did not work well with closures or with function hoisting, so it was eventually abandoned.) -
**Redeclaring a variable with**`let`

is a`SyntaxError`

.This rule, too, is there to help you detect trivial mistakes. Still, this is the difference that is most likely to cause you some issues if you attempt a global

`let`

-to-`var`

conversion, because it applies even to global`let`

variables.If you have several scripts that all declare the same global variable, you’d better keep using

`var`

for that. If you switch to`let`

, whichever script loads second will fail with an error.Or use ES6 modules. But that’s a story for another day.


(Crunchy syntax details: `let`

is a reserved word in strict mode code. In non-strict-mode code, for the sake of backward compatibility, you can still declare variables, functions, and arguments named `let`

—you can write `var let = 'q';`

! Not that you would do that. And `let let;`

is not allowed at all.)

Apart from those differences, `let`

and `var`

are pretty much the same. They both support declaring multiple variables separated by commas, for example, and they both support [destructuring](https://hacks.mozilla.org/2015/05/es6-in-depth-destructuring/).

Note that `class`

declarations behave like `let`

, not `var`

. If you load a script containing a `class`

multiple times, the second time you’ll get an error for redeclaring the class.

`const`


Right, one more thing!

ES6 also introduces a third keyword that you can use alongside `let`

: `const`

.

Variables declared with `const`

are just like `let`

except that you can’t assign to them, except at the point where they’re declared. It’s a `SyntaxError`

.

`<pre>`


const MAX_CAT_SIZE_KG = 3000; // 🙀

MAX_CAT_SIZE_KG = 5000; // SyntaxError

MAX_CAT_SIZE_KG++; // nice try, but still a SyntaxError

</pre>

Sensibly enough, you can’t declare a `const`

without giving it a value.

`<pre>`


const theFairest; // SyntaxError, you troublemaker

</pre>

### Secret agent namespace

*“Namespaces are one honking great idea—let’s do more of those!” —Tim Peters, “The Zen of Python”*

Behind the scenes, nested scopes are one of the core concepts that programming languages are built around. It’s been this way since what, [ALGOL](https://en.wikipedia.org/wiki/ALGOL)? Something like 57 years. And it’s truer today than ever.

Before ES3, JavaScript only had global scopes and function scopes. (Let’s ignore `with`

statements.) ES3 introduced `try`

–`catch`

statements, which meant adding a new kind of scope, used only for the exception variable in `catch`

blocks. ES5 added a scope used by strict `eval()`

. ES6 adds block scopes, for-loop scopes, the new global `let`

scope, module scopes, and additional scopes that are used when evaluating default values for arguments.

All the extra scopes added from ES3 onward are necessary to make JavaScript’s procedural and object-oriented features work as smoothly, precisely, and intuitively as closures—and cooperate seamlessly *with* closures. Maybe you never noticed any of these scoping rules before today. If so, the language is doing its job.

### Can I use `let`

and `const`

now?

Yes. To use them on the web, you’ll have to use an ES6 compiler such as [Babel](http://babeljs.io/), [Traceur](https://github.com/google/traceur-compiler#what-is-traceur), or [TypeScript](http://www.typescriptlang.org/). (Babel and Traceur do not support the temporal dead zone yet.)

io.js supports `let`

and `const`

, but only in strict-mode code. Node.js support is the same, but the `--harmony`

option is also required.

Brendan Eich implemented the first version of `let`

in Firefox [nine years ago](https://developer.mozilla.org/en-US/docs/Web/JavaScript/New_in_JavaScript/1.7). The feature was thoroughly redesigned during the standardization process. Shu-yu Guo is upgrading our implementation to match the standard, with code reviews by Jeff Walden and others.

Well, we’re in the home stretch. The end of our epic tour of ES6 features is in sight. In two weeks, we’ll finish up with what’s probably the most eagerly awaited ES6 feature of them all. But first, next week we’ll have a post that `extends`

our earlier coverage of a `new`

feature that’s just `super`

. So please join us as Eric Faust returns with a look at ES6 subclassing in depth.

## 9 comments

RalphJuly 31st, 2015 at 12:40Jason OrendorffJuly 31st, 2015 at 13:20BehrangAugust 1st, 2015 at 00:49PhistucKAugust 1st, 2015 at 03:38simonleungAugust 1st, 2015 at 05:22TomyAugust 6th, 2015 at 05:16Jason OrendorffAugust 6th, 2015 at 08:19Owen DensmoreAugust 9th, 2015 at 11:02Jason OrendorffAugust 10th, 2015 at 09:31