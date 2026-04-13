---
title: 'MDN browser compatibility data: Taking the guesswork out of web compatibility
  – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2018/02/mdn-browser-compatibility-data/
author: Florian Scholz
published: '2018-02-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Building the web is hard

The most powerful aspect of the web is also what makes it so challenging to build for: its universality. When you create a website, you’re writing code that needs to be understood by a plethora of browsers on different devices and operating systems. It’s difficult.

To make the web evolve in a sane and sustainable way for both users and developers, browser vendors work together to standardize new features, whether it’s a new [HTML element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element), [CSS property](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference#Keyword_index), or [JavaScript API](https://developer.mozilla.org/en-US/docs/Web/API). But different vendors have different priorities, resources, and release cycles — so it’s very unlikely that a new feature will land on all the major browsers at once. As a web developer, this is something you must consider if you’re relying on a feature to build your site.

Even more challenging than waiting for browsers to implement a feature you need is catering for those that never will. Building for the web means supporting older – but sometimes still widely used – versions of browsers, with quirks and feature sets locked in time forever. For all this, choosing to use one particular feature over another on a website effectively means making a decision about which browsers it will optimally support.

## Enter the Browser Compatibility Project

To help developers make these decisions consciously rather than accidentally, [MDN Web Docs](https://developer.mozilla.org/) provides browser compatibility tables in its documentation pages, so that when looking up a feature you’re considering for your project, you know exactly which browsers will support it. Whilst unquestionably helpful, this resource alone doesn’t eliminate all challenges. First of all, it requires people to actively search for compatibility data for each feature they use, which may not be trivial for less experienced developers. In addition, there is the question of what happens when you inherit a project that already has hundreds or thousands of lines of code. Inspecting each line individually to look for compatibility issues doesn’t seem like a reasonable option.

To allow for browser compatibility data to be accessed programmatically rather than requiring developers to manually search for it, the MDN community is working on migrating the compatibility information currently stored on thousands of wiki pages to a machine-readable JSON format in a [GitHub repository](https://github.com/mdn/browser-compat-data). This opens the door to a myriad use cases, such as displaying compatibility information on a text editor as the developer writes the code, or an audit tool that scans an entire codebase and flags compatibility issues that the developer might not be aware of.

The data is available as an [npm package](https://www.npmjs.com/package/mdn-browser-compat-data) and you can get compatibility information for a given web feature like this:

```
const compat = require('mdn-browser-compat-data');
let textJustify = compat.css.properties[‘text-justify’];
// returns a compat data object
```


It will return the data stored in the repository, in this case from the [text-justify.json](https://github.com/mdn/browser-compat-data/blob/master/css/properties/text-justify.json) file. You can query the data set, like for example finding out which Firefox version added support for [text-justify](https://developer.mozilla.org/en-US/docs/Web/CSS/text-justify):

`textJustify.support.firefox; // returns “55”`


The compat data structure is described by a [JSON schema](https://github.com/mdn/browser-compat-data/blob/master/schemas/compat-data-schema.md); as well as the version numbers, it also contains information about prefixes or flags that might need to be set for a feature to work.

The data is kept up-to-date and maintained by the MDN community and browser vendors who, working together formed the [MDN Product Advisory Board](https://blog.mozilla.org/blog/2017/10/18/mozilla-brings-microsoft-google-w3c-samsung-together-create-cross-browser-documentation-mdn/) last year. Board members [agreed to drive updates to compatibility data](https://hacks.mozilla.org/2018/01/introducing-the-mdn-product-advisory-board/) for Edge, Chrome, and Samsung Internet after each stable release and to help review compatibility data PRs that are flagged for their browser.

## Finding compatibility issues from DevTools

An interesting example of the possibilities created by this data is a project called [compat-report](https://addons.mozilla.org/en-US/firefox/addon/compat-report/), an extension made by developer [Eduardo Boucas](https://twitter.com/eduardoboucas?lang=en) as a side project, that adds a Compatibility panel to the browser developer tools. Inside, a table shows how any given site is expected to perform on each of the main browsers, showing each version where no compatibility issues are found in green, those with a few issues in yellow, and those with several problems in red. This gives developers an initial overview of how well their site stacks up against the different browsers on the market.

Clicking on a browser version will launch a more detailed report, highlighting lines with compatibility issues for each style sheet on the page. Where applicable, the extension will also suggest ways to address the problem, such as adding a vendor prefix, as shown in the image below.

This project is still in its early stages, but the scope is immense and the roadmap is ambitious. Currently it only analyzes CSS, but in the future it could also flag compatibility problems with HTML and JavaScript. It could even leverage the vast number of polyfills on MDN to not only flag compat issues but also offer ways to address them.

The extension itself is built using just HTML, CSS and JavaScript and its source is available [on GitHub](https://github.com/eduardoboucas/compat-report). If you like the idea and would like to help us take it further, we’d love for you to contribute.

## About
[
Florian Scholz ](https://developer.mozilla.org)

Florian is the Content Lead for MDN Web Docs, writes about Web platform technologies and researches browser compatibility data. He lives in Bremen, Germany.

## 10 comments

Maxime CorteelFebruary 1st, 2018 at 04:46D DFebruary 1st, 2018 at 07:16Florian ScholzFebruary 2nd, 2018 at 13:50D DFebruary 7th, 2018 at 11:16AnonFebruary 2nd, 2018 at 08:07Florian ScholzFebruary 2nd, 2018 at 13:27Sotiris KatsaniotisFebruary 8th, 2018 at 06:25kidkkrFebruary 8th, 2018 at 16:08anononFebruary 9th, 2018 at 01:15ChuanqiFebruary 9th, 2018 at 18:13