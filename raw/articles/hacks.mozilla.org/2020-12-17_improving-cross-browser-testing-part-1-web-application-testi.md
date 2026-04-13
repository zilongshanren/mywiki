---
title: 'Improving Cross-Browser Testing, Part 1: Web Application Testing Today – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/12/cross-browser-testing-part-1-web-app-testing-today/
author: Maja Frydrychowicz
published: '2020-12-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Testing web applications can be a challenge. Unlike most other kinds of software, they run across a multitude of platforms and devices. They have to be robust regardless of form factor or choice of browser.

We know this is a problem developers feel: when the [ MDN Developer Needs Assessment](https://insights.developer.mozilla.org/) asked web developers for their top pain points, cross-browser testing was in the top five in both [2019](https://insights.developer.mozilla.org/reports/mdn-web-developer-needs-assessment-2019.html#needs-assessment-overall-needs-ranking) and [2020](https://insights.developer.mozilla.org/reports/mdn-web-developer-needs-assessment-2020.html#needs-assessment-ranking-of-all-needs).

Analysis of the 2020 results revealed a [subgroup](https://insights.developer.mozilla.org/reports/mdn-web-developer-needs-assessment-2020.html#needs-assessment-testing-technicians), comprising 13% of respondents, for whom difficulties writing and running tests were their overall biggest pain point with the web platform.

At Mozilla, we see that as a call to action. With our commitment to building a better Internet, we want to provide web developers the tools they need to build great web experiences – including great tools for testing.

In this series of posts we will explore the current web-application testing landscape and explain what Firefox is doing today to allow developers to run more kinds of tests in Firefox.

## The WebDriver Standard

Most current cross-browser test automation uses [WebDriver](https://www.w3.org/TR/webdriver/), a W3C specification for browser automation. The protocol used by WebDriver originated in [Selenium](https://www.selenium.dev/), one of the oldest and most popular browser automation tools.

To understand the features and limitations of WebDriver, let’s dive in and look at how it works under the hood.

WebDriver provides an HTTP-based synchronous command/response protocol. In this model, clients such as Selenium — called a *local end* in WebDriver parlance — communicate with a *remote end* HTTP server using a fixed set of steps:

- The local end sends an HTTP request representing a WebDriver command to the remote end.
- The remote end takes implementation-specific steps to carry out the command, following the requirements of the WebDriver specification.
- The remote end returns an HTTP response to the local end.

This remote end HTTP server could be built into the browser itself, but the most common setup is for all the HTTP processing to happen in a browser-specific *driver* binary. This accepts the WebDriver HTTP requests and converts them into an internal format for the browser to consume.

For example when automating Firefox, [geckodriver](https://github.com/mozilla/geckodriver/) converts WebDriver messages into Gecko’s custom [Marionette protocol](https://firefox-source-docs.mozilla.org/testing/marionette/index.html), and vice versa. [ChromeDriver](https://chromedriver.chromium.org/) and [SafariDriver](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari) work in a similar way, each using an internal protocol specific to their associated browser.

### Example: A Simple Test Script

To understand this better, let’s take a simple example: navigating to a page, finding an element, and testing a property on that element. From the point of view of a test author, the code to implement this might look like:

```
browser.go("http://localhost:8000")
element = browser.querySelectorAll(".test")[0]
assert element.tag == "div"
```


Each line of code in this example causes a single HTTP request from the local end to the remote end, representing a single WebDriver command.

The program does not continue until the local end receives the corresponding HTTP response. In the initial `browser.go`

call, for example, the remote end will only send its response once the browser has finished loading the requested page.

On the wire that program generates the following HTTP traffic (some unimportant details omitted for brevity):

POST /session/25bc4b8a-c96e-4e61-9f2d-19c021a6a6a4/url HTTP/1.1 Content-Length: 43 {"url": "http://localhost:8000/index.html"}

At this point the browser performs the network operations to navigate to the requested URL, `http://localhost:8000/index.html`

. Once that page has finished loading, the remote end sends the following response back to the automation client.

HTTP/1.1 200 OK content-type: application/json; charset=utf-8 content-length: 14 {"value":null}

Next comes the request to find the element with class `test`

:

POST /session/25bc4b8a-c96e-4e61-9f2d-19c021a6a6a4/elements HTTP/1.1 Content-Length: 43 {"using": "css selector", "value": ".test"}

HTTP/1.1 200 OK content-type: application/json; charset=utf-8 content-length: 90 {"value":[{"element-6066-11e4-a52e-4f735466cecf":"0d861ba8-6901-46ef-9a78-0921c0d6bb5a"}]}

And finally the request to get the element tag name:

GET /session/25bc4b8a-c96e-4e61-9f2d-19c021a6a6a4/element/0d861ba8-6901-46ef-9a78-0921c0d6bb5a/name HTTP/1.1

HTTP/1.1 200 OK content-type: application/json; charset=utf-8 content-length: 15 {"value":"div"}

Even though the three lines of the code involve significant network operations, the control flow is simple to understand and easy to express in a large range of common programming languages. That’s very different from the situation inside the browser itself, where an apparently simple operation like loading a page has a large number of asynchronous steps.

The fact that the remote end handles all that complexity makes it much easier to write automation clients.

### Flexibility

In the simple model above, the local end talks directly to the driver binary which is in control of the browser. But in real test deployment scenarios, the situation may be more complex; arbitrary HTTP middleware can be deployed between the local end and the driver.

One common application of this is to provide provisioning capabilities. Using an intermediary such as [Selenium Grid,](https://www.selenium.dev/documentation/en/grid/) a single WebDriver HTTP endpoint can front a large number of OS and browser combinations, proxying the commands for each test to the requested machine.

The well-understood semantics of HTTP, combined with the wealth of existing tooling make this kind of setup relatively easy to build and deploy at scale, even over untrusted, possibly high latency, networks like the internet.

This is important to services such as [SauceLabs](https://saucelabs.com/) and [BrowserStack](https://www.browserstack.com) which run automation on remote servers.

### Limitations of HTTP-Based WebDriver

The synchronous command/response model of HTTP imposes some limitations on WebDriver. Since the browser can only respond to commands, it’s hard to model things which may happen in the browser outside the context of a specific request.

A clear example of this is alerts. Alerts can appear at any time, so every WebDriver command has to specifically check for an alert being present before running.

Similar problems occur with logging; the ideal API would send log events as soon as they are generated, but with HTTP-based WebDriver this isn’t possible. Instead, a logging API requires buffering on the browser side, and the client must accept that it may not receive all log messages.

Concerns about standardizing a poor, unreliable API means that logging features have not yet made it into the W3C specification for WebDriver, despite being a common user request.

One of the reasons WebDriver adopted the HTTP model despite these limitations was the simplicity of the programming model. With a fully blocking API, one could easily write WebDriver clients using only language features that were mainstream in the early 2000s.

Since then, many programming languages have gained first-class support for handling events and asynchronous control flow. This means that some of the underlying assumptions that went into the original WebDriver protocol — like asynchronous, event-driven code being too hard to write — are no longer true.

## DevTools Protocols

As well as automation via WebDriver, modern browsers also provide remote access for the use of the browser’s DevTools. This is essential for cases where it’s difficult to debug an issue on the same machine where the page itself is running, like an issue that only occurs on mobile.

Different browsers provide different DevTools features, which often require explicit support in the engine and expose implementation details that are not visible to web content. Therefore it’s unsurprising that each browser engine has a unique DevTools protocol, according to their particular requirements.

In DevTools, there’s a core requirement that UI must respond to events emitted by the browser engine. Examples include logging console messages and network requests as they come in so that a user can follow progress.

This means that DevTools protocols don’t use the command/response paradigm of HTTP. Instead, they use a bidirectional protocol in which messages may originate from either the client or the browser. This allows the DevTools to update in real time, responding to changes in the browser as they happen.

Remote automation isn’t a core use case of DevTools. Some operations that are common in one case are rare in the other. For example, client-initiated navigation is present in almost all automated tests, but is rare in DevTools.

Nevertheless, low-level control needed when debugging mean it’s possible to write many automation features on top of the DevTools protocol feature set. Indeed in some browsers such as Chrome, the browser-internal message format used to bridge the gap between the WebDriver binary and the browser itself is in fact the DevTools protocol.

This has inevitably led to the question of whether it’s possible to build automation on top of the DevTools protocol directly. With languages offering better support for asynchronous control flow, and modern web applications demanding more low-level control for testing, libraries such as Google’s [Puppeteer](https://developers.google.com/web/tools/puppeteer) have taken DevTools protocols and constructed automation-specific client libraries on top.

These libraries support advanced features such as network request interception which are hard to build on top of HTTP-based WebDriver. The typically promise-based APIs also feel more like modern front-end programming, which has made these tools popular with web developers.

Even mainly WebDriver-based tools are adding additional features which can’t be realised through WebDriver alone. For example some of the new features in [Selenium 4](https://saucelabs.com/blog/new-tricks-in-selenium-4), such as access to console logs and better support for HTTP Authentication, require bidirectional communication, and will initially only be supported in browsers which can speak Chrome’s DevTools protocol.

### DevTools Difficulties

Although using DevTools for automation is appealing in terms of the feature set, it’s also fraught with problems.

DevTools protocols are browser-specific and can expose a lot of internal state that’s not part of the Web Platform. This means that libraries using DevTools features for automation are typically tied to a specific rendering engine.

They are also beholden to changes in those engines; the tight coupling to the engine internals means DevTools protocols usually offer very limited guarantees of stability.

For the DevTools themselves this isn’t a big problem; the same team usually owns the front-end and the back-end so any refactor just has to update both the client and server at the same time, and cross-version compatibility is not a serious concern. But for automation, it imposes a significant burden on both the client library developer and the test authors.

With WebDriver a single client can work with any supported browser release. With DevTools-based automation, a new client may be required for each browser version. This is the case for Puppeteer, for example, where each Puppeteer release is tied to a particular version of Chromium.

The fact that DevTools protocols are browser-specific makes it very challenging to use them as the foundation for cross-browser tooling. Some automation clients, like [Cypress](https://www.cypress.io/) and Microsoft’s [Playwright](https://playwright.dev/), have made heroic efforts here, eschewing WebDriver but still supporting multiple browsers.

Using a combination of existing DevTools protocols and custom protocols implemented through patches to the underlying browser code or via WebExtensions, they provide features not possible in WebDriver whilst supporting several browser engines.

Requiring such a large amount of code to be maintained by the automation library, and putting the library on the treadmill of browser engine updates, makes maintenance difficult and gives the library authors less time to focus on their core automation features.

## Summary and Next Steps

As we have seen, the web application testing ecosystem is becoming fragmented. Most cross-browser testing uses WebDriver; a W3C specification that all major browser engines support.

However, limitations in WebDriver’s HTTP-based protocol mean that automation libraries are increasingly choosing to use browser-specific DevTools protocols to implement advanced features, foregoing cross-browser support when they do.

Test authors shouldn’t have to choose between access to functionality, and browser-specific tooling. And client authors shouldn’t be forced to keep up with the often-breakneck pace of browser engine development.

In our next post, we’ll describe some work Mozilla has done to bring previously Chromium-only test tooling to Firefox.

## Acknowledgements

Thanks to Tantek Çelik, Karl Dubost, Jan Odvarko, Devin Reams, Maire Reavy, Henrik Skupin, and Mike Taylor for their valuable feedback and suggestions.

## About
[
Maja Frydrychowicz ](https://www.erranderr.com/)

## About
[
James Graham ](https://hoppipolla.co.uk)

Software engineer focused on maintaining a healthy open web. Web-platform-tests core team member.

## One comment

AlDecember 17th, 2020 at 23:47