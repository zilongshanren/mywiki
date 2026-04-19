---
title: The Joys of J | Sebastian Schöner
url: https://blog.s-schoener.com/2018-02-10-joys-of-j/
author: Sebastian Schöner
published: '2018-02-10'
source_blog: Hi there! | Sebastian Schöner
source_site: https://blog.s-schoener.com/
category: graphics
fetched: '2026-04-19'
---

I wish to return to the inflammatory word I used to characterize PASCAL: fascist. If PASCAL is fascist, APL is anarchist. I tend to prefer anarchists to fascists. (

[source])

Yesterday, I got lost in the depths of my backup drive’s file system and stumbled over a set of exercises that I did for a class on primality tests and factoring algorithms from when I was studying computer science at university. That semester, I used 4 languages to solve the assignments: Python, because it is convenient; Scala and Haskell, because I love them; and J, presumably because I wanted to make the assignments a bit more interesting (and annoy the TA in the process). I quickly learnt to love J as well.

For the uninitiated, here is one of the J programs I wrote:

```
((1&=@(#@]|[*])#])i.)
```


If you find this hard to read 1, you might just be interested in reading the rest of the post.

# J - A Modern APL dialect

In the 1960s, Kenneth E. Iverson had a revelation: Programmers waste their precious time typing strings of characters representing concepts that could easily be encoded into single symbols 2. Each common operation should have its own symbol and operate on arrays to make it reusable in many contexts. This was the birth of APL, an

*Array Programming Language*. Since there are only so many common ASCII symbols, APL soon extended into what we would now call general Unicode, leading to the development of the

[APL keyboard](https://www.dyalog.com/apl-font-keyboard.htm). Unfortunately, this meant that many people had a hard time typing APL programs. The following is a sample of APL’s expressiveness, probably saying something deeply philosophical about the true nature of life

:

[3](https://blog.s-schoener.com#fn:game-of-life)```
life←{↑1 ⍵∨.∧3 4=+/,¯1 0 1∘.⊖¯1 0 1∘.⌽⊂⍵}
```


Years later, Iverson created J as a new approach to convince the world of his APL-ideas, with a focus on making it easier on the fingers 4.

Nowadays, J is easily mistaken for a [code-golfing language](https://en.wikipedia.org/wiki/Code_golf), which is unfortunate because J is actually serious business.

If you have never worked with an APL like language before, it may be difficult to grasp J. This post is not intended as a full-blown J tutorial 5, but inevitably there are a few things you need to know (or, as I’d argue,

*want*to know, because J is fun!):

- J is supposed to mimick a real languages. There are no functions, but
*verbs*, no values, but*nouns*, no expressions, but*sentences*. - All verbs are unary or binary. In J’s terminology, binary verbs are dyads and unary verbs are monads. Whether a verb is used as a dyad or monad is determined by context. Dyads take arguments left and right, monads only on their right.
- The only real data structure available are arrays in arbitrary dimensions.
- Verbs apply to all kinds of data, usually vectorising over arrays according to an arcane set of rules related to their verb’s inherent
*rank*. - Verbs are modified by
*adverbs*and*conjunctions*. Adverbs can also be used as adjectives to modify nouns. I’m skipping over*gerunds*, but of course this language has*gerund*-like features. - J does not have operator precedence. Evaluation proceeds right-to-left or as parenthesized.
- Not all types of parantheses come in pairs, so don’t get confused.
- Comments start with
`NB.`

and run through to the end of a line.

If you want to follow along on any examples, you can use [this online-interpreter](http://joebo.github.io/j-emscripten/). I recommend entering definitions in the *Script* window below, while using the command prompt above that to execute sentences whose result you’d like to see immediately. The interpreter seems to have a few missing features, especially when it comes to trains and tacit programming (see below), so longer tacit definitions will most likely not work. If you feel like it, [install J](http://code.jsoftware.com/wiki/System/Installation) for yourself.

## Basics

Variable definitions and evaluation proceeds as you would expect after what I have said above:

```
my_variable =: 15 NB. defines a variable
my_variable =: 2 * 4 + 4 NB. sets value to 16 -- right to left execution!
my_list =: 15 30 45 NB. a list of three values
my_variable + my_list NB. adds my_variable to each element in the list
NB. yielding the result 31 46 61
my_list + my_list NB. double each value in my_list
# my_list NB. compute number of elements in the list
my_list =: my_list , 60 NB. append 60 to the list
2 { my_list NB. get 3rd element from the list, i.e. at index 2
i. 5 NB. the list 0, 1, 2, 3, 4; i. is read as 'integers'
2 < i. 5 NB. the list 0, 0, 0, 1, 1
```


## Defining Verbs Procedurally

J supports good ol’ procedural programming with definitions such as a verb that doubles its input:

```
double =: 3 : 0
y + y
)
```


You can then form a full sentence such as `double 3`

. Note how the right (and only) argument to `double`

is automatically named `y`

. Also, the fact that there is no opening parenthesis is no typo. This example doesn’t really show off all the things you can do with procedural definitions, but you will likely already expect that there are `if`

s and `while`

s available, as are `try`

s and `catch`

es. If anything, the example should have convinced you that this is not beautiful.

## Defining Verbs using Operators and Composition

Instead of using procedural definitions of verbs, you can also express verbs in [point-free style](https://en.wikipedia.org/wiki/Tacit_programming). This is also known as *tacit programming* and mainly means that you create a function using function composition only, without mentioning the arguments of the function. For example, we can define addition as

```
plus =: +
```


That’s it: Plus is just another name for addition. Much nicer than using the noisy procedural syntax.

### Operators

It might be tempting to think that doubling could be defined as

```
double =: * 2
```


but this merely applies the monadic verb `*`

to the argument `2`

(yielding a result of `1`

, because monadic `*`

is the signum of the input). Instead, we need to use the *conjunction* `&`

to *bind* the parameter to an argument. Depending on whether we want to bind the left or the right parameter, we swap the order of the operands:

```
double =: * & 2 NB. 2 bound to right parameter
double =: 2 & * NB. 2 bound to left parameter
```


This is a common theme: *Operators* modify verbs. Monadic operators are *adverbs*, dyadic operators are *conjunctions*. In contrast to verbs, adverbs take their argument on the left. Here are some examples:

```
4 % 2 NB. result is 2, because % is division, not the remainder-operation
2 %~ 6 NB. result is 3, because ~ swaps the arguments of a verb
NB. ~ is an adverb
+/ 1 2 3 NB. result is 6, folds the list using +
NB. since / is the insert adverb
```


In a sentence, operators are *always* evaluated before verbs.

### Composition and Trains: Hooks and Forks

All of what we have seen up to this point is still not enough to produce such works of beauty as the verb I showed you in the introduction. This is where *trains* come in, the true genius of J: Sequences of verbs that are not immediately invoked. Trains have two forms with a special meaning: *Hooks* and *Forks*.

#### Hooks

A hook has the form `f g`

where `f`

is a dyad and `g`

is a monad. The resulting verb behaves as follows in a monadic context: `(f g) y`

evaluates as `y f (g y)`

(or equivalently, `y f g y`

). More concisely,

```
(f g) y = y f (g y) = y f g y
```


As an example, consider

```
(+ *:) 2 NB. this produces a result of 6, because monadic *: is squaring
NB. hence (+ *:) 2 = 2 + *: 2 = 2 + 4 = 6
```


Note the importance of the parentheses in `(f g) y`

: With parentheses, there is a hook on the left. Without parentheses, we have `f g y`

which is equivalent to `f (g y)`

. Therefore, trains break the usual form of function composition. This is recovered as `f @ g`

, using the *atop* conjunction `@`

. Thus `f g y = (f @ g) y`

6.

As a dyad, a hook `f g`

behaves as expected:

```
x (f g) y = x f (g y) = x f g y
```


#### Forks

A fork has the form `f g h`

with `g`

a dyad and `f, h`

monadic and dyadic. The behaviour of a fork is as follows:

```
(f g h) y = (f y) g (h y) = (f y) g h y
```


and

```
x (f g h) y = (y f x) g (x h y) = (y f x) g x h y
```


#### Longer Trains

Longer trains are naturally interpreted as hooks and forks, with the convention that trains of even length begin with a hook and trains of odd length begin with a fork. That is,

```
f g h ... = f (g h ...) NB. hook, if total length is even
f g h ... = f g (h ...) NB. fork, if total length is odd
```


# Deconstructing Tacit Programs

Now we know enough to understand some of the programs I had written for said class. But let’s first look at some easier examples. If you want to follow along, you may find it helpful to look at J’s [vocabulary page](http://www.jsoftware.com/help/dictionary/vocabul.htm) or this [slightly more structured version](http://code.jsoftware.com/wiki/NuVoc) of the vocabulary page.

#### Mean

This is a famous example from [J’s Wikipedia page](https://en.wikipedia.org/wiki/J_(programming_language)):

```
avg =: +/ % #
avg 1 2 3 4 5 NB. computes the mean of 1 2 3 4 5
```


Can you see why this works?

`+/ % #`

is a train, or more specifically, a fork. It is applied monadically:

```
(+/ % #) y = (+/ y) % (# y)
```


The left subsentence sums the list up, the right one takes the length of the list. The middle verb is just division.

#### Inverses Modulo A Number

Now for the verb from the introduction:

```
(1&=@(#@]|[*])#])i.
```


It is impossible to see what this verb is doing without the information whether it is used as a monad or a dyad. The actual invocation looks like this

```
204 ((1&=@(#@]|[*])#])i.) 2015
```


It computes the value \(d\) such that \(204 \cdot d = 1 \mod 2015\), if it exists. To understand the implementation of this verb, you must know that `|`

is the remainder operation with swapped arguments and that the brackets `[`

and `]`

are dyads that simply return their lefts or right argument, respectively. How does it work?

It works essentially by brute force. It helps to use more reasonable spacing:

```
204 ((1&=@(#@]|[*])#]) i.) 2015
= 204 ( ( 1&=@( #@] | [ * ] ) # ] ) i.) 2015
```


This makes clear that at the top-level, we have a hook, followed by a fork on the left:

```
f =: 1&=@( #@] | [ * ] )
204 ( (f # ]) i. ) 2015 NB. equivalent to the original sentence
= 204 (f # ]) (i. 2015) NB. unfolding the hook
= (204 f (i. 2015)) # (204 ] (i. 2015)) NB. unfolding the fork
= (204 f (i. 2015)) # (i. 2015) NB. definition of ]
```


This applies `#`

as a dyad, which means that the elements in the right array are copied to a new array where each element is present as many times as the corresponding number in the left array. That left array should thus be 1 for the inverse and 0 everywhere else. Morally, `f`

is therefore multiplying each of the numbers from 0 to 2014 by 204 mod 2015 and compares the results to 1. This is indeed what is happening:

```
204 f (i. 2015)
= 204 (1&=@( #@] | [ * ] )) i. 2015
= 1&= 204 (#@] | [ * ]) i. 2015 NB. definition of @
= 1&= (204 #@] i. 2015) | 204 ([ * ]) i. 2015 NB. definition of fork in a train of odd length
= 1&= #(204 ] i. 2015) | 204 ([ * ]) i. 2015 NB. definition of @
= 1&= #(204 ] i. 2015) | 204 ([ * ]) i. 2015 NB. definition of ]
= 1&= # (i. 2015) | 204 ([ * ]) i. 2015 NB. definition of ]
= 1&= 2015 | 204 ([ * ]) i. 2015 NB. definition of #
= 1&= 2015 | 204 * i. 2015 NB. definition of fork, [, and ]
```


As I notice just know, it seems that the poor idiot that past-me was did not see this much simpler solution:

```
(i.&1)@(]|[*i.@])
```


#### Quicksort

Another example straight from Wikipedia is quicksort:

```
quicksort =: (($:@(<#[), (=#[), $:@(>#[)) ({~ ?@#)) ^: (1<#)
```


You would not use this in J, since there is a sorting verb `/:`

built into the language. But it is not hard to see how this implementation works given the following information and the knowledge that what we see is a quicksort implementation:

`$:`

is a self-reference to the longest verb containing it,`? y`

produces a random number in the range \([0, y)\),`u ^: v`

is the power-of conjunction, which evaluates as`(u ^: v) y = (u y) ^: (v y)`

meaning that`u`

will be iterated on`y`

for`v y`

many steps. For example,`(*: ^: ]) 2`

has a result of`16`

, because it is squaring`2`

twice (or rather, it computes`:* :* 2`

)

Can you see how this quicksort implementation works?

At the top level of the definition, we have the `^:`

conjunction. Its right argument is `(1 < #)`

which is applied to the input list and evaluates to 1 if and only if its length is greater than one: `(1 < #) y = 1 < (# y)`

. This means that the left part of the definition is executed once for lists with at least 2 elements, 0 times otherwise. So that is nothing but an `if`

.

The left part can be read fluently (with some practice):

```
(($:@(<#[), (=#[), $:@(>#[)) ({~ ?@#))
```


This is a hook of the form `lhs rhs`

, evaluating as `(lhs rhs) y = y lhs (rhs y)`

. The right part `({~ ?@#)`

selects a pivot element at random since

```
rhs y
= ({~ ?@#) y NB. definition of rhs
= y {~ (?@# y) NB. definition of hook
= y {~ (? (# y)) NB. definition of @
= (? (# y)) { y NB. definition of ~
=: pivot y
```


where `x { y`

is indexing `y`

with `x`

.

On the left, we have three groups of verbs `u, v, w`

that should by now almost be self-explanatory, separated by the concatenation verb `,`

. This forms a train of two forks

```
y (u, v, w) pivot y
= y (u , (v , w)) pivot y NB. rules for long trains
= (y u pivot y) , (y (v , w) pivot y) NB. definition of fork
= (y u pivot y) , (y v pivot y), (y w pivot y) NB. definition of fork
```


All that is left is to convince yourself that `u, v, w`

select all elements smaller than, equal to, or greater than the pivot from the list, respectively, and recurse on them. But this is easy to see since for `u`

:

```
y ($:@(<#[) pivot y
= $: y (<#[) pivot y NB. definition of @
= $: (y < pivot y) # (y [ pivot y) NB. definition of fork
= $: (y < pivot y) # y NB. definition of [
= quicksort (y < pivot y) # y NB. definition of $:, definition of quicksort
```


Remember that `x # y`

creates a new array where each entry in `y`

is present `n`

times where `n`

is the corresponding value in `x`

. Similar reasoning applies to `v, w`

.

#### Number of Primes up to a Given Bound

To finish off, let’s look at how you could torture a TA who just wants to see a small program that calculates the number of primes up to some given numbers, say 1000, 10000, and 10000. In J, this could be written as

```
(p:^:_1) 1+10^(3 4 5)
```


I consider this cheating because here the inbuilt function `p:`

does all the actual work. My submission was:

```
l =: 0 0&,@(-&1#1:)
s =: *1&<.@((i.&1)|i.@#)
a =: >@[ ([`([,i.&1@]))@.((#>i.&1)@]) >@]
primesUpTo =: >@{.@((a/;s@>@]/)^:_)@((>a:)&;@l)
```


I of course included plenty of comments on what the code is doing on a high level (it uses a straight forward implementation of the sieve of Eratosthenes), but I am confident that nobody took the time to check whether the program was actually working (except for me, obviously). I am also pretty sure that this J code is far from the optimum on close to all metrics (speed, brevity, and - well - readability), but, surprisingly, the TA did not deduct any points for my use of J.

# Conclusion

If you long for more tacit programs in J, take a look at its list of [phrases and idioms](http://www.jsoftware.com/help/phrases/contents.htm). If you feel the sudden need to read a very political essay on APL, [try this article](http://www.users.cloud9.net/~bradmcc/APL.html), which is also the source of the opening quote.

Let me know if you come up with an especially convoluted tacit program for a simple problem yourself :)

-
Needless to say, I do not advocate the use of this style and tacit programming in production code. Do it at home or while you are still in University ;) I should also mention that you can write clear, concise, and performant programs in J, but this is not the reason I love this language for.

[↩](https://blog.s-schoener.com#fnref:disclaimer) -
This incident is unfortunately not recorded in the only

[reliable source](http://james-iry.blogspot.de/2009/05/brief-incomplete-and-mostly-wrong.html)on the history of programming lanauges. Check the 1987 entry on Perl for another reasonable explanation of what APL’s inception could have been like.[↩](https://blog.s-schoener.com#fnref:perl) -
It is an implementation of Conway’s Game of Life, taken straight from

[Wikipedia](https://en.wikipedia.org/wiki/APL_(programming_language)).[↩](https://blog.s-schoener.com#fnref:game-of-life) -
I am deliberatly skipping over all the gory details. APL was at one point or another actually a popular language and there are still plenty of people who swear by it. Its

[Wikipedia entry](https://en.wikipedia.org/wiki/APL_(programming_language))has an extensive section on APL’s history.[↩](https://blog.s-schoener.com#fnref:history) -
There is so much more to learn about this language. As with any language, J has a

[vocabulary](http://code.jsoftware.com/wiki/NuVoc), a book of common[phrases and idioms](http://www.jsoftware.com/help/phrases/contents.htm), a[dictionary](http://www.jsoftware.com/help/dictionary/contents.htm), and a[learner’s guide](http://www.jsoftware.com/help/learning/contents.htm).[↩](https://blog.s-schoener.com#fnref:tutorial) -
This is mostly true, but due to the way that verbs vectorize over arrays, J needs 4 different kinds of verb composition to reflect the different behaviors. See

[this page](http://code.jsoftware.com/wiki/Vocabulary/at), especially the diagram further down below.[↩](https://blog.s-schoener.com#fnref:ranks)