---
title: Announcing Official Puppeteer Support for Firefox – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2024/08/puppeteer-support-for-firefox/
author: James Graham
published: '2024-08-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We’re pleased to announce that, as of version 23, the [Puppeteer](https://pptr.dev/) browser automation library now has first-class support for Firefox. This means that it’s now easy to write automation and perform end-to-end testing using Puppeteer, and run against both Chrome and Firefox.

## How to Use Puppeteer With Firefox

To get started, simply set the product to “`firefox`

” when starting Puppeteer:

```
import puppeteer from "puppeteer";
const browser = await puppeteer.launch({
browser: "firefox"
});
const page = await browser.newPage();
// ...
await browser.close();
```


As with Chrome, Puppeteer is able to download and launch the latest stable version of Firefox, so running against either browser should offer the same developer experience that Puppeteer users have come to expect.

Whilst the features offered by Puppeteer won’t be a surprise, bringing support to multiple browsers has been a significant undertaking. The Firefox support is not based on a Firefox-specific automation protocol, but on WebDriver BiDi, a cross browser protocol that’s undergoing standardization at the W3C, and currently has implementation in both Gecko and Chromium. This use of a cross-browser protocol should make it much easier to support many different browsers going forward.

Later in this post we’ll dive into some of the more technical background behind WebDriver BiDi. But first we’d like to call out how today’s announcement is a great demonstration of how productive collaboration can advance the state of the art on the web. Developing a new browser automation protocol is a lot of work, and great thanks goes to the Puppeteer team and the other members of the W3C Browser Testing and Tools Working Group, for all their efforts in getting us to this point.

You can also check out the Puppeteer team’s[ post](https://developer.chrome.com/blog/firefox-support-in-puppeteer-with-webdriver-bidi) about making WebDriver BiDi production ready.

## Key Features

For long-time Puppeteer users, the features available are familiar. However for people in other automation and testing ecosystems — particularly those that until recently relied entirely on HTTP-based WebDriver — this section outlines some of the new functionality that WebDriver BiDi makes possible to implement in a cross-browser manner.

### Capturing of Log Messages

A common requirement when testing web apps is to ensure that there are no unexpected errors reported to the console. This is also a case where an event-based protocol shines, since it avoids the need to poll the browser for new log messages.

```
import puppeteer from "puppeteer";
const browser = await puppeteer.launch({
browser: "firefox"
});
const page = await browser.newPage();
page.on('console', msg => {
console.log(`[console] ${msg.type()}: ${msg.text()}`);
});
await page.evaluate(() => console.debug('Some Info'));
await browser.close();
```


Output:

[console] debug: Some Info

### Device Emulation

Often when testing a reactive layout it’s useful to be able to ensure that the layout works well at multiple screen dimensions, and device pixel ratios. This can be done by using a real mobile browser, either on a device, or on an emulator. However for simplicity it can be useful to perform the testing on a desktop set up to mimic the viewport of a mobile device. The example below shows loading a page with Firefox configured to emulate the viewport size and device pixel ratio of a Pixel 5 phone.

```
import puppeteer from "puppeteer";
const device = puppeteer.KnownDevices["Pixel 5"];
const browser = await puppeteer.launch({
browser: "firefox"
});
const page = await browser.newPage();
await page.emulate(device);
const viewport = page.viewport();
console.log(
`[emulate] Pixel 5: ${viewport.width}x${viewport.height}` +
` (dpr=${viewport.deviceScaleFactor}, mobile=${viewport.isMobile})`
);
await page.goto("https://www.mozilla.org");
await browser.close();
```


Output:

[emulate] Pixel 5: 393x851 (dpr=3, mobile=true)

### Network Interception

A common requirement for testing is to be able to track and intercept network requests. Interception is especially useful for avoiding requests to third party services during tests, and providing mock response data. It can also be used to handle HTTP authentication dialogs, and override parts of the request and response, for example adding or removing headers. In the example below we use network request interception to block all requests to web fonts on a page, which might be useful to ensure that these fonts failing to load doesn’t break the site layout.

```
import puppeteer from "puppeteer";
const browser = await puppeteer.launch({
browser: 'firefox'
});
const page = await browser.newPage();
await page.setRequestInterception(true);
page.on("request", request => {
if (request.url().includes(".woff2")) {
// Block requests to custom user fonts.
console.log(`[intercept] Request aborted: ${request.url()}`);
request.abort();
} else {
request.continue();
}
});
const response = await page.goto("https://support.mozilla.org");
console.log(
`[navigate] status=${response.status()} url=${response.url()}`
);
await browser.close();
```


Output:

[intercept] Request aborted: https://assets-prod.sumo.prod.webservices.mozgcp.net/static/Inter-Bold.3717db0be15085ac.woff2 [navigate] status=200 url=https://support.mozilla.org/en-US/

### Preload Scripts

Often automation tooling wants to provide custom functionality that can be implemented in JavaScript. Whilst WebDriver has always allowed injecting scripts, it wasn’t possible to ensure that an injected script was always run before the page started loading, making it impossible to avoid races between the page scripts and the injected script.

WebDriver BiDi provides “preload” scripts which can be run before a page is loaded. It also provides a means to emit custom events from scripts. This can be used, for example, to avoid polling for expected elements, but instead using a mutation observer that fires as soon as the element is available. In the example below we wait for the <title> element to appear on the page, and log its contents.

```
import puppeteer from "puppeteer";
const browser = await puppeteer.launch({
browser: 'firefox',
});
const page = await browser.newPage();
const gotMessage = new Promise(resolve =>
page.exposeFunction("sendMessage", async message => {
console.log(`[script] Message from pre-load script: ${message}`);
resolve();
})
);
await page.evaluateOnNewDocument(() => {
const observer = new MutationObserver(mutationList => {
for (const mutation of mutationList) {
if (mutation.type === "childList") {
for (const node of mutation.addedNodes) {
if (node.tagName === "TITLE") {
sendMessage(node.textContent);
}
}
}
};
});
observer.observe(document.documentElement, {
subtree: true,
childList: true,
});
});
await page.goto("https://support.mozilla.org");
await gotMessage;
await browser.close();
```


Output:

[script] Message from pre-load script: Mozilla Support

## Technical Background

Until recently people wishing to automate browsers had two main choices:

- Use the W3C
[WebDriver](https://w3c.github.io/webdriver/)API, which was based on earlier work by the Selenium project. - Use a browser-specific API for talking to each supported browser such as
[Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)(CDP) for Chromium-based browsers, or Firefox’s[Remote Debugging Protocol](https://firefox-source-docs.mozilla.org/devtools/backend/protocol.html)(RDP) for Gecko-based browsers.

Unfortunately both of those options come with significant tradeoffs. The “classic” WebDriver API is HTTP-based, and its model involves automation sending a command to the browser and waiting for a response. That works well for automation scenarios where you load a page and then verify, for example, that some element is displayed, but the inability to get events — e.g. console logs — back from the browser, or run multiple commands concurrently, makes the API a poor fit for more advanced use cases.

By contrast, browser-specific APIs have generally been designed around supporting the complex use cases of in-browser devtools. This has given them a feature set far in advance of what’s possible using WebDriver, as they need to support use cases such as recording console logs, or network requests.

Therefore, browser automation clients have been forced to make the choice between supporting many browsers using a single protocol and providing a limited feature set, or providing a richer feature set but having to implement multiple protocols to provide functionality separately for each supported browser. This obviously increased the cost and complexity of creating great cross-browser automation, which isn’t a good situation, especially when developers [commonly cite](https://mdn.dev/archives/insights/reports/mdn-web-testing-report-2021.html) cross-browser testing as one the main pain points in developing for the web.

Long time developers might notice the analogy here to the situation with editors before the development of [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP). At that time each text editor or IDE had to implement bespoke support for each different programming language. That made it hard to get support for a new language into all the tools that developers were using. The advent of LSP changed that by providing a common protocol that could be supported by any combination of editor and programming language. For a new programming language like TypeScript to be supported across all editors it no longer needs to get them to add support one-by-one; it only needs to provide an LSP server and it will automatically be supported across any LSP-supporting editor. The advent of this common protocol has also enabled things that were hard to imagine before. For example specific libraries like Tailwind getting their own [LSP implementation](https://www.npmjs.com/package/@tailwindcss/language-server) to enable bespoke editor functionality.

So to improve cross-browser automation we’ve taken a similar approach: developing [WebDriver BiDi](https://w3c.github.io/webdriver-bidi/), which brings the automation featureset previously limited to browser-specific protocols to a standardized protocol that can be implemented by any browser and used by any automation tooling in any programming language.

At Mozilla we see this strategy of standardizing protocols in order to remove barriers to entry, allow a diverse ecosystem of interoperable implementations to flourish, and enable users to choose those best suited to their needs as a key part of our manifesto and [web vision](https://www.mozilla.org/en-US/about/webvision/full/#openness).

For more details about the design of WebDriver BiDi and how it relates to classic WebDriver, please see our [earlier](https://hacks.mozilla.org/2020/12/cross-browser-testing-part-1-web-app-testing-today/) [posts](https://hacks.mozilla.org/2021/01/improving-cross-browser-testing-part-2-new-automation-features-in-firefox-nightly/).

## Removing experimental CDP support in Firefox

As part of our early work on improving cross-browser testing, we shipped a partial implementation of CDP, limited to a few commands and events needed to support testing use cases. This was previously the basis of experimental support for Firefox in Puppeteer. However, once it became clear that this was not the way forward for cross-browser automation, effort on this was stopped. As a result it is unmaintained and doesn’t work with modern Firefox features such as site isolation. Therefore support is [scheduled to be removed](https://fxdx.dev/deprecating-cdp-support-in-firefox-embracing-the-future-with-webdriver-bidi/) at the end of 2024.

If you are currently using CDP with Firefox, and don’t know how to transition to WebDriver BiDi, please reach out using one of the [channels listed at the bottom of this post](https://hacks.mozilla.org#contact-us), and we will discuss your requirements.

## What’s Next?

Although Firefox is now officially supported in Puppeteer, and has enough functionality to cover many automation and testing scenarios, there are still some APIs that remain unsupported. These broadly fall into three categories (consult the [Puppeteer documentation](https://pptr.dev/webdriver-bidi) for a full list):

- Highly CDP-specific APIs, notably those in the
[CDPSession](https://pptr.dev/api/puppeteer.cdpsession)module. These are unlikely to be supported directly, but specific use cases that currently require these APIs could be candidates for standardization. - APIs which require further standards work. For example
[page.accessibility.snapshot](https://pptr.dev/api/puppeteer.accessibility.snapshot)returns a dump of the Chromium accessibility tree. However because there’s currently no standardized description of what that tree should look like this is hard to make work in a cross-browser way. There are also cases which are much more straightforward, as they only require work on the WebDriver BiDi spec itself; for example[page.setGeolocation](https://pptr.dev/api/puppeteer.page.setgeolocation). - APIs which have a standard but are not yet implemented, for example the ability to execute scripts in workers required for commands like
[WebWorker.evaluate](https://pptr.dev/api/puppeteer.webworker.evaluate).

We expect to fill these gaps going forward. To help prioritize, we’re interested in your feedback: Please try running your Puppeteer tests in Firefox! If you’re unable to get them in Firefox because of a bug or missing feature, please let us know using one of the methods below so that we can take it into account when planning our future standards and implementation work:

- For Firefox implementation bugs, please file a bug on
[Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Remote+Protocol&component=WebDriver+BiDi) - If you’re confident that the issue is in Puppeteer, please file a bug in their
[issue tracker](https://github.com/puppeteer/puppeteer/issues). - For features missing from the WebDriver BiDi
[specification](https://w3c.github.io/webdriver-bidi/), please file an issue on[GitHub](https://github.com/w3c/webdriver-bidi/issues/) - If you want to talk to us about use cases or requirements, please use the
[#webdriver](https://matrix.to/#/#webdriver:mozilla.org)channel on Mozilla’s Matrix instance or email[dev-webdriver@mozilla.org](mailto:dev-webdriver@mozilla.org).

## About
[
James Graham ](https://hoppipolla.co.uk)

Software engineer focused on maintaining a healthy open web. Web-platform-tests core team member.