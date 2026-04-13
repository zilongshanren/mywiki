---
title: Puppeteer Support for the Cross-Browser WebDriver BiDi Standard – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2023/12/puppeteer-webdriver-bidi/
author: James Graham
published: '2023-12-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We are pleased to share that [Puppeteer](https://pptr.dev/) now supports the next-generation, cross-browser [WebDriver BiDi standard](https://w3c.github.io/webdriver-bidi/). This new protocol makes it easy for web developers to write automated tests that work across multiple browser engines.

## How Do I Use Puppeteer With Firefox?

The WebDriver BiDi protocol is supported starting with [Puppeteer v21.6.0](https://pptr.dev/webdriver-bidi). When calling `puppeteer.launch`

pass in `"firefox"`

as the product option, and `"webDriverBiDi"`

as the protocol option:

```
const browser = await puppeteer.launch({
product: 'firefox',
protocol: 'webDriverBiDi',
})
```


You can also use the `"webDriverBiDi"`

protocol when testing in Chrome, reflecting the fact that WebDriver BiDi offers a single standard for modern cross-browser automation.

In the future we expect `"webDriverBiDi"`

to become the default protocol when using Firefox in Puppeteer.

## Doesn’t Puppeteer Already Support Firefox?

Puppeteer has had experimental support for Firefox based on a partial re-implementation of the proprietary [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) (CDP). This approach had the advantage that it worked without significant changes to the existing Puppeteer code. However the CDP implementation in Firefox is incomplete and has significant technical limitations. In addition, the CDP protocol itself is not designed to be cross browser, and undergoes frequent breaking changes, making it unsuitable as a long-term solution for cross-browser automation.

To overcome these problems, we’ve worked with the WebDriver Working Group at the W3C to create a standard automation protocol that meets the needs of modern browser automation clients: this is WebDriver BiDi. For more details on the protocol design and how it compares to the classic HTTP-based WebDriver protocol, see our [earlier](https://hacks.mozilla.org/2020/12/cross-browser-testing-part-1-web-app-testing-today/) [posts](https://hacks.mozilla.org/2021/01/improving-cross-browser-testing-part-2-new-automation-features-in-firefox-nightly/).

As the standardization process has progressed, the Puppeteer team has added a WebDriver BiDi backend in Puppeteer, and provided feedback on the specification to ensure that it meets the needs of Puppeteer users, and that the protocol design enables existing CDP-based tooling to easily transition to WebDriver BiDi. The result is a single protocol based on open standards that can drive both Chrome and Firefox in Puppeteer.

## Are All Puppeteer Features Supported?

Not [yet](https://puppeteer.github.io/ispuppeteerwebdriverbidiready/); WebDriver BiDi is still a work in progress, and doesn’t yet cover the full feature set of Puppeteer.

Compared to the Chrome+CDP implementation, there are some feature gaps, including support for accessing the cookie store, network request interception, some emulation features, and permissions. These features are actively being standardized and will be integrated as soon as they become available. For Firefox, the only missing feature compared to the Firefox+CDP implementation is cookie access. In addition, WebDriver BiDi already offers improvements, including better support for multi-process Firefox, which is essential for testing some websites. More information on the complete set of supported APIs can be found in the [Puppeteer documentation](https://pptr.dev/webdriver-bidi), and as new WebDriver-BiDi features are enabled in Gecko we’ll publish details on the [Firefox Developer Experience blog](https://fxdx.dev/).

Nevertheless, we believe that the WebDriver-based Firefox support in Puppeteer has reached a level of quality which makes it suitable for many real automation scenarios. For example at Mozilla we have successfully [ported](https://github.com/mozilla/pdf.js/pull/17172) our Puppeteer tests for [pdf.js](https://mozilla.github.io/pdf.js/) from Firefox+CDP to Firefox+WebDriver BiDi.

## Is Firefox’s CDP Support Going Away?

We currently don’t have a specific timeline for removing CDP support. However, maintaining multiple protocols is not a good use of our resources, and we expect WebDriver BiDi to be the future of remote automation in Firefox. If you are using the CDP support outside of the context of Puppeteer, we’d love to hear from you (see below), so that we can understand your use cases, and help transition to WebDriver BiDi.

## Where Can I Provide Feedback?

For any issues you experience when porting Puppeteer tests to BiDi, please open issues in the [Puppeteer issue tracker](https://github.com/puppeteer/puppeteer/issues/new/choose), unless you can verify the bug is in the Firefox implementation, in which case please [file a bug on Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Remote%20Protocol&component=WebDriver%20BiDi).

If you are currently using CDP with Firefox, please join the [#webdriver matrix channel](https://matrix.to/#/#webdriver:mozilla.org) so that we can discuss your use case and requirements, and help you solve any problems you encounter porting your code to WebDriver BiDi.

**Update**: The Puppeteer team have published “[Harness the Power of WebDriver BiDi: Chrome and Firefox Automation with Puppeteer](https://developer.chrome.com/blog/puppeteer-webdriver-bidi-2023)“.

## About
[
James Graham ](https://hoppipolla.co.uk)

Software engineer focused on maintaining a healthy open web. Web-platform-tests core team member.