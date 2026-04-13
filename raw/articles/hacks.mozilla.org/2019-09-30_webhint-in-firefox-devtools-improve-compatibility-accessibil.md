---
title: 'WebHint in Firefox DevTools: Improve Compatibility, Accessibility and more
  – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/09/webhint-in-firefox-devtools-improve-compatibility-accessibility-and-more/
author: Harald Kirschner
published: '2019-09-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Creating experiences that look and work great across different browsers is one of the biggest challenges on the web. It also is the most rewarding part, as it gets your app to as many users as possible. On the other hand, cross-browser compatibility is also the web’s biggest frustration. Testing legacy browsers late in the development process can break a feature that you spent hours on, even requiring rewrites to fix.

What if the tools in your primary development browser could warn you sooner? Thanks to [Webhint in Firefox DevTools](https://addons.mozilla.org/en-US/firefox/addon/webhint/), we can do exactly that, and more.

### The Webhint engine

[Webhint](http://webhint.io/) provides feedback about your site’s compatibility, performance, security, and accessibility to guide improvements. A key benefit is integration across the development cycle — while you author in [VS Code](https://marketplace.visualstudio.com/items?itemName=webhint.vscode-webhint), test in [CI/CD automation](https://www.npmjs.com/package/hint), or benchmark sites in the [online scanner](https://webhint.io/scanner/). Having Webhint available in DevTools adds in-page context and inspection capabilities.

Firefox DevTools was happy to collaborate with the Webhint team, which just [released version 1.0](https://medium.com/webhint/the-webhint-browser-extension-v1-release-df9044ddaf69) of their extension. With the recommendations that the DevTools panel provides, developers on any browser (there is also a [Chrome extension](https://medium.com/webhint/announcing-the-webhint-browser-extension-abb22f4cfeb)) can spend less time looking up cross-browser compatibility tables like [caniuse or MDN](https://hacks.mozilla.org/2019/09/caniuse-and-mdn-compat-data-collaboration/). The cross-browser guidance for CSS and HTML, a core part of the 1.0 release, is also one of the first projects to apply MDN’s [browser-compat-data](https://github.com/mdn/browser-compat-data) on code to detect compatibility.

### The foundation to build on

The hints are not rules written in stone. In fact, the [hint engine](https://github.com/webhintio/hint/) is extensible by design so developers can capture their own expertise and best practices for their projects. We also have plans to tweak the heuristics behind recommendations, especially for new ground like compatibility, based on your feedback. We are also working to integrate recommendations further into DevTools. Everything should be at your fingertips when you need it.

### Wrapping up

Install [Webhint for Firefox](https://addons.mozilla.org/en-US/firefox/addon/webhint/), [Chrome](https://chrome.google.com/webstore/detail/webhint/gccemnpihkbgkdmoogenkbkckppadcag?hl=en) or [Edge (Chromium)](https://microsoftedge.microsoft.com/insider-addons/detail/mlgfbihcfnkaenjpdcngdnhcpkdmcdee) and run it against your old and new projects. Find out how you could further optimize compatibility, security, accessibility, and speed. We hope it will help you to make your site work for as many users as possible.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

## 5 comments

ThomasSeptember 30th, 2019 at 04:30Harald Kirschner (digitarald)October 2nd, 2019 at 08:51jopOctober 8th, 2019 at 07:56maikOctober 10th, 2019 at 11:04Harald Kirschner (digitarald)October 15th, 2019 at 10:55