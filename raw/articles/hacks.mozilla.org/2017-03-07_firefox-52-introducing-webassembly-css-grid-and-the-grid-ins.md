---
title: 'Firefox 52: Introducing WebAssembly, CSS Grid and the Grid Inspector – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2017/03/firefox-52-introducing-web-assembly-css-grid-and-the-grid-inspector/
author: Dan Callahan
published: '2017-03-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Introduction

It is definitely an exciting time in the evolution of the web with the adoption of new standards, performance gains, better features for designers, and new tooling. Firefox 52 represents the fruition of a number of features that have been in progress for several years. While many of these will continue to evolve and improve, there’s plenty to celebrate in today’s release of Firefox.

In this article, the Developer Relations team covers some of the most innovative features to land, including WebAssembly, CSS Grid, the CSS Grid Inspector Tool, an improved Responsive Design Mode, and Async and Await support for JavaScript.

## WebAssembly breaks barriers between web and native

Firefox 52 supports [WebAssembly](https://research.mozilla.org/webassembly/), a new format for safe, portable, and efficient binary programs on the Web. As an emerging open standard developed by Mozilla, Google, Microsoft, and Apple, WebAssembly will eventually run everywhere that JavaScript does: in every major browser, and in browser-derived runtimes like Node.js and Electron. WebAssembly is designed to be ubiquitous.

Compilers like Mozilla’s [Emscripten](https://github.com/kripken/emscripten) can target the WebAssembly virtual architecture, making it possible to run portable C/C++ on the web at near-native speeds. In addition to C/C++, the [Rust](https://www.rust-lang.org/) programming language has [preliminary suppor](https://users.rust-lang.org/t/compiling-to-the-web-with-rust-and-emscripten/7627)t for WebAssembly, and [LLVM](http://llvm.org/) itself includes an experimental WebAssembly backend. We expect many other languages to add support for WebAssembly in the coming years.

Via Emscripten, WebAssembly makes it straightforward to port entire games and native applications to the Web, but it can also do much more. Thanks to its speed and easy interoperability with JavaScript, tasks which were previously too demanding or impractical for the web are now within reach.

(You can [click here to play](https://mzl.la/webassemblydemo) the full Zen Garden demo. Firefox 52 required, desktop only at this time. )

JavaScript functions can call WebAssembly functions, and vice versa. This makes it possible to mix-and-match between high-level JavaScript and low-level C/C++/Rust within a single web application. Developers can reuse WebAssembly modules without needing to understand their internals, much as they do today with minified JavaScript libraries.

In areas where consistent performance is most important—games, audio/video manipulation, data analysis, raw computation, codecs, etc.—WebAssembly offers clear advantages in size and speed. For this reason, we expect that many popular libraries and frameworks will eventually come to rely on WebAssembly, either directly or indirectly.

In terms of code reuse and software architecture, the wall between “native” and the web is falling, and this is just the beginning. Tooling and debugging will continue to improve, as will interoperability, performance, and raw capabilities. For example, multi-threading and SIMD are already on the WebAssembly Roadmap.

Get started with [WebAssembly on MDN](https://developer.mozilla.org/en-US/docs/WebAssembly), and find the latest information direct from the creators of WebAssembly at [WebAssembly.org](http://webassembly.org/).

## CSS Grid and the Grid Inspector

Firefox 52 includes support for [CSS Grid Layout Module Level 1](https://www.w3.org/TR/css3-grid-layout/), a CSS specification that defines 18 new CSS properties. CSS Grid is a two-dimensional layout system for the web, making it much easier to code many of the layout patterns we’ve been solving for years using grid frameworks, natively in the browser. And it opens up a world of new possibilities for graphic design. Whether you are focusing on user interfaces for app experiences or the editorial design of content, there’s a lot of power for you in this new toolset.

CSS Grid works by defining rows and columns, and placing items into areas on the grid. The rows and columns can be given a specific size (fixed, fluid, or a mix), or they can be defined to resize themselves depending on the size of content. Items on the grid can be explicitly placed in CSS, or they might be placed by the browser according to the Grid auto-placement algorithm. These sizing and placement options give CSS Grid more power and flexibility than any of the existing layout frameworks. In addition, the ability to define and place things in rows is completely new.

We are also proud to announce our new [Grid Inspector Tool](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_grid_layouts), which allows you to see the grid lines directly on the page, making it easier to see what’s happening.

See the examples from this video at [labs.jensimmons.com/2017/01-003.html](http://labs.jensimmons.com/2017/01-003.html). And find a playground of more examples at [labs.jensimmons.com](http://labs.jensimmons.com).

Interested in learning Grid? We have in-depth guides on MDN:

[Basic concepts of grid layout](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout)[Relationship of grid layout to other layout methods](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/Relationship_of_Grid_Layout)[Line-based placement with CSS Grid](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/Line-based_Placement_with_CSS_Grid)[Grid template areas](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/Grid_Template_Areas)[Layout using named grid lines](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/Layout_using_Named_Grid_Lines)[Auto-placement in CSS Grid Layout](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/Auto-placement_in_CSS_Grid_Layout)[Box alignment in CSS Grid Layout](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/Box_Alignment_in_CSS_Grid_Layout)[CSS grids, logical values and writing modes](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/CSS_Grid,_Logical_Values_and_Writing_Modes)[CSS Grid Layout and Accessibility](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/CSS_Grid_Layout_and_Accessibility)[CSS Grid Layout and Progressive Enhancement](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/CSS_Grid_and_Progressive_Enhancement)[Realizing common layouts using CSS Grid Layout](https://developer.mozilla.org/docs/Web/CSS/CSS_Grid_Layout/Realizing_common_layouts_using_CSS_Grid_Layout)

Here are answers to the two most frequently asked questions about CSS Grid:

**Should I use Grid or Flexbox? Which is better?**

You’ll use both, mixing CSS Grid with Flexbox and the other CSS Properties that affect layout (floats, margins, multicolumn, writing modes, inline block, etc.). It’s not a choose-only-one situation. Grid is the right tool when you want to control sizing and alignment in two dimensions. Flexbox is the right tool when you are only concerned with controlling one dimension. Most projects will use both, each on a different little piece of the page. Once you [understand the differences between the two](https://rachelandrew.co.uk/archives/2016/03/30/should-i-use-grid-or-flexbox/), it’ll be clear how they work together brilliantly.

**Why should I get excited about CSS Grid now? Won’t it take years before Grid is supported in enough browsers to be able to use it?**

Because of changes to the way browser companies work together to create new CSS, wide [support for CSS Grid](http://caniuse.com/#feat=css-grid) will arrive at an unprecedented speed. Mozilla is shipping support first, in Firefox 52 on March 7th. Chrome 57 will support Grid a week later, on March 14. Safari 10.1 will ship support for Grid; it’s currently in beta. Internet Explorer 10 and 11 already have support for a much earlier version of the specification, behind an -ms prefix. (You may want to utilize it, or you may not. [Learn about the details](https://rachelandrew.co.uk/archives/2016/11/26/should-i-try-to-use-the-ie-implementation-of-css-grid-layout/) before deciding.) MS Edge also has current support for the original draft of the spec, with an update to the current spec coming sometime in the future.

You can ship websites that use CSS Grid today, before 100% of your users have a browser with CSS Grid, by thinking through the structure of your code and planning for what happens in all browsers. [Feature Queries](https://hacks.mozilla.org/2016/08/using-feature-queries-in-css/) are a key tool for making sure all users have a good experience on your site.

## Async functions and the `await`

keyword

Firefox 52 also includes a brand new JavaScript feature from ES2017: asynchronous functions and their companion, the `await`

operator. Async functions build on top of ES2015 Promises, allowing authors to write asynchronous code in a similar way to how they would write their synchronous equivalents.

Take the following example, which takes the result of one asynchronous request, and uses part of it as the argument to a second asynchronous function. Here’s how it would look with a traditional callback approach:

```
function loadProfile() {
getUser(function (err, user) {
if (err) {
handleError(err);
} else {
getProfile(user.id, function (err, profile) {
if (err) {
handleError(err)
} else {
displayProfile(profile);
}
});
}
});
}
```


Relatively straightforward, but if we were to need to do additional processing and asynchronous requests, the levels of nesting or series of callback functions could become difficult to manage. Also, with more complex callback sequences, it can become difficult to determine the flow of the code, making debugging difficult.

Promises, introduced in ES2015, allow for a more compact representation of the same flow:

```
function loadProfile() {
getUser()
.then(function (user) {
return getProfile(user.id);
})
.then(displayProfile)
.catch(handleError);
}
```


Promises excel at simplifying these sequential method sequences. In this example, instead of passing a function to `getUser`

and `getProfile`

, the functions now return a Promise, which will be resolved when the function’s result is available. However, when additional processing or conditional calls are required, the nesting can still become quite deep and control flow can again be hard to follow.

Async functions allow us to re-write the example to resemble the way we would write a synchronous equivalent, without blocking the thread the way the synchronous code would!:

```
async function loadProfile() {
try {
let user = await getUser();
displayProfile(await getProfile(user.id));
} catch (err) {
handleError(err);
}
}
```


The `async`

keyword in front of the function tells the JS engine that the following function can be paused by asynchronous requests, and that the result of the function will be a Promise. Each time we need to wait for an asynchronous result, we use the `await`

keyword. This will pause execution of the function without stopping other functions from running. Also, `getUser`

and `getProfile`

don’t need to be changed from how they would be written in the Promise example.

Async functions aren’t a cure-all for complex control flow, but for many cases they can simplify the authoring and maintenance of `async`

code, without importing costly libraries. To learn more see the [ async](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/AsyncFunction) and

[MDN documentation.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await)

`await`

## Responsive Design Mode

In addition to the Grid Inspector described above, Firefox now includes an improved Responsive Design Mode (RDM). The improved RDM tool can do network throttling, simulating various connection speeds primarily experienced by mobile users. In addition, various screen size and pixel density simulations are available for common devices. Many of the features were described in [an earlier post introducing RDM](https://hacks.mozilla.org/2016/11/new-responsive-design-mode-rdm-lands-in-firefox-dev-tools/). Currently this feature is only enabled if [e10s](https://wiki.mozilla.org/Electrolysis) is also [enabled in the browser](https://support.mozilla.org/t5/Manage-preferences-and-add-ons/Enable-multiprocess-support/ta-p/1371917). Be sure to read over the complete [documentation for RDM on MDN](https://developer.mozilla.org/en-US/docs/Tools/Responsive_Design_Mode).

## More Firefox 52 goodness

These are some highlights of the game-changing features we’ve brought to the browser in Firefox 52. To see the a detailed list of all release changes, including a feature for identifying auto-generated whitespace, and the ability to detect insecure password fields, see the [Firefox 52 Release notes](https://developer.mozilla.org/en-US/Firefox/Releases/52).

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 22 comments

LukeMarch 7th, 2017 at 19:06Jason WeathersbyMarch 9th, 2017 at 12:50Ravi KasireddyMarch 8th, 2017 at 04:54Travis DohertyMarch 8th, 2017 at 07:51chathurangaMarch 8th, 2017 at 09:05Igor Cavour OliveiraMarch 8th, 2017 at 20:50Steve McWilliamMarch 9th, 2017 at 08:34Paweł P.March 9th, 2017 at 13:02Dan kokotMarch 9th, 2017 at 14:42Michal HantlMarch 9th, 2017 at 23:02AdamMarch 9th, 2017 at 23:48Dan CallahanMarch 10th, 2017 at 07:37giorgosMarch 12th, 2017 at 07:43Joshua CogliatiMarch 12th, 2017 at 07:49AkashMarch 12th, 2017 at 10:39Gary HMarch 13th, 2017 at 08:45Johnny WalkerMarch 14th, 2017 at 06:44EliahMarch 13th, 2017 at 09:04Johnny WalkerMarch 14th, 2017 at 06:46AlbertMarch 17th, 2017 at 05:42JhonsMarch 28th, 2017 at 16:11Dan CallahanMarch 31st, 2017 at 14:28