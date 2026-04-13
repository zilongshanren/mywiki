---
title: Debugging Modern Web Applications – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/05/debugging-modern-web-applications/
author: Jasonlaster Github Io
published: '2018-05-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Building and debugging modern JavaScript applications in Firefox DevTools just took a *quantum* leap forward. In collaboration with [Logan Smyth](https://github.com/loganfsmyth), Tech Lead for [Babel](https://babeljs.io/), we leveled up the debugger’s source map support to let you inspect the code that you actually wrote. Combined with the ongoing initiative to offer first-class JS framework support across all our devtools, this will boost productivity for modern web app developers.

Modern JS frameworks and build tools play a critical role today. Frameworks like [React](https://reactjs.org/), [Angular](https://angular.io/), and [Ember](https://www.emberjs.com/) let developers build declarative user interfaces with JSX, directives, and templates. Tools like [Webpack](https://webpack.js.org/), [Babel](http://babeljs.io/), and [PostCSS](https://postcss.org/) let developers use new JS and CSS features before they are supported by browser vendors. These tools help developers write simpler code, but generate more complicated code to debug.

In the example below, we use Webpack and Babel to compile ES Modules and async functions into vanilla JS, which can run in any browser. The original code on the left is pretty simple. The generated, browser-compatible code on the right is much more complicated.

![In the example below, we use Webpack and Babel to compile ES Modules and async functions into vanilla JS. The original code on the left is pretty simple. The generated, browser-compatible code on the right is much more complicated.](../../assets/b521af9da58194c1.jpg)


*Figure 1. Original file on the left, generated file on the right.*

When the debugger pauses, it uses source maps to navigate from line 13 in the generated code to line 4 in the original code. Unfortunately, because pausing actually happens on line 13, it can be difficult for the user to figure out what the value of * dancer* is at that time. Moving the mouse over the variable

**returns**

*dancer*`undefined`

and the only way to find the scope of *is to open all six of the available scopes in the Scopes pane followed by expanding the*

**dancer***object! This complicated and frustrating process is why many people opt to disable source maps.*

**_emojis**![A view of the disconnect between the original code file and the generated code, which opens multiple scopes](../../assets/c3af2069d30f2dc6.png)


*Figure 2. Value of dancer is undefined, six separate scopes in the Scopes pane.*

To address this problem we teamed up with Logan Smyth to see if it was possible to make the interaction feel more natural, as if you were debugging your original code. The result is a new engine that maps source maps data with Babel’s syntax tree to show the variables you expect to see the way you want to see them.

![Now the panel displays the correct value of dancer, and the Scopes pane shows one scope](../../assets/602929561f620d35.png)


*Figure 3. Correct value of dancer is displayed, Scopes pane shows one scope.*

These improvements were first implemented for Babel and Webpack, and we’re currently adding support for TypeScript, Angular, Vue, Ember, and many others. If your project already generates source maps there is a good chance this feature will work for you out of the box.

To try it out, just head over and download [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/). You can help us by testing this against your own project and [reporting](https://github.com/firefox-devtools/debugger.html/issues/new) any issues. If you want to follow along, say hello, or contribute, you can also find us on the devtools channel [Github](https://github.com/firefox-devtools/debugger.html/issues/5561) or [Mozilla Discourse](https://discourse.mozilla.org/c/devtools) or in the [devtools Slack](https://devtools-html-slack.herokuapp.com/)!

Our 2018 goal is to improve the lives of web developers who are building modern apps using the latest frameworks, build tools and best practices. Fixing variables is just the beginning. The future is bright!

## About
[
jlaster ](http://jasonlaster.github.io)

Staff Engineer on Firefox Developer Tools devving the DevTools and debugging the debugger.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

## 6 comments

AaronMay 15th, 2018 at 12:16Harald KirschnerMay 24th, 2018 at 12:56ValentinMay 17th, 2018 at 00:12Harald KirschnerMay 24th, 2018 at 12:54ThomazellaMay 17th, 2018 at 08:55Neville BradleyMay 19th, 2018 at 19:32