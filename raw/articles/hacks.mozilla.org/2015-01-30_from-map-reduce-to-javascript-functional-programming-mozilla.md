---
title: From Map/Reduce to JavaScript Functional Programming – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2015/01/from-mapreduce-to-javascript-functional-programming/
author: Greg Weng
published: '2015-01-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Since ECMAScript 5.1, `Array.prototype.map`

& `Array.prototype.reduce`

were introduced to major browsers. These two functions not only allow developers to describe a computation more clearly, but also to simplify the work of writing loops for traversing an array; especially when the looping code actually is for **mapping** the array to a new array, or for the accumulation, checksum, and other similar **reducing** operations.


## Map/Reduce

**Map** actually means to compute things with the original array without doing *structural changes* to the output. For example, when `map`

receives an array, you can make sure the output will be another array, and the only difference is that the elements inside it may be transformed from the original value/type to another value/type. So we can say the `doMap`

function from the above example comes with the following **type signature**:

![doMap signature](../../assets/06c18b96a2e4d287.png)


The signature reveals that `[Number]`

means this is an array of numbers. So we now can read the signature as:


`doMap`

is a function, which would turn an array of numbers to an array of booleans

On the other hand, the **reducing** operation means we may change the structure of the input data type to a new one. For example, the signature of the `doReduce`

is:

![doReduce signature](../../assets/d9e89777723c34f7.png)


Here, the `Array`

of `[Number]`

is gone. So we can see the major difference between `map`

and `reduce`

1.

## Functional Programming

In fact, the concepts of `map`

and `reduce`

are older even than JavaScript and are widely used in other functional programming languages, such as Lisp or Haskell 2. This observation is noted in the famous article ‘JavaScript: The World’s Most Misunderstood Programming Language’ by Douglas Crockford

:

[3](https://hacks.mozilla.org#cite-ref-3)JavaScript’s C-like syntax, including curly braces and the clunky for statement, makes it appear to be an ordinary procedural language.

This is misleading because JavaScript has more in common with functional languages like Lisp or Scheme than with C or Java.

This is one reason why JavaScript can do some functional-like things which other orthogonal OOP languages can’t or won’t do. For example, before Java 8 [4](https://hacks.mozilla.org#cite-ref-4) 5, if we wanted to do some ‘callback’ things common in JavaScript, we’d need to create a redundant ‘anonymous class.’:

```
Button button =
(Button) findViewById(R.id.button);
button.setOnClickListener(
new OnClickListener() {
public void onClick(View v) {
// do something
}
}
);
```

Of course, using anonymous callbacks or not in JavaScript is always controversial. We may encounter *callback hell* especially when the component keeps growing. However, first-class functions can do lots of things beyond the callback. In Haskell, we can organize our whole GUI program similar to the Quake-like games 6 with only functions

. That is, we can even make it without the

[7](https://hacks.mozilla.org#cite-ref-7)*classes*,

*methods*,

*inheritance*,

*templates*and other stuff

people usually expect to have when a program needs to be constructed.

[8](https://hacks.mozilla.org#cite-ref-8)![Frag](../../assets/2a2b722a37a2781f.png)


*Frag, the Quake-like game in Haskell*

Therefore, in the JavaScript world, it’s possible to follow similar patterns to construct our programs, rather than hurriedly implementing our own ‘class’ and ‘class system,’ as programmers often do when starting on a problem 9. Adding some

**functional flavor**in JavaScript is not so bad after all, especially when features like

`map`

and `reduce`

are supported by native APIs. To adopt this approach also means we can write more concise codeby combining features instead of redefining them. The only limitation is the language itself is still not functional enough, so we may run into trouble if we play too many tricks, although this should be solvable with the right library

[10](https://hacks.mozilla.org#cite-ref-10).

[11](https://hacks.mozilla.org#cite-ref-11)`map`

and `reduce`

receive other functions as arguments and output them as results. This is important because in this way they present the basic idea of composing computations in the functional world, and are able to glue small pieces together with flexibility and scalability. For example, let’s take a look at the signature of our `map`

expression mentioned above:

![map signature](../../assets/5c8672dc4b2aa94c.png)


You’ll notice that the second argument indicates a function with type `Number -> Boolean`

. In fact, you can give it any function with `a -> b`

type. This may not be so odd in the world of JavaScript — we write tons of callbacks in our daily work. However, the point is that higher-order functions are functions as well. They can be composed into larger ones till we generate the complete program with only first-class functions and some powerful high-order functions like `id`

, `reduce`

, `curry`

, `uncurry`

, `arrow`

and `bind`

12.

## Map/Reduce in Practice

Since we may encounter language limitations, we can’t write our JavaScript code in fully functional style; however, we can *borrow* the idea of types and composition to do lots of things. For example, when you think in types, you will find that `map`

is not only for data handling:

![map & fold signatures](../../assets/47146b9784266e3b.png)


This is what the type signatures for map and reduce would look like in Haskell. We can substitute the `a`

and `b`

with *anything*. So, what if `a`

becomes `SQL`

and `b`

becomes `IO x `

? Remember, we’re thinking in type, and `IO x`

is nothing more than an ordinary type like `Int`

or `URL`

:

```
-- Let's construct queries from SQL statements.
makeQueries strs = map str prepare conn str
doQuery qrys = foldl (results query results >> query) (return ()) qrys
-- Do query and get results.
let stmts = [ "INSERT INTO Articles ('Functional JavaScript')"
, "INSERT INTO Gecko VALUES ('30.a1')"
, "DELETE FROM Articles WHERE version='deprecated'"
]
main = execute (doQuery (makeQuery stmts))`
```

(Note: This is a simplified Haskell example for demo only. It can’t actually be executed.)

The example creates a `makeQueries`

function with `map`

, which will turn the `SQL`

into `IO ()`

13; this also means we generate several actions which can be performed.

![makeQueries signature](../../assets/ef0c65d32a37410c.png)


And then, the `doQuery`

function, which is actually a reducing operation, will execute the queries:

![doQueries signature](../../assets/0a4ab2ab2e9e5674.png)


Note its reducing operation performs IO action with the help of the `bind`

function (`>>`

) of the specific Monad. This topic is not covered in this article, but readers should imagine this as a way to compose functions to execute them step by step, just as a Promise does 24.

The technique is useful not only in Haskell but also in JavaScript. We can use this idea with Promises and ES6 arrow functions to organize a similar computation:

```
// Use a Promise-based library to do IO.
var http = require("q-io/http")
,noop = new Promise(()=>{})
,prepare =
(str)=> http.read('http://www.example.com/' + str)
.then((res)=> res.body.toString())
// the 'then' is equal to the '>>'
,makeQuery =
(strs)=> strs.map((str)=> prepare(str))
,doQuery =
(qrys)=> qrys.reduce((results, qry)=> results.then(qry), noop)
,stmts = [ "articles/FunctionalJavaScript"
, "blob/c745ef73-ece9-46da-8f66-ebes574789b1"
, "books/language/Haskell"
]
,main = doQuery(makeQuery(stmts));
```

(NOTE: In Node.js, the similar querying code with map/reduce and Promise would not run like the Haskell version, since we need Lazy Promise 14 and Lazy Evaluation

)

[15](https://hacks.mozilla.org#cite-ref-15)We’re very close to what we want: define computations with functions, and then combine them to perform it later, although the idea of ‘later’ is not actually true since we don’t have real lazy evaluation in JavaScript. This can be accomplished if we play the trick of keeping an undone Promise — a `resolve`

function which is only resolved when we want to do so. However, even this is tricky, and there are still some unsolvable issues.

Another thing to note is that our program doesn’t need variable variables, but some computation results are transformed and forwarded at every step of our program. In fact, this is just one reason why functional languages can stay pure, and thus they can benefit from the optimization and getting rid of unexpected side-effects [16](https://hacks.mozilla.org#cite-ref-16) 17.

## More on Functional Programming

Map/reduce are the most common functional features in JavaScript. With other not-so-functional features like Promise, we can use tricks like Monad-style computation control, or we can easily define curried functions with ES6’s fat-arrow functions 18 and so on. Also, there are some excellent libraries which provide nice functional features


[19](https://hacks.mozilla.org#cite-ref-19)

[20](https://hacks.mozilla.org#cite-ref-20), and some Domain Specific Languages (DSLs) are even born with functional spirit

[21](https://hacks.mozilla.org#cite-ref-21)

[22](https://hacks.mozilla.org#cite-ref-22). Of course, the best way to understand functional programming is to learn a language designed for it, like Haskell, ML or OCaml. Scala, F#, and Erlang are good choices, too.

[23](https://hacks.mozilla.org#cite-ref-23)1. In fact, `map`

can be implemented with `reduce`

. The most basic operation for structure like this is `reduce`

.

[https://github.com/timoxley/functional-javascript-workshop/blob/440da6737f34b4550301ba3a77b2e4b7721e99fd/problems/implement_map_with_reduce/solution.js#L11](https://github.com/timoxley/functional-javascript-workshop/blob/440da6737f34b4550301ba3a77b2e4b7721e99fd/problems/implement_map_with_reduce/solution.js#L11) [↩](https://hacks.mozilla.org#ref-1)

2. [http://en.wikipedia.org/wiki/Lisp_(programming_language)#Control_structures](http://en.wikipedia.org/wiki/Lisp_(programming_language)#Control_structures) [↩](https://hacks.mozilla.org#ref-2)

3. [http://javascript.crockford.com/javascript.html](http://javascript.crockford.com/javascript.html) [↩](https://hacks.mozilla.org#ref-3)

4. Java 8 now includes the lambda function: [https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html](https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html) [↩](https://hacks.mozilla.org#ref-4)

5. C++ traditionally has not been a functional language, but C++11 introduces lambda functions: [http://en.wikipedia.org/wiki/C%2B%2B11#Lambda_functions_and_expressions](http://en.wikipedia.org/wiki/C%2B%2B11#Lambda_functions_and_expressions) [↩](https://hacks.mozilla.org#ref-5)

6. [https://www.haskell.org/haskellwiki/Frag](https://www.haskell.org/haskellwiki/Frag) [↩](https://hacks.mozilla.org#ref-6)

7. Haskell can represent data structure in function sense, even though declaring a function and a data type are still not the same thing: [http://book.realworldhaskell.org/read/data-structures.html](http://book.realworldhaskell.org/read/data-structures.html) [↩](https://hacks.mozilla.org#ref-7)

8. Yes, I’m cheating: we have Typeclass, Functor, `instance`

and type variable in Haskell. [↩](https://hacks.mozilla.org#ref-8)

9. For those who can’t live without classes, ES6 is in your future: [http://wiki.ecmascript.org/doku.php?id=strawman:maximally_minimal_classes](http://wiki.ecmascript.org/doku.php?id=strawman:maximally_minimal_classes) [↩](https://hacks.mozilla.org#ref-9)

10. I’ve found that some ‘bad functional code’ can be refactored as concisely as possible by strictly following some functional patterns. The most problematic ‘functional’ code happens when the coder mixes two programming styles badly. This can mix problems from two paradigms in a way that makes the code more complicated. [↩](https://hacks.mozilla.org#ref-10)

11. I always hit a wall when I want to have nice Monad and lazy Promise in JavaScript. However, if you don’t mind a ‘crazy’ implementation, these are doable, and we can even have ‘Monad Transformer’ in JavaScript. Other features, like tail-recursion optimization and real lazy-evaluation, are impossible to do without runtime support. [↩](https://hacks.mozilla.org#ref-11)

12. The functions `arrow`

and `bind`

are actually `>>>`

and `>>=`

in Haskell. They’re the keys In Haskell to compose our computation and program with specific effects; hence we can have state machine, networking, event handling, IO statements, and asynchronous flow control. Importantly, these are still plain functions. [↩](https://hacks.mozilla.org#ref-12)

13. The type `IO ()`

means ‘do IO without any value returned.’ The `IO a`

means some IO actions may get value `a`

when the function had been performed, although some actions only get `()`

. For example, the function to get a string from user input would be: `ask:: IO String`

, while the function to print string out is `print:: String -> IO String`

. [↩](https://hacks.mozilla.org#ref-13)

14. [http://www.jroller.com/vaclav/entry/promises_getting_lazy](http://www.jroller.com/vaclav/entry/promises_getting_lazy) [↩](https://hacks.mozilla.org#ref-14)

15. [http://www.haskell.org/haskellwiki/Lazy_evaluation](http://www.haskell.org/haskellwiki/Lazy_evaluation) [↩](https://hacks.mozilla.org#ref-15)

16. JavaScript can do this with a library for structures like map, set, and list. Facebook created a library of immutable data structures called immutable-js for this: [https://github.com/facebook/immutable-js](https://github.com/facebook/immutable-js) [↩](https://hacks.mozilla.org#ref-16)

17. You can do almost the same thing with immutable-js and convince everyone to use only `let`

and `const`

to define variables. [↩](https://hacks.mozilla.org#ref-17)

18. [http://wiki.ecmascript.org/doku.php?id=harmony:arrow_function_syntax](http://wiki.ecmascript.org/doku.php?id=harmony:arrow_function_syntax) [↩](https://hacks.mozilla.org#ref-18)

19. wu.js: [http://fitzgen.github.io/wu.js/](http://fitzgen.github.io/wu.js/) [↩](https://hacks.mozilla.org#ref-19)

20. Ramda: [http://ramdajs.com/ramdocs/docs/](http://ramdajs.com/ramdocs/docs/) [↩](https://hacks.mozilla.org#ref-20)

21. transducer.js: [http://jlongster.com/Transducers.js–A-JavaScript-Library-for-Transformation-of-Data](http://jlongster.com/Transducers.js--A-JavaScript-Library-for-Transformation-of-Data) [↩](https://hacks.mozilla.org#ref-21)

22. LiveScript: [http://livescript.net/](http://livescript.net/) [↩](https://hacks.mozilla.org#ref-22)

23. Elm: [http://elm-lang.org/](http://elm-lang.org/) [↩](https://hacks.mozilla.org#ref-23)

24. No, they’re not really the same, but you *could* implement Promise in Monad[↩](https://hacks.mozilla.org#ref-24)

## 5 comments

Gleb BahmutovJanuary 30th, 2015 at 08:22Kyle KressFebruary 1st, 2015 at 07:42AldoFebruary 2nd, 2015 at 08:59Alex WeberFebruary 6th, 2015 at 12:44Brian mFebruary 7th, 2015 at 15:24