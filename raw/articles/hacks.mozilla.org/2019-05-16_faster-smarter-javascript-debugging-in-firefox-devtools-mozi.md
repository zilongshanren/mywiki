---
title: Faster smarter JavaScript debugging in Firefox DevTools – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2019/05/faster-smarter-javascript-debugging-in-firefox/
author: Harald Kirschner
published: '2019-05-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Script debugging is one of the most powerful and complex productivity features in the web developer toolbox. Done right, it empowers developers to fix bugs quickly and efficiently. So the question for us, the Firefox DevTools team, has been, are the Firefox DevTools doing it right?

We’ve been listening to feedback from our community. Above everything we heard the need for greater **reliability** and **performance**; especially with modern web apps. Moreover, script debugging is a hard-to-learn skill that should work in similar fashion across browsers, but isn’t consistent because of feature and UI gaps.

With these pain points in mind, the DevTools Debugger team – with help from our tireless [developer community](https://devtools-html-slack.herokuapp.com/) – landed countless updates to design a more productive debugging experience. The work is ongoing, but Firefox 67 marks an important milestone, and we wanted to highlight some of the fantastic improvements and features. We invite you to [open up Firefox Quantum: Developer Edition](https://www.mozilla.org/en-US/firefox/developer/), try out the debugger on the examples below and your projects and let us know if you notice the difference.

## A rock-solid debugging experience

Fast and reliable debugging is the result of many smaller interactions. From initial loading and source mapping to breakpoints, console logging, and variable previews, everything needs to *feel* solid and responsive. The debugger should be consistent, predictable, and capable of understanding common tools like [webpack](https://webpack.js.org/), [Babel](https://babeljs.io), and [TypeScript](https://www.typescriptlang.org).

We can proudly say that *all* of those areas have improved in the past months:

**Faster load time**. We’ve eliminated the worst performance cliffs that made the debugger slow to open. This has resulted in a 30% speedup in our[performance test suite](https://firefox-dev.tools/performance-dashboard/tools/debugger.html?days=90&filterstddev=true&ignoreFlags=true). We’ll share more of our performance adventures in a future post.**Excellent source map support.**A revamped and[faster](https://hacks.mozilla.org/2018/01/oxidizing-source-maps-with-rust-and-webassembly/)source-map backend perfects the illusion that you’re debugging*your*code, not the compiled output from*Babel*,*Webpack*,*TypeScript*,*vue.js*, etc.

Generating correct source maps can be challenging, so we also contributed patches to build tools (i.e.[babel](https://github.com/babel/babel/pull/8380),[vue](https://github.com/vuejs/vue-loader/issues/1163#issuecomment-384712864).[js](https://github.com/babel/babel/issues/7632),[regenerator](https://github.com/facebook/regenerator/issues/342)) – benefiting the whole ecosystem.**Reduced overhead when debugger isn’t focused.**No need to worry any longer about keeping the DevTools open! We found and removed many expensive calculations from running in the debugger when it’s in the background.**Predictable breakpoints, pausing, and stepping.**We fixed many long-standing bugs deep in the debugger architecture, solving some of the most common and frustrating issues related to lost breakpoints, pausing in the wrong script, or stepping through pretty-printed code.**Faster variable preview.**Thanks to our faster source-map support (and lots of additional work), previews are now displayed much more quickly when you hover your mouse over a variable while execution is paused.

These are just a handful of highlights. We’ve also resolved countless [bugs](https://github.com/firefox-devtools/debugger/issues?q=is%3Aissue+is%3Aclosed+label%3A%22%3Abug%3A+bug%22) and [polish](https://github.com/firefox-devtools/debugger/issues?q=is%3Aissue+is%3Aclosed+label%3A%22%3Awave%3A+polish%22) issues.

### Looking ahead

Foremost, we must maintain a high standard of quality, which we’ll accomplish by explicitly setting aside time for polish in our planning. Guided by user feedback, we intend to use this time to improve new and existing features alike.

Second, continued investment in our [performance](https://firefox-dev.tools/performance-dashboard/) and [correctness](https://github.com/firefox-devtools/debugger/tree/master/src/workers/parser/tests/fixtures/frameworks) tests ensures that the ever-changing JavaScript ecosystem, including a wide variety of frameworks and compiled languages, is well supported by our tools.

## Debug all the things with new features

Finding and pausing in just the right location can be key to understanding a bug. This should feel effortless, so we’ve scrutinized our own tools—and studied others—to give you the best possible experience.

### Inline breakpoints for fine-grained pausing and stepping

Why should breakpoints operate on lines, when lines can have multiple statements? Thanks to inline breakpoints, it’s now easier than ever to debug minified scripts, arrow functions, and chained method calls. Learn more about [breakpoints on MDN](https://developer.mozilla.org/en-US/docs/Tools/Debugger/How_to/Set_a_breakpoint) or [try out the demo](https://firefox-devtools-example-babel-typescript.glitch.me/).

### Logpoints combine the power of Console and Debugger

Console logging, also called `printf() debugging`

, is a quick and easy way to observe your program’s flow, but it rapidly becomes tedious. Logpoints break that tiresome edit-build-refresh cycle by dynamically injecting `console.log()`

statements into your running application. You can stay in the browser and monitor variables without pausing or editing any code. Learn more about [log points on MDN](https://developer.mozilla.org/en-US/docs/Tools/Debugger/Set_a_log_point).

### Seamless debugging for JavaScript Workers

[Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API) power the modern web and need to be first-class concepts in DevTools. Using the new *Threads* panel, you can switch between and independently pause different execution contexts. This allows workers and their scripts to be debugged within the same Debugger panel, similarly to other modern browsers. Learn more about [Worker debugging on MDN](https://developer.mozilla.org/en-US/docs/Tools/Debugger).

### Human-friendly variable names for source maps

Debugging bundled and compressed code isn’t easy. The [Source Maps](https://github.com/mozilla/source-map) project, started and maintained by Firefox, bridges the gap between minified code running in the browser and its original, human-friendly version, but the translation isn’t perfect. Often, bits of the minified build output shine through and break the illusion. We can do better!

By combining source maps with the [Babel parser](https://babeljs.io/docs/en/babel-parser), Firefox’s Debugger can now preview the original variables you care about, and hide the extraneous cruft from compilers and bundlers. This can even work in the console, automatically resolving human-friendly identifiers to their actual, minified names behind the scenes. Due to its performance overhead, you have to [enable this feature](https://developer.mozilla.org/en-US/docs/Tools/Debugger/Using_the_Debugger_map_scopes_feature) separately by clicking the “Map” checkbox in the Debugger’s *Scopes* panel. Read the MDN documentation on [using the map scopes feature](https://developer.mozilla.org/en-US/docs/Tools/Debugger/Using_the_Debugger_map_scopes_feature).

### What’s next

Developers frequently need to switch between browsers to ensure that the web works for everyone, and we want our DevTools to be an intuitive, seamless experience. Though browsers have converged on the same broad organization for tools, we know there are still gaps in both features and UI. To help us address those gaps, please [let us know](https://bugzilla.mozilla.org/enter_bug.cgi?product=DevTools&component=Debugger) where you experience friction when switching browsers in your daily work.

## Your input makes a big difference

As always, we would love to hear your feedback on how we can improve DevTools and the browser.

- File bug reports in
[here in Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=DevTools&component=General) - Chat with us in the
[Firefox DevTools Slack](https://devtools-html-slack.herokuapp.com/) - Share ideas and questions in Mozilla’s
[Developer Tools Discourse](https://discourse.mozilla.org/c/devtools) - Tweet us at
[@FirefoxDevTools](https://twitter.com/FirefoxDevTools)

While all these updates will be ready to try out in Firefox 67, when it’s released next week, we’ve polished them to perfection in Firefox 68 and added a few more goodies. Download [Firefox Developer Edition (68)](https://www.mozilla.org/en-US/firefox/developer/) to try the latest updates for devtools and platform now.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

## 31 comments

Billal BEGUERADJMay 17th, 2019 at 03:00Harald Kirschner (digitarald)May 17th, 2019 at 09:59SaruMay 17th, 2019 at 04:57Harald Kirschner (digitarald)May 17th, 2019 at 09:58VincentMay 17th, 2019 at 12:28artalarMay 17th, 2019 at 22:14OlgaMay 17th, 2019 at 23:05Yoh AdamsMay 17th, 2019 at 23:42Harald Kirschner (digitarald)May 20th, 2019 at 08:46EdmundMay 18th, 2019 at 03:16MarkMay 19th, 2019 at 11:59Ivan EnderlinMay 21st, 2019 at 00:17Rafael RamalhoMay 21st, 2019 at 02:40Harald Kirschner (digitarald)May 21st, 2019 at 08:51Da ScritchMay 21st, 2019 at 08:04Harald Kirschner (digitarald)May 21st, 2019 at 21:43FnLnMay 27th, 2019 at 15:49AslanMay 22nd, 2019 at 01:00Harald Kirschner (digitarald)May 22nd, 2019 at 06:56MikeyBMay 22nd, 2019 at 14:53Harald Kirschner (digitarald)May 22nd, 2019 at 16:31WykksMay 23rd, 2019 at 06:59Harald Kirschner (digitarald)May 23rd, 2019 at 09:41Rafael Corrêa GomesMay 23rd, 2019 at 08:08AnonymousMay 26th, 2019 at 02:37Harald Kirschner (digitarald)May 29th, 2019 at 09:41ThomasMay 29th, 2019 at 04:06Harald Kirschner (digitarald)May 29th, 2019 at 09:30DavidJune 3rd, 2019 at 02:07Harald Kirschner (digitarald)June 3rd, 2019 at 06:57DavidJune 4th, 2019 at 07:06