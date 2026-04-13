---
title: 'New in Firefox 61: Developer Edition – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2018/05/new-in-firefox-61-developer-edition/
author: Dan Callahan
published: '2018-05-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 61: Developer Edition is available now, and contains a ton of great new features and under-the-hood improvements.

## A Darker Dark Theme

Taking inspiration from [Spinal Tap](https://www.youtube.com/watch?v=46kXH6GGtT0), Developer Edition’s dark theme now darkens more parts of the browser, including the new tab page.

Searchable websites can now be added to Firefox via the “Add Search Engine” item inside the Page Action menu. The sites must describe their search APIs using [OpenSearch](https://developer.mozilla.org/en-US/docs/Web/OpenSearch) metadata.

And yes, the Page Action menu is also dark, if you’re using a dark theme.

## More Powerful Developer Tools

More than just source maps, Firefox 61 understands how tools like Babel and Webpack work, making it possible to seamlessly inspect and interact with your original code right within the Debugger, as if it had never been bundled and minified in the first place. We’re also working to add native support for inspecting components and scopes in modern frameworks like React.

To learn more, see our separate, in-depth blog post: * Debugging Modern Web Applications*.

## Nicer Developer Tools

The Developer Tools have seen numerous quality-of-life improvements.

You can now rearrange tools to suit your individual workflow, and any tabs that don’t fit in the current window remain readily accessible in an overflow menu.

The Network panel also gained prominent drop-down menus for controlling network throttling and importing/exporting [HTTP Archive](https://en.wikipedia.org/wiki/.har) (“HAR”) files.

We’ve also sped up the DevTools across the board, and are [measuring and tracking performance](https://blog.nightly.mozilla.org/2018/04/10/improving-devtools-performance-one-iteration-at-a-time/) as an explicit goal for the team. Even more improvements are on the way.

In Firefox Quantum, we re-implemented many of the DevTools using basic web technologies: HTML, JavaScript, and CSS. We’re even using React inside the DevTools themselves! This means that if you know how to build for the web, you know how to hack on the DevTools. If you’d like to get involved, we have a great [getting started guide](http://docs.firefox-dev.tools/) with pointers to [good first bugs](http://bugs.firefox-dev.tools/) to tackle.

## The Accessibility Inspector

There’s also an entirely new tool available, the Accessibility Inspector, which reveals the logical structure of your page, as it might appear to a screen reader or other assistive software.

This is a low-level tool meant to help you understand how Firefox and screen readers “see” your content. To learn more, including how to enable and use this new tool, check out Marco Zehe’s article [ Introducing the Accessibility Inspector](https://www.marcozehe.de/2018/04/11/introducing-the-accessibility-inspector-in-the-firefox-developer-tools/). If you’re looking for more opinionated tools to help audit and improve your site’s accessibility, consider add-ons like the

[aXe Developer Tools](https://addons.mozilla.org/en-US/firefox/addon/axe-devtools/)or the

[WAVE Accessibility Extension](https://addons.mozilla.org/en-US/firefox/addon/wave-accessibility-tool/).

## Behind the Scenes

Lastly, we landed a number of improvements and refactorings that should make Firefox a better all-around browser.

- Firefox now parses CSS stylesheets in multiple parallel threads. This can significantly improve the time to
*first paint*for websites, especially when there are many stylesheets on a single page. - The multi-tier WebAssembly compiler has been implemented for the AArch64 CPU architecture common in smartphones and tablets. You can read more about the benefits of this compiler design in Lin Clark’s article
*,*.*Making WebAssembly Even Faster* - On macOS, like on Windows, browser add-ons now run in a separate, dedicated process. A continuation of our work with multi-process Firefox, this helps Firefox itself stay responsive, even when an add-on is busy doing work.

Firefox 61 is currently available in [Beta](https://www.mozilla.org/firefox/channel/desktop/#beta) and [Developer Edition](https://www.mozilla.org/firefox/developer/), and it will become the stable version of Firefox on June 26th. If you’d like to keep up with Firefox development as it happens, we recommend reading the [Firefox Nightly Blog](https://blog.nightly.mozilla.org/), or following [@FirefoxNightly](https://twitter.com/firefoxnightly) on Twitter.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.