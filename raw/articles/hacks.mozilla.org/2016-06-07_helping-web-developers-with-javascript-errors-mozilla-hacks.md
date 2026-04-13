---
title: Helping web developers with JavaScript errors – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/06/helping-web-developers-with-javascript-errors/
author: Florian Scholz
published: '2016-06-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Errors are one of the more frustrating things you encounter while programming. Those little messages in the console can ruin your entire afternoon, day, or week. When “undefined is not a function” appears yet again, it’s often time to get another coffee.

Even if you use the [one true JavaScript exception handler](https://twitter.com/DivineOmega/status/695744177557106688), and have a lightning fast “copy and paste into $search_engine” reflex, the process of tracking down helpful information about an error can be annoying.

It doesn’t necessarily need to be that way! Some programming languages (hi [Rust](https://doc.rust-lang.org/book/error-handling.html)) take their error reporting to the next level by providing more information than just the fact that something went wrong.

We are not introducing JavaScript Clippy today. However, with the help of the MDN community, we are going to add links to documentation from error messages that appear within the [Firefox Developer Tools console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console).

![](../../assets/da87e2933854e2fd.gif)


This is to help you debug faster and learn more about JavaScript’s edge cases and lesser known functionality. Especially if you are new to JavaScript, we hope that you’ll appreciate this additional debugging help, or for those times when you’ve had too much coffee and you still can’t find the solution.

Documenting all the JavaScript, DOM, and other varieties of error messages that are thrown at you is a lot of work. We are focusing on the most commonly thrown errors for now. If you feel like helping here, [get in touch with the MDN community](https://developer.mozilla.org/en-US/docs/MDN/Community/Conversations) and we promise you’ll learn a lot about JavaScript’s interesting quirks!

Try a recent [Nightly build of Firefox](https://nightly.mozilla.org/) to test this feature, or have a look at the [MDN JavaScript error documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors) directly.

## About
[
Florian Scholz ](https://developer.mozilla.org)

Florian is the Content Lead for MDN Web Docs, writes about Web platform technologies and researches browser compatibility data. He lives in Bremen, Germany.

## One comment

StefanyJune 13th, 2016 at 14:48