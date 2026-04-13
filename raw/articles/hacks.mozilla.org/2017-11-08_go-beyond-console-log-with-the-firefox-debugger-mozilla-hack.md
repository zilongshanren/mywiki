---
title: Go beyond console.log with the Firefox Debugger – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/11/go-beyond-console-log-with-the-firefox-debugger/
author: Dustin Driver
published: '2017-11-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

`console.log`

is no debugger. It’s great for figuring out what your JavaScript app is up to, but it’s limited to spitting out a minimal amount of information. If your code is complex, you’ll need a proper debugger. That’s why we’ve added a new section to the Firefox DevTools Playground that’s [all about debugging](https://mozilladevelopers.github.io/playground/debugger). We’ve built four basic lessons that use the Firefox Debugger to examine and repair a simple JavaScript to-do app.

## Introducing the Debugger Playground

The lessons are completely free and the to-do app code is [available for download from GitHub](https://mozilladevelopers.github.io/sample-todo/01-variables/).

These lessons are a new format for us and we’re very excited to bring them to you. We’re always looking for new ways to help developers learn things and improve the daily workflow. If you have an idea, let us know. We’ll be expanding the Playground in the coming months and we’d love to hear from developers like you.

If you’re not familiar with the Firefox Debugger, take a look at the [debugger docs](https://developer.mozilla.org/en-US/docs/Tools/Debugger) on MDN and watch this quick intro video:

Now let’s take a look at a lesson from the new Debugger Playground. Ever use `console.log`

to find the value of a variable? There’s an easier and more accurate way to do this with the Debugger.

## Use Debugger to find the value of a variable

It’s much easier to find a variable with Firefox Debugger than it is with `console.log`

. Here’s how it works:

Let’s take a look at a simple to-do app. [Open the to-do app in new tab](https://mozilladevelopers.github.io/sample-todo/01-variables/).

This app has a function called `addTodo`

which will take the value of the input form, create an object, and then push that object onto an array of tasks. Let’s test it out by adding a new task. You’d expect to have this new task added to the list, but instead you see “[object HTMLInputElement]”.

Something is broken, and we need to debug the code. The temptation is to start adding console.log throughout the function, to pinpoint where the problem is. The approach might look something like this:

```
const addTodo = e => {
e.preventDefault();
const title = document.querySelector(".todo__input");
console.log('title is: ', title);
const todo = { title };
console.log('todo is: ', todo');
items.push(todo);
saveList();
console.log(‘The updated to-do list is: ‘, items);
document.querySelector(".todo__add").reset();
};
```


This can work, but it is cumbersome and awkward. We also have to remember to remove these lines after fixing the code. There’s a much better way to do it with the Debugger using what is called a breakpoint…

## Learn more on the Debugger Playground

The Debugger Playground covers the basics of using the Firefox Debugger, examining the call stack, setting conditional breakpoints, and more. We know there’s a steep learning curve to using the Debugger (and debugging JavaScript), so we’ve pieced together a simple to-do app that’s easy to understand and decode. It’s also useful to run in your browser to keep things on track throughout your work day. The app is [available here for download](https://github.com/MozillaDevelopers/sample-todo) on GitHub. Grab it and then head over to the [Playground](https://mozilladevelopers.github.io/playground/) to walk through the lessons there.

Let us know what you’d like to see next. We’re working on new lessons about the latest web technologies and we’d love to hear from you. Post in the comments below.

## About Dustin Driver

Journalist, tech writer, and video producer helping Mozilla keep the Web open and accessible for everyone.

## 9 comments

LesMurphyNovember 9th, 2017 at 09:38Dustin DriverNovember 13th, 2017 at 07:55Chris EdwardsNovember 9th, 2017 at 10:01RichardNovember 10th, 2017 at 06:01Dustin DriverNovember 13th, 2017 at 07:53JamesNovember 10th, 2017 at 18:31Dustin DriverNovember 13th, 2017 at 07:55Jeremy WaltonNovember 17th, 2017 at 10:26Jason LasterNovember 21st, 2017 at 15:05