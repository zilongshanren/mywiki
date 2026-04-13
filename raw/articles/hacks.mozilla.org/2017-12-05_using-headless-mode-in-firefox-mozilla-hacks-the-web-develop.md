---
title: Using Headless Mode in Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/12/using-headless-mode-in-firefox/
author: Sergi Mansilla
published: '2017-12-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*If you know the ropes, good news! Firefox now has support for headless mode, making it easier to use as a backend to automated tools. You can jump ahead to learn how to use it.*

Browser automation is not a new idea, but is an increasingly important part of how modern websites are built, tested, and deployed. Automation setups range from scripts run on local machines to vast deployments of specialized servers running in the cloud. To this end, browsers have long supported some level of automated control, usually via third-party driver software.

Browsers are at their core a user interface to the web, and a *graphical* user interface in particular. This poses a few problems for automation. In some environments, there may be no graphical display available, or it may be desirable to not have the browser appear at all when being controlled. This has required tools like [virtual display software](https://en.wikipedia.org/wiki/Xvfb) in order to run properly, adding complexity. More recently, tools like [Lighthouse](https://developers.google.com/web/tools/lighthouse/) have packaged complex automated tests into a simple attractive package. They use the browser as a testing runtime, but there’s no need to display the browser window while the tests run.

For years, the best way to load webpages without displaying UI was [PhantomJS](http://phantomjs.org/), which is based on WebKit. While it remains a fantastic tool, it’s valuable to be able to run automated browser tests in official browsers, and so it’s valuable to have a headless mode available.

In June, Google shipped Chrome 59 featuring a headless mode, and Firefox has followed close behind with headless mode available on all platforms starting with version 56.

## Using Firefox in Headless Mode

Launching Firefox in headless mode is simple enough. From the command line, simply add the `-headless`

argument:

```
/path/to/firefox -headless
```


Great! Firefox is running in headless mode. How do you control it?

Right.

There are multiple options out there, many of which actually pre-date headless mode itself. Let’s review them!

### Selenium/WebDriver

*There’s a wealth of of information about selenium-webdriver testing on the MDN page for headless mode. Here’s a high-level overview.*

Selenium is a venerable tool for browser automation, and it’s all the better with a headless browser. Writing a headless test is just as it was before, and there are some great libraries out there to make it easier. For instance, here is a basic node script to capture a screenshot of a webpage:

```
const { Builder } = require('selenium-webdriver');
const firefox = require('selenium-webdriver/firefox');
const fs = require('fs');
require('geckodriver');
async function capture(url) {
const binary = new firefox.Binary(firefox.Channel.RELEASE);
binary.addArguments('-headless'); // until newer webdriver ships
const options = new firefox.Options();
options.setBinary(binary);
// options.headless(); once newer webdriver ships
const driver = new Builder().forBrowser('firefox')
.setFirefoxOptions(options).build();
await driver.get(url);
const data = await driver.takeScreenshot();
fs.writeFileSync('./screenshot.png', data, 'base64');
driver.quit();
}
capture('https://hacks.mozilla.org/');
```


Really the only difference when using headless mode is to make sure the right argument is passed.

That said, if you just need a screenshot of a webpage, that’s built in:

```
# -screenshot assumes -headless
firefox -screenshot https://hacks.mozilla.org/
# want to pick the resolution?
firefox -screenshot https://hacks.mozilla.org/ --window-size=480,1000
```


### DevTools Debugging Protocol

Firefox has a [debugging protocol](https://searchfox.org/mozilla-central/source/devtools/docs/backend/protocol.md) that allows scripts to drive its DevTools from remotely. There are libraries such as [node-firefox](https://github.com/mozilla/node-firefox) and [foxdriver](https://github.com/saucelabs/foxdriver) that use this protocol to remotely debug websites, fetch their logs, etc. For security reasons, the remote debugging protocol is not enabled by default, but can be enabled in preferences or from the command line:

```
/path/to/firefox --start-debugger-server 6000 -headless
```


In addition, the remote debugging protocol also speaks WebSockets! You can connect a webpage to a remote Firefox and drive it from there:

```
/path/to/firefox --start-debugger-server ws:6000 -headless
```


## Learn (Lots) More!

This is an overview of what’s possible with headless Firefox and it’s the early days of support, but there’s already great information out there. In particular:

- Brendan Dahl (who’s responsible for Firefox’s headless mode- thanks Brendan!) wrote a post on
[using headless Firefox as a substitute for PhantomJS](https://adriftwith.me/coding/2017/04/21/headless-slimerjs-with-firefox/) - Myk Melez has a much deeper post on
[using selenium-webdriver to control Firefox](https://mykzilla.org/2017/08/30/headless-firefox-in-node-js-with-selenium-webdriver/) - If you’re looking for an example production-level headless code, I wrote a simple command line tool called
[FoxShot](https://github.com/potch/foxshot)to make capturing lots of screenshots from Firefox easier.

Happy scripting!

## 5 comments

GPDecember 5th, 2017 at 18:52RickDecember 6th, 2017 at 01:01Philipp HanckeDecember 7th, 2017 at 01:04PatrickDecember 6th, 2017 at 02:51MuhammadDecember 7th, 2017 at 09:12