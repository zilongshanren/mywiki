---
title: insertAdjacentHTML() Enables Faster HTML Snippet Injection – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2011/11/insertadjacenthtml-enables-faster-html-snippet-injection/
author: Janet Swisher
published: '2011-11-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The following is a guest post by

[Henri Sivonen]:

In Firefox 8, we’ve added support for `insertAdjacentHTML()`

. It’s an ancient feature of Internet Explorer that has recently been formalized in HTML5 and then spun out into the [DOM Parsing specification]. The bad news is that Firefox is the last major browser to implement this feature. The good news is that since other major browsers implement it already, you can start using it unconditionally as soon as the Firefox 8 update has been rolled out to users.

## Basic Usage

`insertAdjacentHTML(<var>position</var>, <var>markup</var>)`

is a method on `HTMLElement`

DOM nodes. It takes two string arguments. The first argument is one of `"beforebegin"`

, `"afterbegin"`

, `"beforeend"`

, or `"afterend"`

and gives the insertion point relative to the node that `insertAdjacentHTML()`

is invoked on. The second argument is a string containing HTML markup that gets parsed as an HTML fragment (similar to a string assigned to `innerHTML`

) and inserted to the position given by the first argument.

If the node that `insertAdjacentHTML()`

is invoked on is a `p`

element

with the text content “foo”, the insertion points would be where the comments are in the following snippet:

```
```foo


The `"beforebegin"`

and `"afterend"`

positions work only if

the node is in a tree and has an element parent.

For example, consider the following code:

```
```foo


This code produces this log output:

foobar


Well, that does not look particularly special. In fact, it looks like something that could have been done using plain old `innerHTML`

. So why bother with `insertAdjacentHTML()`

when `<var>element</var>.innerHTML += "<var>markup</var>";`

already works?

There are two reasons.

`insertAdjacentHTML()`

doesn’t corrupt what’s already in the DOM.`insertAdjacentHTML()`

is faster.

## Avoiding DOM corruption

Let’s consider the DOM corruption issue first. When you do `<var>element</var>.innerHTML += "<var>markup</var>";`

, the browser does the following:

- It gets the value of
`innerHTML`

by serializing the descendants of`<var>element</var>`

. - It appends the right hand side of
`+=`

to the string. - It removes the children of
`<var>element</var>`

. - It parses the new string that contains the serialization of the old descendants followed by some new markup.

The old descendants might have been script-inserted to form a subtree that doesn’t round-trip when serialized as HTML and reparsed. In that case, after the operation, the tree would have a different shape even for the “old” parts. (For example, if `<var>element</var>`

had a `p`

child which in turn had a `div`

child, the subtree wouldn’t round-trip.) Furthermore, even if serializing and reparsing resulted in a same-looking tree, the nodes created by the parser would be different nodes than the nodes that were children of `<var>element</var>`

at first. Thus, if other parts of the JavaScript program were holding references to descendants of `<var>element</var>`

, after `<var>element</var>.innerHTML += "<var>markup</var>";`

had been executed, those references would point to detached nodes and `<var>element</var>`

would have new similar but different descendants.

When additional content is inserted using `insertAdjacentHTML()`

, the existing nodes stay in place.

## Better performance

Serializing and reparsing is also what leads to performance problems with the `<var>element</var>.innerHTML += "<var>markup</var>";`

pattern. Each time some more content is appended, all the existing content in `<var>element</var>`

gets serialized and reparsed. This means that appending gets slower and slower, because each time there more and more previous content to serialize and reparse.

Using `insertAdjacentHTML()`

can make a big difference. For testing purposes, I started with an empty `div`

and ran a loop that tried to append as many tweets as possible to the `div`

in five seconds. A tweet is actually rather large when you count all the mark-up that implements @mention linkification, the name of the tweeter, retweet and favoriting UI, etc. It weighs about 1600 characters of HTML source—most of it mark-up.

On the computer that I used for testing, the `innerHTML`

way of appending managed to append only *slightly over 200* tweets in five full seconds. In contrast, the `insertAdjacentHTML("beforeend", ...)`

way of appending managed to append *almost 30,000* tweets in 5 seconds. (Yes, that’s hundreds versus tens of thousands.) Obviously, real Web apps should never block the event loop for five seconds—this is just for benchmark purposes. However, this illustrates how the `innerHTML`

way of appending becomes notably slower as more and more content accumulates to be serialized and reparsed each time.

At this point, some readers might wonder if `insertAdjacentHTML()`

offers any benefit over `createContextualFragment()`

. After all, conceptually `insertAdjacentHTML()`

creates a fragment and inserts it.

Using `createContextualFragment()`

, my test manages only slightly over 25,000 tweets in five seconds, while using `insertAdjacentHTML()`

manages slightly under 30,000. This is because Gecko accelerates `insertAdjacentHTML()`

when the insertion point has no next sibling (only for HTML though—not for XML so far). The `"beforeend"`

insertion point never has a next sibling and is always accelerated (for HTML). The `"beforebegin"`

insertion point always has a next sibling (the node that `insertAdjacentHTML()`

was invoked on) and is never accelerated. For `"afterbegin"`

and `"afterend"`

, whether the operation is accelerated depends on the situation.

In conclusion, you can make your Web app perform better by using `<var>element</var>.insertAdjacentHTML("beforeend", "<var>markup</var>");`

where you currently use `<var>element</var>.innerHTML += "<var>markup</var>";`

.

## About
[
Janet Swisher ](https://developer.mozilla.org)

Janet is the Community Lead and Project Manager for MDN Web Docs. She joined Mozilla in 2010, and has been involved in open source software since 2004 and in technical communication since the 20th century. She lives in Austin, Texas, with her husband and a standard poodle.

## 15 comments

Alex ChangNovember 9th, 2011 at 21:32FatihNovember 9th, 2011 at 22:00Maurizio DOmbaNovember 10th, 2011 at 00:21Rene KriestNovember 10th, 2011 at 01:16TheodorNovember 10th, 2011 at 01:58RuturajNovember 10th, 2011 at 04:10pdNovember 10th, 2011 at 05:17timmywilNovember 10th, 2011 at 07:33Henri SivonenNovember 11th, 2011 at 03:42Richard KimberNovember 11th, 2011 at 06:01Manuel StrehlNovember 11th, 2011 at 06:08Jamie MurphyNovember 11th, 2011 at 06:59Dmitry PashkevichNovember 11th, 2011 at 07:23Henri SivonenNovember 14th, 2011 at 02:20Marcos ZanonaNovember 16th, 2011 at 08:38